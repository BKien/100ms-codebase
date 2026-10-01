// Run a copy beside the bundled node_modules junction, as described in SKILL.md.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const requireValue = (ok, message) => { if (!ok) throw new Error(message); };
const hash = data => 'sha256:' + crypto.createHash('sha256').update(data).digest('hex');
const json = async file => JSON.parse((await fs.readFile(file, 'utf8')).replace(/^\uFEFF/, ''));
const same = (a, b) => JSON.stringify(a ?? null) === JSON.stringify(b ?? null);
const args = process.argv.slice(2);
const mode = args.shift();
const options = {};
while (args.length) {
  const key = args.shift();
  requireValue(key?.startsWith('--') && args.length, 'Expected --option value');
  options[key.slice(2)] = args.shift();
}
requireValue(['inspect', 'fill'].includes(mode) && options['repo-root'], 'Use inspect|fill --repo-root <Business repo>');
const root = await fs.realpath(options['repo-root']);
const within = (parent, child) => { const rel = path.relative(parent, child); return !rel.startsWith('..') && !path.isAbsolute(rel); };
async function safeOutput(file) {
  const absolute = path.resolve(root, file);
  const relativeParts = path.relative(root, absolute).split(path.sep);
  requireValue(within(root, absolute) && !relativeParts[0]?.toLowerCase().endsWith('-master'), 'Output outside Business scope');
  // Resolve existing ancestors before mkdir to reject junction/symlink escapes.
  let ancestor = path.dirname(absolute);
  while (true) {
    try { ancestor = await fs.realpath(ancestor); break; }
    catch (e) { if (e.code !== 'ENOENT') throw e; ancestor = path.dirname(ancestor); }
  }
  const ancestorParts = path.relative(root, ancestor).split(path.sep);
  requireValue(within(root, ancestor) && !ancestorParts[0]?.toLowerCase().endsWith('-master'), 'Output parent escapes Business scope');
  await fs.mkdir(path.dirname(absolute), {recursive: true});
  return absolute;
}
const updates = mode === 'fill' ? await json(options.updates) : null;
if (updates) requireValue(await fs.realpath(updates.repo_root) === root && updates.schema_version === 1, 'Updates repository/schema mismatch');
const input = path.resolve(root, updates?.workbook ?? options.workbook ?? '');
requireValue(path.extname(input).toLowerCase() === '.xlsx', 'Only .xlsx is supported');
const raw = await fs.readFile(input);
if (updates) requireValue(hash(raw) === updates.workbook_sha256, 'Workbook changed since mapping');
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
if (mode === 'inspect') {
  const query = options.sheet
    ? {kind: 'region', sheetId: options.sheet, range: options.range ?? 'A1:Z30', maxChars: 12000, tableMaxRows: 30, tableMaxCols: 26}
    : {kind: 'workbook,sheet,table', maxChars: 8000, tableMaxRows: 6, tableMaxCols: 8};
  console.log((await workbook.inspect(query)).ndjson);
} else {
  requireValue(options.output, '--output is required');
  const output = await safeOutput(options.output);
  requireValue(output.toLowerCase() !== input.toLowerCase(), 'Save a new workbook; never overwrite the input');
  requireValue(path.extname(output).toLowerCase() === '.xlsx', 'Output must be .xlsx');
  const receiptPath = output + '.fill-report.json';
  // Reserve a new name; never silently overwrite a prior export/receipt.
  for (const name of [output, receiptPath]) {
    try { await fs.access(name); throw new Error('Output already exists: ' + name); }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
  }
  const seen = new Set();
  const regions = new Map();
  // Validate every target before the first workbook mutation.
  for (const cell of updates.updates) {
    const key = JSON.stringify([cell.sheet, cell.cell]);
    requireValue(!seen.has(key) && /^[A-Z]{1,3}[1-9][0-9]{0,6}$/.test(cell.cell), 'Duplicate/invalid target');
    seen.add(key);
    const sheet = workbook.worksheets.getItem(cell.sheet);
    const target = sheet.getRange(cell.cell);
    requireValue(!target.formulas?.[0]?.[0] && !target.displayFormulas?.[0]?.[0], 'Formula target must remain untouched: ' + key);
    requireValue(same(target.values?.[0]?.[0], cell.expected_value), 'Cell value changed: ' + key);
    requireValue(cell.overwrite_existing || cell.expected_value == null || cell.expected_value === '', 'Existing value requires explicit refresh: ' + key);
    requireValue(Array.isArray(cell.basis) && cell.basis.length, 'Missing mapping context: ' + key);
    for (const basis of cell.basis) requireValue(same(sheet.getRange(basis.cell).values?.[0]?.[0], basis.value), 'Mapping heading/identity changed: ' + key);
    requireValue(cell.value !== null && ['number', 'string', 'boolean'].includes(typeof cell.value), 'Only non-null scalar writes');
    requireValue(typeof cell.value !== 'number' || Number.isFinite(cell.value), 'Non-finite cell value');
    requireValue(!cell.reason || cell.value === 'N/A', 'Unavailable cell must be literal N/A');
    if (cell.source) requireValue(hash(await fs.readFile(cell.source)) === cell.source_sha256, 'Canonical result changed; regenerate updates');
    requireValue(typeof cell.review_range === 'string' && /^[A-Z]+[1-9][0-9]*:[A-Z]+[1-9][0-9]*$/.test(cell.review_range), 'Bounded review range required');
    regions.set(JSON.stringify([cell.sheet, cell.review_range]), {sheetName: cell.sheet, range: cell.review_range});
  }
  for (const cell of updates.updates) {
    const value = typeof cell.value === 'string' && cell.value.startsWith('=') ? "'" + cell.value : cell.value;
    workbook.worksheets.getItem(cell.sheet).getRange(cell.cell).values = [[value]];
  }
  workbook.recalculate();
  const checks = [];
  for (const region of regions.values()) {
    checks.push((await workbook.inspect({kind: 'region', sheetId: region.sheetName, range: region.range, maxChars: 6000})).ndjson);
  }
  const errors = (await workbook.inspect({kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: {useRegex: true, maxResults: 100}, maxChars: 8000})).ndjson;
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(output);
  const saved = await SpreadsheetFile.importXlsx(await FileBlob.load(output));
  for (const cell of updates.updates) {
    const actual = saved.worksheets.getItem(cell.sheet).getRange(cell.cell).values?.[0]?.[0];
    requireValue(same(actual, cell.value) || (typeof cell.value === 'string' && cell.value.startsWith('=') && actual === "'" + cell.value), 'Saved value mismatch');
  }
  const receipt = {...updates, output, output_sha256: hash(await fs.readFile(output)), checks, formula_error_scan: errors,
    verification: 'Mapped cells reimported and checked against planned values. Region inspection and formula-error scan retained; native-feature preservation requires separate data/structure checks.'};
  await fs.writeFile(receiptPath, JSON.stringify(receipt, null, 2) + '\n', {flag: 'wx'});
  console.log(JSON.stringify({output, receipt: receiptPath, filled_count: updates.filled_count, na_count: updates.na_count}, null, 2));
}
