# Environment checks

Use only commands available for the detected OS. Record versions and status, not unrelated host details.

## Common checks

```bash
pwd
git status --short
git rev-parse --show-toplevel
uname -s
uname -m
docker --version
docker compose version
docker info
docker compose --env-file finalsource/.env -f finalsource/compose.yaml config --quiet
git check-ignore finalsource/.env
git ls-files --error-unmatch finalsource/.env
```

Run the Compose config command only when `finalsource/.env` exists. The final `git ls-files` command is expected to fail when the env file is safely untracked.

## Installation feasibility

- macOS: verify a supported macOS version, Apple Silicon/Intel architecture, virtualization availability, free disk and permission to install Docker Desktop. Starting Docker Desktop is a GUI action requiring approval.
- Windows: verify supported Windows edition/build, WSL 2 or Hyper-V capability and virtualization enabled. Prefer Docker Desktop with WSL 2 unless institutional policy requires another supported path.
- Linux: identify distribution/package manager, 64-bit architecture, kernel/cgroup support and permission for the official Docker Engine repository or Docker Desktop. Compose must be v2 (`docker compose`), not legacy `docker-compose`.
- Managed VM/container: report nested-virtualization or daemon/socket restrictions; do not attempt to bypass policy.

Never claim Docker can be installed solely because the OS name is supported. Report unknown prerequisites explicitly.
