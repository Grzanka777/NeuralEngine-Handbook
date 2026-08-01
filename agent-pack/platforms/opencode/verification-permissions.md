# OpenCode Verification Permissions

This document defines the minimum read-only command set required for the
OpenCode Quick Verification skill. It does **not** modify active permissions
in `~/.config/opencode/`. Future permission updates for a dedicated verifier
or reviewer must be reviewed separately.

## Required read-only commands

The following commands are required for Quick Verification:

| Command | Purpose |
|---|---|
| `find` | File presence, artifact detection |
| `test` | Path existence checks |
| `wc` | File and line counting |
| `sha256sum` | Exact-copy equality verification |
| `diff` | Byte comparison |
| `cmp` | Byte comparison (alternative) |
| `grep` | Text search, placeholder and mandatory-rule detection |
| `sed` (without `-i`) | YAML frontmatter stripping for body comparison |
| `git status` | Working-tree scope audit |
| `git diff` | Scope audit |
| `git rev-parse` | Git HEAD identification |
| `git ls-files` | File listing |
| `neural status` | NeuralEngine availability check |
| `neural search` | Optional (only if prior knowledge is relevant) |

## Currently allowed commands (OpenCode `arch-data-engineer`)

The `arch-data-engineer` agent has unrestricted bash access. All commands
listed above are implicitly allowed.

The `reviewer` agent has an explicit allowlist. The following commands from
the required set are **currently allowed** for the reviewer:

| Command | Reviewer status |
|---|---|
| `neural status` | Allowed |
| `neural search` | Allowed |
| `git status` | Allowed |
| `git diff` | Allowed |
| `git rev-parse` | Allowed |
| `git ls-files` | Allowed |
| `find` | **Would trigger `ask`** |
| `test` | **Would trigger `ask`** |
| `wc` | **Would trigger `ask`** |
| `sha256sum` | **Would trigger `ask`** |
| `diff` | **Would trigger `ask`** |
| `cmp` | **Would trigger `ask`** |
| `grep` | Tool `grep` is available but bash `grep` would trigger `ask` |
| `sed` | **Would trigger `ask`** |

Seven of the 14 required commands would trigger `ask` for the reviewer agent.
The reviewer cannot run Quick Verification without manual approval for these
commands.

## Commands that must remain denied

These commands must **never** be allowed for a verification skill, regardless
of the agent:

| Command | Reason |
|---|---|
| `rm *` | Destructive |
| `mv *` | Mutates filesystem |
| `cp *` | Could overwrite platform files |
| `sed -i*` | Mutates files |
| `git add*` | Staging mutation |
| `git commit*` | Repository mutation |
| `git push*` | Remote mutation |
| `git reset*` | Repository mutation |
| `git restore*` | Could discard changes |
| `git checkout*` | Branch mutation |
| `git switch*` | Branch mutation |
| `uv run ruff check --fix*` | Auto-fix mutation |
| `uv run ruff format*` | Format mutation |

## Explicit prohibition

The following pattern must **never** be allowed:

```text
bash "*": allow
```

Unrestricted bash access defeats the purpose of a permission model for
verification. Verification must remain read-only by permission design, not
just by convention.

## Recommended future permission additions

For a dedicated verifier agent or an updated reviewer, the following
permission additions are recommended:

```yaml
bash:
  "find *": allow
  "test *": allow
  "wc *": allow
  "sha256sum *": allow
  "diff *": allow
  "cmp *": allow
  "grep *": allow
  "sed *": allow           # Without -i only; sed -i* remains denied
```

These additions would enable the reviewer (or a future verifier agent) to run
Quick Verification without manual approval for each command.

## Current OpenCode verification skill permissions

The verification skill itself does not define an agent permission model. It
runs under the active agent's permissions. For `arch-data-engineer`, all
commands are available. For `reviewer`, manual approval is needed for seven
commands.

A dedicated verifier agent is not created in this task. The permission
additions above are a recommendation for a future update.
