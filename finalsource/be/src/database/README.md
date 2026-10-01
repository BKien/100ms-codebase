# Deferred database input

The researcher deferred database preparation on 2026-10-01. This baseline has no entities, migrations, active schema or database fingerprint. The main application does not open a database connection. The setup-only CLI keeps synchronization and automatic migrations disabled.

Before an experiment run, resolve the persistence.sql procedure/trigger policy, review a MySQL 8.4 migration and DBML, apply it in authorized setup and capture all three database pins. Never use the archived Financial schema.
