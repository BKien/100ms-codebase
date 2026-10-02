"""Read-only correspondence validation for the selected 100ms setup baseline."""
import hashlib,json,re,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.codex/skills/gen-coding-prompt/scripts'))
import database_baseline as db

def sha(path):
    return 'sha256:'+hashlib.sha256(path.read_bytes()).hexdigest()

def model(text):
    enums={n:re.findall(r'^\s*([A-Z][A-Z_]*)\s*$',body,re.M) for n,body in re.findall(r'Enum (\w+) \{(.*?)\n\}',text,re.S)}
    result={}
    for table,body in re.findall(r'Table (\w+) \{(.*?)\n\}',text,re.S):
        columns=[]
        for line in body.splitlines():
            m=re.fullmatch(r'\s+(\w+)\s+([a-z_]+(?:\(\d+\))?)\s*(?:\[(.*)\])?\s*',line)
            if not m:continue
            name,kind,flags=m.groups();flags=flags or ''
            expected="enum("+','.join("'"+e+"'" for e in enums[kind])+")" if kind in enums else {'boolean':'tinyint(1)'}.get(kind,kind)
            default=re.search(r'default:\s*('+chr(96)+'.*?'+chr(96)+r"|'.*?'|true|false|\d+)",flags)
            value=default[1].strip(chr(96)).strip("'") if default else None
            value={'true':'1','false':'0'}.get(value,value)
            columns.append({'name':name,'type':expected,'nullable':'NO' if 'not null' in flags or 'pk' in flags else 'YES','default':value,'primary':'pk' in flags,'enum':kind in enums})
        result[table]=columns
    return result

def canonical_default(value):
    return None if value is None else str(value).lower().replace('()','')

def validate():
    preparation=json.loads((ROOT/'docs/00-context/sources/100ms-database-adaptation.json').read_text(encoding='utf8'))
    source=ROOT/preparation['source_schema']
    active=ROOT/'docs/00-context/engineering/schema.dbml'
    migration=ROOT/preparation['migration_path']
    assert sha(source)==preparation['source_schema_sha256']
    assert sha(active)==preparation['active_dbml_sha256']
    assert sha(migration)==preparation['migration_sha256'],'Applied migration bytes changed'
    source_model=model(source.read_text(encoding='utf8').replace('\r\n','\n'))
    active_model=model(active.read_text(encoding='utf8'))
    assert set(source_model)==set(active_model)==set(preparation['tables'])
    for table,columns in source_model.items():
        projected=[c for c in active_model[table] if c['name']!='idempotency_key_digest']
        assert projected==columns,table+': source column changed'
    runtime=db.Runtime()
    rows=runtime.query(db.metadata_sql())
    assert set(r[1] for r in rows if r[0]=='table')==set(active_model)|{'typeorm_migrations'}
    for table,columns in active_model.items():
        actual=sorted([r for r in rows if r[0]=='column' and r[1]==table],key=lambda r:r[3])
        assert len(actual)==len(columns),table+': column count'
        for expected,observed in zip(columns,actual):
            assert (observed[2],observed[4],observed[5])==(expected['name'],expected['type'],expected['nullable']),table+': column shape'
            assert canonical_default(observed[6])==canonical_default(expected['default']),table+': default'
            if expected['enum']:
                assert observed[9]=='utf8mb4_bin', table+': enum collation'
        expected_pk=[c['name'] for c in columns if c['primary']]
        actual_pk=[r[3] for r in sorted([r for r in rows if r[0]=='key' and r[1]==table and r[2]=='PRIMARY'],key=lambda r:r[4])]
        assert actual_pk==expected_pk,table+': primary key'
    foreign={}
    text=source.read_text(encoding='utf8').replace('\r\n','\n')
    for table,body in re.findall(r'Table (\w+) \{(.*?)\n\}',text,re.S):
        for field,parent,parent_field in re.findall(r'^\s+(\w+)\s+\S+\s+\[[^\n]*ref:\s*>\s*(\w+)\.(\w+)',body,re.M):
            foreign[table+'_'+field+'_fk']=(table,[field],parent,[parent_field])
    for name,child,fields,parent,parent_fields in re.findall(r'Ref (\w+): (\w+)\.\(([^)]+)\) > (\w+)\.\(([^)]+)\)',text):
        foreign[name]=(child,[s.strip() for s in fields.split(',')],parent,[s.strip() for s in parent_fields.split(',')])
    actual_foreign=[r for r in rows if r[0]=='foreign_key']
    assert len(actual_foreign)==len(foreign)==28
    for fk in actual_foreign:
        expected=foreign[fk[2]]
        keys=sorted([r for r in rows if r[0]=='key' and r[2]==fk[2]],key=lambda r:r[4])
        assert (fk[1],[r[3] for r in keys],fk[8],[r[8] for r in keys])==expected
        assert fk[6:8]==['RESTRICT','RESTRICT']
    check_names={r[1] for r in rows if r[0]=='check'}
    assert check_names=={
        'sessions_version_positive','participants_version_positive','live_streams_version_positive',
        'stage_requests_version_positive','content_shares_version_positive','recordings_version_positive',
        'participant_display_name','message_body_shape','message_sequence_positive','reaction_sequence_positive',
        'share_source_present','idempotency_key_present','idempotency_expiry'}
    index_names={r[2] for r in rows if r[0]=='index' and r[-1]}
    assert index_names=={'one_joined_membership','one_joined_host','one_pending_stage_request','one_active_share','one_active_recording'}
    digest_indexes=[r for r in rows if r[0]=='index' and r[1]=='idempotency_records' and r[2]=='idempotency_key_lookup']
    assert [r[5] for r in sorted(digest_indexes,key=lambda r:r[4])]==['principal_id','session_id','operation','idempotency_key_digest']
    assert all(r[3]==1 and r[7] is None for r in digest_indexes),'Digest must be non-unique and not prefix-indexed'
    digest=next(r for r in rows if r[0]=='column' and r[1]=='idempotency_records' and r[2]=='idempotency_key_digest')
    assert digest[7]=='STORED GENERATED' and 'sha2' in digest[10] and ',256)' in digest[10]
    # Existing capture verifies complete history, unsupported-object policy and actual emptiness.
    head,fingerprint=db.capture(require_empty=True,expected_head=preparation['migration_head'])
    assert fingerprint==db.fingerprint(rows)
    baseline={'migration_head':head,'dbml_sha256':sha(active),'schema_fingerprint_sha256':fingerprint}
    db.validate_input({'database_baseline':baseline})
    receipt={
        'artifact_type':'researcher-prepared-database-baseline','prepared_at':datetime.now(timezone.utc).isoformat(),
        'source_adaptation_path':'docs/00-context/sources/100ms-database-adaptation.json',
        'database_baseline':baseline,'fingerprint_protocol':db.PROTOCOL,
        'validation':{'status':'PASS','mysql_version':next(r[1] for r in rows if r[0]=='server'),
            'application_tables':16,'migration_history_records':1,'foreign_keys':28,'checks':13,
            'conditional_unique_indexes':5,'source_column_inventory_preserved':True,
            'dbml_runtime_columns_defaults_nullability_pk_fk_correspondence':True,
            'unsupported_schema_objects':0,'application_tables_empty':True,
            'idempotency_digest_index_non_unique':True,'sync_and_automatic_migrations_disabled':True},
        'boundaries':'Setup only; no UC business implementation, BR audit, seeds, reset, tests, experiment configuration or run creation.'}
    path=ROOT/'docs/00-context/sources/100ms-database-baseline.json'
    path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=='__main__':
    validate()
