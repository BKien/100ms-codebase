"""Prepare reviewed 100ms tables-only infrastructure from the exact schema snapshot."""
from pathlib import Path
from datetime import datetime,timezone
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'resource/specification-sources/100ms-2026-10-01-001/schema.dbml'
assert SOURCE.read_bytes()==Path('D:/figma_spec/100ms Video Conferencing and Live Streaming/schema.dbml').read_bytes()
text=SOURCE.read_text(encoding='utf8').replace('\r\n','\n')
# The lookup digest is deliberately NON-unique: collisions never imply key equality.
projection=text.replace("MySQL 8.0 persistence contract. Compile this schema, then apply persistence.sql.",
 "MySQL 8.4 repository-priority tables-only baseline. Do not execute persistence.sql. Aggregate capacity, membership identity and full-key replay are application MutationGateway responsibilities; see 100MS-DATABASE-ADAPTATION.md.")
projection=projection.replace('  idempotency_key text [not null]',
 "  idempotency_key text [not null]\n  idempotency_key_digest binary(32) [note: 'GENERATED ALWAYS AS (UNHEX(SHA2(CAST(idempotency_key AS BINARY), 256))) STORED; non-unique lookup only. Compare full key byte-exact under session lock.']")
projection=projection.replace('  indexes { (principal_id, session_id, operation, idempotency_key) [unique] }',
 "  indexes { (principal_id, session_id, operation, idempotency_key_digest) [name: 'idempotency_key_lookup'] }")
projection += '''
// Every table uses InnoDB, utf8mb4, utf8mb4_0900_bin and ROW_FORMAT=DYNAMIC.
// All FKs use ON DELETE RESTRICT ON UPDATE RESTRICT; nullable FKs remain nullable.
// MySQL enum columns use utf8mb4_bin for functional-index generated-column compatibility.
// Primary-key columns are NOT NULL. Defaults absent in source remain absent.
// Functional CASE indexes are exact source expressions and are not extra business fields.
// mutation_responses is written once by MutationGateway; response/receipt atomicity is application-enforced.
// SQL CHECK names/expressions installed by the initial migration:
TablePartial persistence_checks {
  ~checks_note varchar(1) [note: 'Documentation only; this TablePartial is never a live table.']
}
// participants: participant_display_name (display_name = TRIM(display_name) AND CHAR_LENGTH(display_name) BETWEEN 1 AND 50)
// chat_messages: message_body_shape (body = TRIM(body) AND CHAR_LENGTH(body) BETWEEN 1 AND 1000); message_sequence_positive (sequence > 0)
// reaction_events: reaction_sequence_positive (sequence > 0)
// content_shares: share_source_present (CHAR_LENGTH(TRIM(source_reference)) > 0)
// idempotency_records: idempotency_key_present (CHAR_LENGTH(TRIM(idempotency_key)) > 0); idempotency_expiry (expires_at = TIMESTAMPADD(HOUR,24,completed_at))
'''
# CHECK declarations are represented in DBML's named checks sections below.
projection=projection[:projection.index('TablePartial persistence_checks')]+projection[projection.index('// participants: participant_display_name'):]
checks={
 'participants':[('participant_display_name','display_name = TRIM(display_name) AND CHAR_LENGTH(display_name) BETWEEN 1 AND 50')],
 'chat_messages':[('message_body_shape','body = TRIM(body) AND CHAR_LENGTH(body) BETWEEN 1 AND 1000'),('message_sequence_positive','sequence > 0')],
 'reaction_events':[('reaction_sequence_positive','sequence > 0')],
 'content_shares':[('share_source_present','CHAR_LENGTH(TRIM(source_reference)) > 0')],
 'idempotency_records':[('idempotency_key_present','CHAR_LENGTH(TRIM(idempotency_key)) > 0'),('idempotency_expiry','expires_at = TIMESTAMPADD(HOUR, 24, completed_at)')],
}
# Keep runtime expressions documented even with DBML readers predating named CHECK blocks.
for table,items in checks.items():
 pattern=r'(Table '+table+r' \{)(.*?)(\n\})'
 def add_checks(m,items=items):
  block='\n  checks {\n'+''.join('    '+chr(96)+expr+chr(96)+" [name: '"+name+"']\n" for name,expr in items)+'  }\n'
  return m[1]+m[2]+block+m[3]
 projection=re.sub(pattern,add_checks,projection,flags=re.S)
enums={name:re.findall(r'^\s*([A-Z][A-Z_]*)\s*$',body,re.M) for name,body in re.findall(r'Enum (\w+) \{(.*?)\n\}',text,re.S)}
tables=re.findall(r'Table (\w+) \{(.*?)\n\}',text,re.S)
assert len(tables)==16
foreign=[]
statements=[]
index_names={
 'sessions':[['status','created_at']],
 'participants':[['session_id','status'],['session_id','user_id']],
 'stage_requests':[['session_id','participant_id','status']],
 'content_shares':[['session_id','status']],
 'recordings':[['session_id','status']],
 'departures':[['session_id','participant_id','created_at']],
}
unique_indexes={
 'participants': [('participants_session_identity',['session_id','id'])],
 'chat_messages':[('chat_messages_sequence',['session_id','sequence'])],
 'reaction_events':[('reaction_events_sequence',['session_id','sequence'])],
}
functional={
 'participants': [
 ('one_joined_membership',"(session_id, ((CASE WHEN status = 'JOINED' THEN principal_id ELSE NULL END)))"),
 ('one_joined_host',"(((CASE WHEN status = 'JOINED' AND role = 'HOST' THEN session_id ELSE NULL END)))")],
 'stage_requests':[('one_pending_stage_request',"(session_id, participant_id, ((CASE WHEN status = 'PENDING' THEN 1 ELSE NULL END)))")],
 'content_shares':[('one_active_share',"(((CASE WHEN status = 'ACTIVE' THEN session_id ELSE NULL END)))")],
 'recordings':[('one_active_recording',"(((CASE WHEN status IN ('STARTING', 'RECORDING') THEN session_id ELSE NULL END)))")],
}
for table,body in tables:
 definitions=[]
 for line in body.splitlines():
  m=re.fullmatch(r'\s+(\w+)\s+([a-z_]+(?:\(\d+\))?)\s*(?:\[(.*)\])?\s*',line)
  if not m:continue
  column,kind,flags=m.groups();flags=flags or ''
  if kind in enums:
   sqltype='ENUM('+','.join("'"+v+"'" for v in enums[kind])+')'
  elif kind=='boolean':sqltype='BOOLEAN'
  else:sqltype=kind.upper()
  if kind in enums:sqltype+=' CHARACTER SET utf8mb4 COLLATE utf8mb4_bin'
  nullable='NOT NULL' if 'not null' in flags or 'pk' in flags else 'NULL'
  definition='  '+chr(96)+column+chr(96)+' '+sqltype+' '+nullable
  if 'default:' in flags:
   default=re.search(r'default:\s*('+chr(96)+'.*?'+chr(96)+r"|'.*?'|true|false|\d+)",flags)[1]
   default=default.strip(chr(96))
   definition+=' DEFAULT '+{'true':'TRUE','false':'FALSE'}.get(default,default)
  if 'pk' in flags:definition+=' PRIMARY KEY'
  if 'unique' in flags:definition+=' UNIQUE'
  definitions.append(definition)
  ref=re.search(r'ref:\s*>\s*(\w+)\.(\w+)',flags)
  if ref:foreign.append((table+'_'+column+'_fk',table,[column],ref[1],[ref[2]]))
  check=re.search(r'check:\s*'+chr(96)+'(.*?)'+chr(96),flags)
  if check:definitions.append('  CONSTRAINT '+chr(96)+table+'_'+column+'_positive'+chr(96)+' CHECK ('+check[1]+')')
 for columns in index_names.get(table,[]):
  definitions.append('  INDEX '+chr(96)+table+'_'+'_'.join(columns)+'_idx'+chr(96)+' ('+', '.join(chr(96)+c+chr(96) for c in columns)+')')
 for name,columns in unique_indexes.get(table,[]):
  definitions.append('  UNIQUE INDEX '+chr(96)+name+chr(96)+' ('+', '.join(chr(96)+c+chr(96) for c in columns)+')')
 for name,expression in functional.get(table,[]):
  definitions.append('  UNIQUE INDEX '+chr(96)+name+chr(96)+' '+expression)
 if table=='idempotency_records':
  at=next(i for i,d in enumerate(definitions) if d.startswith('  '+chr(96)+'idempotency_key'+chr(96)))+1
  definitions.insert(at,'  '+chr(96)+'idempotency_key_digest'+chr(96)+' BINARY(32) GENERATED ALWAYS AS (UNHEX(SHA2(CAST(idempotency_key AS BINARY), 256))) STORED')
  definitions.append('  INDEX '+chr(96)+'idempotency_key_lookup'+chr(96)+' (principal_id, session_id, operation, idempotency_key_digest)')
 for name,expression in checks.get(table,[]):
  definitions.append('  CONSTRAINT '+chr(96)+name+chr(96)+' CHECK ('+expression+')')
 assert definitions and any('PRIMARY KEY' in d for d in definitions),table
 statements.append('CREATE TABLE '+chr(96)+table+chr(96)+' (\n'+',\n'.join(definitions)+'\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC')
for name,child,child_fields,parent,parent_fields in re.findall(r'Ref (\w+): (\w+)\.\(([^)]+)\) > (\w+)\.\(([^)]+)\)',text):
 foreign.append((name,child,[s.strip() for s in child_fields.split(',')],parent,[s.strip() for s in parent_fields.split(',')]))
assert len(foreign)==28,len(foreign)
for name,child,fields,parent,target_fields in foreign:
 statements.append('ALTER TABLE '+chr(96)+child+chr(96)+' ADD CONSTRAINT '+chr(96)+name+chr(96)+' FOREIGN KEY ('+', '.join(chr(96)+c+chr(96) for c in fields)+') REFERENCES '+chr(96)+parent+chr(96)+' ('+', '.join(chr(96)+c+chr(96) for c in target_fields)+') ON DELETE RESTRICT ON UPDATE RESTRICT')
stamp=str(int(datetime.now(timezone.utc).timestamp()*1000))
label='Initial100msSchema'
folder=ROOT/'finalsource/be/src/database/migrations'
folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.ts')),'Never overwrite a prepared/applied migration'
migration=folder/(stamp+'-'+label+'.ts')
# Use explicit SQL literals in the saved TypeORM migration; no DBML compiler at runtime.
def literal(sql):
 return chr(96)+sql.replace(chr(96),'\\'+chr(96))+chr(96)
source="import { MigrationInterface, QueryRunner } from 'typeorm';\n\n"
source+="// Researcher-authorized setup. MySQL 8.4, mysql84-tables-v1; source snapshot remains immutable.\n"
source+="// Digest lookup is NON-unique. MutationGateway must lock session and compare the complete key.\n"
source+='export class '+label+stamp+' implements MigrationInterface {\n'
source+='  public async up(queryRunner: QueryRunner): Promise<void> {\n'
source+="    await queryRunner.query(\"SET SESSION time_zone = '+00:00'\");\n"
for sql in statements:source+='    await queryRunner.query('+literal(sql)+');\n'
source+='  }\n\n  // Destructive rollback: execute only on an explicit researcher request outside a run.\n'
source+='  public async down(queryRunner: QueryRunner): Promise<void> {\n'
for name in ['session_host','sessions_spotlighted_participant_scope']:
 source+='    await queryRunner.query('+literal('ALTER TABLE '+chr(96)+'sessions'+chr(96)+' DROP FOREIGN KEY '+chr(96)+name+chr(96))+');\n'
for table,_ in reversed(tables):
 source+='    await queryRunner.query('+literal('DROP TABLE '+chr(96)+table+chr(96))+');\n'
source+='  }\n}\n'
migration.write_text(source,encoding='utf8',newline='\n')
active=ROOT/'docs/00-context/engineering/schema.dbml'
assert not active.exists(),'Do not replace an existing active schema'
active.write_text(projection,encoding='utf8',newline='\n')
receipt={
 'schema':'100ms-repository-priority-database-adaptation-v1','prepared_at':datetime.now(timezone.utc).isoformat(),
 'authorization':'Researcher request 2026-10-02: prioritize repository database requirements; author migrations from supplied 100ms schema; perform setup per Google Docs Database tab.',
 'source_schema':str(SOURCE.relative_to(ROOT)).replace('\\','/'),
 'source_schema_sha256':'sha256:'+hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'source_supplement':'resource/specification-sources/100ms-2026-10-01-001/persistence.sql',
 'source_supplement_sha256':'sha256:'+hashlib.sha256((SOURCE.parent/'persistence.sql').read_bytes()).hexdigest(),
 'active_dbml':'docs/00-context/engineering/schema.dbml','active_dbml_sha256':'sha256:'+hashlib.sha256(active.read_bytes()).hexdigest(),
 'migration_path':migration.relative_to(ROOT).as_posix(),'migration_head':label+stamp,
 'migration_sha256':'sha256:'+hashlib.sha256(migration.read_bytes()).hexdigest(),
 'tables':[t for t,_ in tables],'foreign_key_count':len(foreign),
 'decisions':{'mysql':'8.4','fingerprint':'mysql84-tables-v1 unchanged','executable_schema_objects':'none',
 'capacity_identity_and_atomic_replay':'application MutationGateway; not implemented by this setup',
 'idempotency_storage':'TEXT retained; stored SHA-256 digest non-unique index; full byte-exact key equality under SERIALIZABLE/session lock',
 'api_business_semantics':'unchanged; no key limit added','foreign_key_actions':'RESTRICT/RESTRICT explicit',
 'database_records':'no seed/reset/data deletion'},
 'runtime_status':'not-applied'}
out=ROOT/'docs/00-context/sources/100ms-database-adaptation.json'
out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'migration_path':receipt['migration_path'],'migration_head':receipt['migration_head'],'tables':len(tables),'foreign_keys':len(foreign),'dbml_sha256':receipt['active_dbml_sha256']}))
