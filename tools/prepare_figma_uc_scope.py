"""Pin a UC-focused capture request from the approved, already verified inventory."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = '100ms-2026-10-02-001'
DATASET = ROOT / 'resource/figma-design-dataset' / VERSION

# Explicit screen selection; IDs must already occur in FIGMA-LINK-REVIEW.md.
SELECTIONS = {
  1: '6007:51246 6007:51266 6007:51296 6007:51317 6066:89729 6066:89749 6066:89779 6066:89039 6066:89077',
  2: '6007:51341 6007:51391 6007:51418 6066:89824 6012:45669 6012:45686 6012:45783 6012:45757 6066:89024 6066:89065',
  3: '6007:51102 6007:87452 6007:87457 6007:87462 6007:87294 6012:46515 6012:91115 6012:91122',
  4: '6007:87446 6007:87130 6012:91129 6012:91109 6012:91122',
  5: '6007:51398 6007:87410 6007:87420 6007:87425 6012:45649 6012:45653 6012:90640 6012:90658',
  6: '6007:87261 6007:87266 6007:87286 6012:90852 6012:90856 6012:90844 6012:90865',
  7: '6007:87235 6007:87241 6007:87247 6007:87253 6012:90811 6012:90818 6012:90825 6012:90833',
  8: '6007:58204 6007:58211 6007:58218 6012:90873 6012:90881 6012:90905 6012:54087 6012:54095',
  9: '6007:58174 6007:58181 6007:58188 6012:90740 6012:90748 6012:90786 6012:54014 6012:54022 6012:54031',
  10: '6007:58047 6045:42131',
  11: '6007:58057 6007:58063 6007:58070 6007:87336 6007:87343 6007:77993 6012:53876 6012:53894 6012:78247',
  12: '6007:51133 6007:51161 6066:89800 6066:89053 6012:45822',
  13: '6026:1184330 6026:1184356',
  14: '6007:96237 6007:96344 6007:96540 6007:96324 6007:87353 6007:87359 6007:77668 6007:77774 6007:77874 6007:78001 6007:58080 6012:102743 6012:102748 6012:102826 6012:102840 6012:78025 6012:78092 6012:78247 6012:54129',
  15: '6007:57904 6007:57911 6007:58234 6073:21769 6012:78177 6012:78184 6012:53602 6012:53632',
  16: '6007:57964 6007:57969 6007:57974 6007:57979 6012:91155 6012:91161 6012:91171 6012:91177 6012:53842 6012:53847 6012:53856 6012:53861',
  17: '6007:58165 6007:58149 6007:58163 6007:87165 6007:87163 6012:91011 6012:91021 6066:112897 6012:54187',
  18: '6007:58149 6007:58165 6007:58147 6007:87132 6007:87130 6012:90959 6012:90969 6066:112577 6066:112591',
}


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    assert not (DATASET / 'FROZEN.json').exists()
    path = DATASET / 'capture-request.json'
    original_path = DATASET / 'superseded-full-file-capture-request.json'
    if not original_path.exists():
        original_path.write_bytes(path.read_bytes())
    original = json.loads(original_path.read_text(encoding='utf-8'))
    inventory = {n['id']:n for n in original['targets']}
    review_path = ROOT / 'docs/00-context/FIGMA-LINK-REVIEW.md'
    review = review_path.read_text(encoding='utf-8')
    approved = {a + ':' + b for a,b in re.findall(r'node-id=(\d+)-(\d+)', review)}
    coverage = {}
    for number, selected in SELECTIONS.items():
        source = next((ROOT / 'docs/01-inception/use-cases').glob(f'uc-{number:02d}-*.md'))
        text = source.read_text(encoding='utf-8')
        functional = text.split('## UML')[0]
        primary = original['primary_nodes'][number - 1]
        ids = list(dict.fromkeys([primary] + [i for i in selected.split()
            if 'Desktop' in inventory[i]['page_name'] or i in {'6045:42131','6073:21769'}]))
        assert all(i in inventory and i in approved for i in ids)
        flows = ['Basic Flow'] + re.findall(r'(?m)^(AF-\d+|EF-\d+):',functional)
        coverage[f'UC-{number:03d}'] = {
            'source_uc':source.relative_to(ROOT).as_posix(),
            'source_uc_sha256':'sha256:' + hashlib.sha256(source.read_bytes()).hexdigest(),
            'primary_node_id':primary,'required_node_ids':ids,
            'platforms':['desktop'],
            'excluded_platforms':['mobile'],
            'platform_scope_authorized_by':'Researcher explicitly requested desktop only; no mobile capture',
            'flow_inventory':flows,
            'flow_coverage':[
                {'flow_id':flow, 'evidence_node_ids':ids,
                 'coverage_kind':'captured-ui-and-spec-behavior',
                 'note': 'Frames provide exact UI/control/feedback styles. UC defines actions, cancellation, failure retention and server behavior; frame reuse does not prove runtime flow correctness.'}
                for flow in flows],
            'design_limitations':[
                'No dedicated Figma screen is asserted for every server/device failure, cancellation or receipt state. Implement behavior/message semantics from this frozen UC/API using the captured controls and feedback styles.',
                'Desktop only by researcher instruction; mobile UI references in the frozen UC are outside this dataset scope. This dataset does not establish mobile design readiness.',
                'Representative desktop peer-count layouts preserve selected modes; redundant count variants are outside mandatory capture.'
            ]}
    required = list(dict.fromkeys(i for uc in coverage.values() for i in uc['required_node_ids']))
    write(path, {'dataset_version':VERSION,'file_key':original['file_key'],
        'derived_from_dataset':'100ms-2026-10-01-001','scope':'desktop-uc-sufficient-v2',
        'platforms':['desktop'],'excluded_platforms':['mobile'],
        'scope_authorized_by':'Researcher instruction on 2026-10-02: quota-optimal UC capture; latest instruction explicitly desktop only, no mobile',
        'prepared_at':datetime.now(timezone.utc).isoformat(),'primary_nodes':original['primary_nodes'],
        'uc_files':original['uc_files'],'targets':[inventory[i] for i in required],
        'coverage_path':'uc-design-coverage.json','discovery_target_count':len(original['targets']),
        'excluded_target_count':len(original['targets']) - len(required),
        'excluded_categories':['mobile','documentation','changelogs','unused foundations/component libraries','redundant layout peer-count variants'],
        'supplementary_capture_method':'read-only native Plugin API; batches within one approved page'})
    write(DATASET / 'uc-design-coverage.json', {'schema':'uc-design-coverage-v1','dataset_version':VERSION,
        'coverage_type':'design-input-sufficiency; not BR/flow audit','use_cases':coverage})
    marker = '\n## Active UC-sufficient capture scope (2026-10-02)\n'
    review = review.split(marker)[0]
    review = review.replace('Full-file capture includes product pages, documentation, foundations, components and local assets.',
        'The historical full-file inventory is discovery evidence. The active scope below selects only UC-required product states and referenced components/assets.')
    review += marker + '\nResearcher authorized quota-optimal **desktop-only** capture for the frozen UC specifications and explicitly excluded mobile in the latest instruction. Required nodes are selected from the verified Replacement URLs already listed above; no UC provenance URL is used. Frozen UC mobile references remain unchanged as provenance, outside this dataset scope. Documentation, unused libraries and redundant peer counts are optional. Previously downloaded mobile evidence is retained only as superseded evidence and is not used by desktop resolution.\n\n'
    review += f'Exact version: `{VERSION}`. Required inventory and flow/platform coverage: [capture request](../../resource/figma-design-dataset/{VERSION}/capture-request.json), [coverage matrix](../../resource/figma-design-dataset/{VERSION}/uc-design-coverage.json).\n\n'
    review += '| UC | Primary | Required nodes (shared nodes captured once) |\n|---|---|---|\n'
    for uc, entry in coverage.items():
        review += f"| {uc} | `{entry['primary_node_id']}` | " + ', '.join('`' + i + '`' for i in entry['required_node_ids']) + ' |\n'
    review_path.write_text(review,encoding='utf-8',newline='\n')
    print(json.dumps({'version':VERSION,'required_nodes':len(required),'discovery_nodes':len(original['targets']),
                      'pages':len({inventory[i]['page_id'] for i in required}),'use_cases':len(coverage)}))


if __name__ == '__main__':
    main()
