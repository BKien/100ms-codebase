// Read-only Figma Plugin API script. Prefix with explicit approved captureTargets.
// No loadAllPagesAsync, source mutation, API fallback or full-file traversal.
const page = await figma.getNodeByIdAsync(captureTargets[0].page_id);
if (!page || page.type !== 'PAGE') throw new Error('Approved page missing');
await figma.setCurrentPageAsync(page);
const properties = [
  'id','type','name','visible','opacity','blendMode','x','y','width','height',
  'relativeTransform',
  'rotation','constraints','layoutMode','layoutWrap','layoutSizingHorizontal',
  'layoutSizingVertical','primaryAxisSizingMode','counterAxisSizingMode',
  'primaryAxisAlignItems','counterAxisAlignItems','counterAxisAlignContent',
  'paddingLeft','paddingRight','paddingTop','paddingBottom','itemSpacing',
  'counterAxisSpacing','layoutAlign','layoutGrow','layoutPositioning','clipsContent',
  'fills','strokes','strokeWeight','strokeAlign','strokeCap','strokeJoin','dashPattern',
  'strokeTopWeight','strokeBottomWeight','strokeLeftWeight','strokeRightWeight',
  'effects','isMask','maskType','cornerRadius','cornerSmoothing','topLeftRadius',
  'topRightRadius','bottomLeftRadius','bottomRightRadius','fillStyleId',
  'strokeStyleId','effectStyleId','textStyleId','characters','fontName','fontSize',
  'fontWeight','lineHeight','letterSpacing','textAlignHorizontal','textAlignVertical',
  'textAutoResize','textCase','textDecoration','paragraphIndent','paragraphSpacing',
  'listSpacing','hangingPunctuation','hangingList','textTruncation','maxLines',
  'arcData','pointCount','innerRadius','booleanOperation',
  'componentProperties','componentPropertyReferences','componentPropertyDefinitions',
  'variantProperties'
];
const nativeAssets = new Map();
const nativeGeometryOwners = new Set();
const cachedHashes = new Set(typeof knownAssetHashes === 'undefined' ? [] : knownAssetHashes);
const failures = [];
const clean = v => JSON.parse(JSON.stringify(v, (_, value) => typeof value === 'symbol' ? 'MIXED' : value));
async function walk(node, vectorOwner = null) {
  const result = {};
  for (const key of properties) {
    if (!(key in node)) continue;
    let value;
    try { value = node[key]; }
    catch (error) {
      if (key.startsWith('component') || key === 'variantProperties') {
        (result.metadata_unavailable ||= []).push({property:key,reason:'source-component-metadata-error'});
        continue;
      }
      throw error;
    }
    if (value !== undefined) result[key] = typeof value === 'symbol' ? 'MIXED' : clean(value);
  }
  if (node.type === 'TEXT') {
    result.textRuns = clean(node.getStyledTextSegments([
      'fontName','fontSize','fills','letterSpacing','lineHeight',
      'textCase','textDecoration','textStyleId'
    ]));
  }
  for (const key of ['fills','strokes']) {
    const paints = result[key];
    if (!Array.isArray(paints)) continue;
    for (const paint of paints) {
      if (paint.type === 'IMAGE' && paint.imageHash && !nativeAssets.has(paint.imageHash)) {
        try {
          const image = figma.getImageByHash(paint.imageHash);
          if (!image) throw new Error('Missing image');
          const bytes = await image.getBytesAsync();
          const hash = nativeHash(bytes);
          nativeAssets.set(paint.imageHash, {identifier:paint.imageHash,kind:'image-paint',
            dimensions:await image.getSizeAsync(), native_sha256:hash, byte_size:bytes.length,
            ...(cachedHashes.has(hash) ? {cached_sha256:hash} : {data:figma.base64Encode(bytes)})});
        } catch (error) { failures.push({identifier:paint.imageHash,kind:'image-paint',reason:'native-image-read-failed'}); }
      }
    }
  }
  if (['VECTOR','BOOLEAN_OPERATION','LINE','ELLIPSE','POLYGON','STAR'].includes(node.type)) {
    if (vectorOwner && nativeGeometryOwners.has(vectorOwner)) {
      result.geometry_kind = 'native-boolean-descendant';
      if ('vectorPaths' in node) result.vectorPaths = clean(node.vectorPaths);
    } else {
      result.geometry_asset_identifier = vectorOwner || node.id;
    }
    if (!vectorOwner) {
      try {
        const svg = await node.exportAsync({format:'SVG_STRING'});
        const hash = nativeHash(svg);
        nativeAssets.set(node.id, {identifier:node.id,kind:'vector-export',native_sha256:hash,
          ...(cachedHashes.has(hash) ? {cached_sha256:hash} : {svg})});
      } catch (error) {
        if (node.type === 'VECTOR' && node.vectorPaths.length) {
          result.vectorPaths = clean(node.vectorPaths);
          result.geometry_kind = 'native-vector-paths';
          result.svg_export_status = 'unavailable; exact native paths captured';
          delete result.geometry_asset_identifier;
        } else if (node.type === 'BOOLEAN_OPERATION' && node.children.length) {
          nativeGeometryOwners.add(node.id);
          result.geometry_kind = 'native-boolean-subtree';
          result.svg_export_status = 'unavailable; exact operation and child geometry captured';
          delete result.geometry_asset_identifier;
        } else { failures.push({identifier:node.id,kind:'vector-export',reason:'native-vector-export-failed'}); }
      }
    }
  }
  const owner = vectorOwner || (node.type === 'BOOLEAN_OPERATION' ? node.id : null);
  if ('children' in node) result.children = await Promise.all(node.children.map(child => walk(child, owner)));
  return result;
}
const nodes = [];
const screenshots = [];
for (const target of captureTargets) {
  if (target.page_id !== page.id) throw new Error('Batch crosses pages');
  const node = await figma.getNodeByIdAsync(target.id);
  if (!node || node.type !== target.type || node.name !== target.name) throw new Error('Approved target identity drift');
  let owner = node;
  while (owner && owner.type !== 'PAGE') owner = owner.parent;
  if (!owner || owner.id !== target.page_id) throw new Error('Approved target page drift');
  const before = failures.length;
  const tree = await walk(node);
  if (target.needs_screenshot) screenshots.push(node);
  nodes.push({id:node.id,tree,screenshot_requested:!!target.needs_screenshot,
    failures:failures.slice(before)});
}
// The connector caps text at 20 KB. Lossless compression keeps exact floats,
// IDs and text; return an explicit size blocker rather than a truncated tree.
const raw = JSON.stringify({page_id:page.id,nodes,
  assets:Array.from(nativeAssets.values()).sort((a,b)=>a.identifier.localeCompare(b.identifier)),
  failures:failures.sort((a,b)=>a.identifier.localeCompare(b.identifier))});
const input = fflate.strToU8(raw);
const compressed=fflate.zlibSync(input,{level:9});
const encoded=figma.base64Encode(compressed);
const chunkIndex = typeof captureChunk === 'number' ? captureChunk : 0;
const chunkSize = 18500;
const chunkCount = Math.max(Math.ceil(encoded.length/chunkSize),screenshots.length);
if(chunkIndex<0 || chunkIndex>=chunkCount) throw new Error('Invalid capture chunk');
const screenshotNode = screenshots[chunkIndex];
if(screenshotNode) await screenshotNode.screenshot({scale:1,contentsOnly:true});
return {codec:'zlib-utf8-v1',uncompressed_bytes:input.length,
  encoded:encoded.slice(chunkIndex*chunkSize,(chunkIndex+1)*chunkSize),
  chunk_index:chunkIndex,chunk_count:chunkCount,total_encoded_characters:encoded.length,
  content_adler32:Array.from(compressed.slice(-4)),screenshot_node_id:screenshotNode?.id || null};
