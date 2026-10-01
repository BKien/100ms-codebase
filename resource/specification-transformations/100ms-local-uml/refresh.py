"""Project the supplied UML onto each UC's unchanged OCL vocabulary.

This is a bounded transformer for the supplied 100ms OCL syntax, not an OCL
evaluator. Unknown navigation fails closed. No application or DB changes.
"""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD_RECEIPT = ROOT / 'docs/00-context/sources/100ms-source-retrieval.json'
NEW_RECEIPT = ROOT / 'docs/00-context/sources/100ms-local-uml-retrieval.json'
ARCHIVE = ROOT / 'resource/specification-transformations/100ms-local-uml/before'
UC_DIR = ROOT / 'docs/01-inception/use-cases'
TYPE = r'\w+(?:\(\w+\))?'
PRIMITIVES = {'String', 'Boolean', 'Integer', 'Real'}
TOKEN = re.compile(r"'[^']*'|@pre|::|->|\w+|[^\s]")
HELPER_DEPENDENCIES = {
    'Paging.latestRecording': [('Recording', 'id'), ('Recording', 'createdAt'), ('Recording', 'sessionId')],
    'Paging.participants': [('Participant', 'id'), ('Participant', 'joinedAt'), ('Participant', 'sessionId'), ('ParticipantPage', 'nextCursor')],
    'Paging.messages': [('ChatMessage', 'sequence'), ('ChatMessage', 'sessionId'), ('MessagePage', 'nextCursor')],
    'Paging.reactions': [('ReactionEvent', 'sequence'), ('ReactionEvent', 'sessionId')],
}


def sha(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def classifiers(text):
    result = {}
    for kind, name, body in re.findall(r'(class|enum) (\w+) \{\n(.*?)\n\}', text, re.S):
        members = {}
        for line in body.splitlines():
            line = line.strip()
            member = re.match(r'(?:\{static\} )?(\w+)', line).group(1)
            members[member] = line
        result[name] = (kind, members)
    return result


def result_type(line):
    return re.search(r':\s*(' + TYPE + r')\s*$', line).group(1)


def element(typ):
    match = re.fullmatch(r'(?:Set|Sequence|Bag|OrderedSet)\((\w+)\)', typ)
    return match.group(1) if match else typ


class Vocabulary:
    def __init__(self, model):
        self.model = model
        self.used = defaultdict(set)
        self.reasons = defaultdict(set)
        self.rule = None
        self.extents = set()

    def type(self, typ):
        name = element(typ)
        if name in self.model:
            self.used[name]
            self.reasons[name].add(self.rule)
        elif name not in PRIMITIVES:
            raise ValueError(f'{self.rule}: unknown type {name}')

    def member(self, owner, name):
        owner = element(owner)
        self.type(owner)
        kind, members = self.model[owner]
        if name not in members:
            raise ValueError(f'{self.rule}: unknown member {owner}.{name}')
        self.used[owner].add(name)
        self.reasons[f'{owner}.{name}'].add(self.rule)
        if kind == 'enum':
            return owner
        line = members[name]
        typ = result_type(line)
        self.type(typ)
        if '(' in line.split(':', 1)[0]:
            for param_type in re.findall(r':\s*(' + TYPE + ')', line):
                self.type(param_type)
        for dependency_owner, dependency_member in HELPER_DEPENDENCIES.get(f'{owner}.{name}', []):
            self.member(dependency_owner, dependency_member)
        return typ

    def scan(self, tokens, env, implicit=None):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '(':
                end = self.close(tokens, i)
                self.scan(tokens[i + 1:end], env, implicit)
                i = end + 1
                continue
            if token in env or token in self.model:
                typ = env.get(token, token)
                self.type(typ)
                i += 1
                while i < len(tokens):
                    if tokens[i] == '@pre':
                        i += 1
                        continue
                    if tokens[i] not in {'.', '::', '->'}:
                        break
                    separator, name = tokens[i:i + 2]
                    i += 2
                    receiver = typ
                    if name == 'allInstances':
                        self.extents.add(element(typ))
                        typ = f'Set({element(typ)})'
                    elif name in {'select', 'reject', 'including', 'excluding', 'asSequence', 'asSet'}:
                        pass
                    elif name in {'any', 'first', 'last', 'at'}:
                        typ = element(typ)
                    elif name in {'size'}:
                        typ = 'Integer'
                    elif name in {'exists', 'one', 'forAll', 'isUnique', 'notEmpty', 'isEmpty', 'oclIsNew', 'oclIsUndefined'}:
                        typ = 'Boolean'
                    else:
                        typ = self.member(receiver, name)
                    if i < len(tokens) and tokens[i] == '@pre':
                        i += 1
                    if i < len(tokens) and tokens[i] == '(':
                        end = self.close(tokens, i)
                        args = tokens[i + 1:end]
                        nested = dict(env)
                        if '|' in args and args.index('|') <= 3:
                            pipe = args.index('|')
                            nested[args[0]] = element(receiver)
                            args = args[pipe + 1:]
                        self.scan(args, nested, element(receiver) if separator == '->' else None)
                        i = end + 1
                continue
            if re.fullmatch(r'\w+', token) and implicit in self.model:
                if token in self.model[implicit][1]:
                    self.member(implicit, token)
            i += 1

    @staticmethod
    def close(tokens, start):
        depth = 0
        for i in range(start, len(tokens)):
            depth += (tokens[i] == '(') - (tokens[i] == ')')
            if depth == 0:
                return i
        raise ValueError('Unbalanced OCL parentheses')

    def rule_block(self, block):
        self.rule = re.search(r'-- (BR-UC-\d+-\d+)', block).group(1)
        clean = re.sub(r'--[^\n]*', '', block)
        context = re.search(r'context (\w+)(?:::(\w+)\((.*?)\):\s*(' + TYPE + r'))?\n', clean)
        owner, operation, params, returns = context.groups()
        env = {'self': owner}
        self.type(owner)
        if operation:
            self.member(owner, operation)
            env['result'] = returns
            env.update(re.findall(r'(\w+):\s*(' + TYPE + ')', params))
        body = clean[context.end():]
        for var, typ in re.findall(r'let (\w+)\s*:\s*(' + TYPE + ')', body):
            env[var] = typ
            self.type(typ)
        self.scan(TOKEN.findall(body), env)

    def render(self, utility_text):
        lines = ['```plantuml', '@startuml', 'hide empty members']
        for name, (kind, members) in self.model.items():
            if name not in self.used:
                continue
            selected = list(members) if kind == 'enum' else [m for m in members if m in self.used[name]]
            # Full enum domains preserve type semantics, including unconstrained values.
            if not selected and name in self.extents:
                lines.extend([f'class {name} <<extent>> {{', f'  {{static}} allInstances(): Set({name})', '}'])
            elif not selected:
                stereotype = 'datatype' if name == 'DateTime' or name in PRIMITIVES else 'opaque'
                lines.extend([f'class {name} <<{stereotype}>> {{', '}'])
                lines.append(f'note right of {name}: Used only as a type; no structural member is accessed by these BRs.')
            else:
                lines.append(f'{kind} {name} {{')
                lines.extend('  ' + members[m] for m in selected)
                lines.append('}')
        if any(not self.used[name] for name in self.extents):
            lines.extend(['note "allInstances() is the standard OCL classifier extent.\\nAn extent-only classifier has no structural properties in this UC projection." as ExtentSemantics'])
        for owner in self.used:
            for name in sorted(self.used[owner]):
                key = f'{owner}{"." if owner == "String" else "::"}{name}'
                match = re.search(r'^' + re.escape(key) + r'\([^\n]*\n((?:- [^\n]*\n)+)', utility_text, re.M)
                if match:
                    lines.extend([f'note right of {owner}', *[s[2:] for s in match.group(1).splitlines()], 'end note'])
        if 'RequestContext' in self.used:
            lines.extend(['note right of RequestContext', 'Request-local trusted adapter data; not a process-global singleton.', 'Principal and session are decoded from the authenticated session access token.'])
            if 'participantId' in self.used['RequestContext']:
                lines.append("participantId resolves the principal's membership.")
            if 'providerAuthenticated' in self.used['RequestContext']:
                lines.append('Provider callbacks use a separate authenticated adapter.')
            lines.append('end note')
        if 'TransactionContext' in self.used:
            lines.append('note right of TransactionContext: Describes the database transaction for the current operation.')
        lines.extend(['@enduml', '```'])
        return '\n'.join(lines) + '\n\n'


def prepare(receipt):
    utility = (UC_DIR / 'OCL-UTILITY-DEFINITIONS.md').read_text(encoding='utf-8')
    changes = []
    for entry in receipt['projections']:
        if not re.fullmatch(r'docs/01-inception/use-cases/uc-\d+-.+\.md', entry['projection_path']):
            continue
        path = ROOT / entry['projection_path']
        archive = ARCHIVE / path.name
        before = (archive if archive.exists() else path).read_bytes()
        assert sha(before) == entry['projection_sha256'], f'Projection drift: {path}'
        snapshot = (ROOT / entry['source_snapshot_path']).read_bytes()
        assert sha(snapshot) == entry['source_sha256'], f'Source drift: {path}'
        text = before.decode('utf-8').replace('\r\n', '\n')
        start, end = text.index('## UML Model\n'), text.index('## Business Rules\n')
        model = classifiers(text[start:end])
        vocab = Vocabulary(model)
        blocks = re.findall(r'(?:~~~|```)ocl\n(.*?)(?:~~~|```)', text[end:], re.S)
        for block in blocks:
            vocab.rule_block(block)
        uml = '## UML Model\n\nLocal projection of exactly the vocabulary needed by the Business Rules below, including signature and helper types. Enum domains are retained in full to preserve their value semantics.\n\n' + vocab.render(utility)
        after = text[:start] + uml + text[end:]
        after = after.replace('retrieved_at: ', 'uml_projection_contract: br-local-uml-v1\numl_projection_receipt: docs/00-context/sources/100ms-local-uml-retrieval.json\nretrieved_at: ', 1)
        changes.append((entry, before, after.encode('utf-8'), vocab, len(blocks)))
    assert len(changes) == 18
    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    receipt = json.loads(OLD_RECEIPT.read_text(encoding='utf-8-sig'))
    changes = prepare(receipt)
    for entry, before, after, vocab, count in changes:
        print(f"{Path(entry['projection_path']).stem}: {len(vocab.used)} classifiers, {sum(len(v) for v in vocab.used.values())} used members, {count} BRs")
    if args.verify:
        current = json.loads(NEW_RECEIPT.read_text(encoding='utf-8'))
        for entry in current['projections']:
            assert sha((ROOT / entry['projection_path']).read_bytes()) == entry['projection_sha256']
            assert sha((ROOT / entry['source_snapshot_path']).read_bytes()) == entry['source_sha256']
        for entry, before, after, vocab, count in changes:
            assert (ROOT / entry['projection_path']).read_bytes() == after
            previous = before.decode('utf-8').replace('\r\n', '\n')
            actual = after.decode('utf-8')
            assert previous[previous.index('## Business Rules\n'):] == actual[actual.index('## Business Rules\n'):]
            assert previous[previous.index('# UC-'):previous.index('## UML Model\n')] == actual[actual.index('# UC-'):actual.index('## UML Model\n')]
            assert len(re.findall(r'^```plantuml$', actual, re.M)) == 1
            assert 'shared-domain-model' not in actual
        assert not (UC_DIR / 'shared-domain-model.md').exists()
        print('PASS: all 18 local UML projections, unchanged BR/functional text, source/projection hashes, and no active shared model.')
        return
    if not args.write:
        return
    if NEW_RECEIPT.exists():
        current = json.loads(NEW_RECEIPT.read_text(encoding='utf-8'))
        for entry in current['projections']:
            assert sha((ROOT / entry['projection_path']).read_bytes()) == entry['projection_sha256'], 'Active projection changed after refresh'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    refreshed = dict(receipt)
    refreshed['artifact_type'] = '100ms-source-retrieval-local-uml-refresh'
    refreshed['refresh_at'] = now
    refreshed['refresh_source'] = 'checksum-verified existing source snapshot; no new external retrieval'
    refreshed['previous_receipt_path'] = OLD_RECEIPT.relative_to(ROOT).as_posix()
    refreshed['previous_receipt_sha256'] = sha(OLD_RECEIPT.read_bytes())
    refreshed['researcher_instruction'] = 'Each UC UML contains only vocabulary needed by its own BRs; no shared model.'
    refreshed['uml_projection_contract'] = 'br-local-uml-v1'
    refreshed['helper_member_dependencies'] = HELPER_DEPENDENCIES
    refreshed['projections'] = [dict(e) for e in receipt['projections'] if not e['projection_path'].endswith('/shared-domain-model.md')]
    refreshed['uml_changes'] = []
    for entry, before, after, vocab, count in changes:
        path = ROOT / entry['projection_path']
        backup = ARCHIVE / path.name
        if not backup.exists():
            backup.write_bytes(before)
        assert backup.read_bytes() == before
        path.write_bytes(after)
        updated = next(e for e in refreshed['projections'] if e['projection_path'] == entry['projection_path'])
        updated['projection_sha256'] = sha(after)
        updated['transformations'] = [t for t in entry['transformations'] if t != 'inline supplied shared UML vocabulary'] + ['researcher-authorized BR-local UML projection; unchanged BRs and functional specification']
        refreshed['uml_changes'].append({'path': entry['projection_path'], 'previous_projection_sha256': sha(before), 'previous_projection_archive': backup.relative_to(ROOT).as_posix(), 'rule_count': count, 'classifiers': list(vocab.used), 'member_rule_references': {k: sorted(v) for k, v in sorted(vocab.reasons.items())}})
    shared = UC_DIR / 'shared-domain-model.md'
    shared_entry = next(e for e in receipt['projections'] if e['projection_path'].endswith('/shared-domain-model.md'))
    backup = ARCHIVE / shared.name
    if shared.exists():
        assert sha(shared.read_bytes()) == shared_entry['projection_sha256']
        backup.write_bytes(shared.read_bytes())
        shared.unlink()
    assert sha(backup.read_bytes()) == shared_entry['projection_sha256']
    refreshed['retired_shared_model'] = {'previous_projection_path': shared_entry['projection_path'], 'archive_path': backup.relative_to(ROOT).as_posix(), 'sha256': shared_entry['projection_sha256'], 'status': 'historical evidence only; not an active UML dependency'}
    NEW_RECEIPT.write_text(json.dumps(refreshed, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
