# Agent Pack v0.3.0 Release Decision

## Decision

**RELEASE PREPARED — BLOCKED PENDING CERTIFICATION**

Agent Pack v0.3.0 is a permission-enforcement release. The release is prepared
but not yet published. Repository validation, Quick Verification, and Standard
Verification are complete. Release remains blocked until certification is
executed.

## Scope

v0.3.0 enforces Verification Framework permissions on the OpenCode reviewer
agent:

- Eight narrow read-only shell command permissions added to the reviewer:
  `find *`, `test *`, `wc *`, `sha256sum *`, `diff *`, `cmp *`, `grep *`,
  `sed *`.
- `verification` skill added to reviewer required skills.
- Quick Verification runs through the reviewer without permission prompts.
- All existing deny boundaries preserved.
- No dedicated verifier agent introduced.

### Rationale

Extending the existing reviewer was chosen over adding a dedicated verifier
agent because:

1. **Smallest coherent change.** Adding eight allow patterns to an existing
   agent is a 9-line diff in one file. A new verifier agent would require a
   new agent definition, permission model, skill assignment, and routing
   configuration.
2. **No new routing.** The reviewer already runs Quick Verification during
   review. Adding permissions to the existing reviewer avoids introducing a
   separate agent routing decision.
3. **No duplicated permission model.** A dedicated verifier would need a
   permission model duplicating the reviewer's read-only boundaries with the
   verification additions. Extending the reviewer avoids this duplication.

## Evidence

| Check | Result |
|---|---|
| Repository validation (ruff, mypy, pytest) | TBD |
| Quick Verification | PASS (29 files, 8/8 SHA-256, 3/3 body equality) |
| Standard Verification | PASS WITH NOTES — 4 non-blocking findings (grep false positives) |
| Certification | TBD — must be executed after release preparation |
| Reviewer repository ↔ active equality | SHA-256 `d395635a...` match, cmp exit 0 |
| Git scope | TBD — release preparation diff must be limited to allowed files |
| NeuralEngine unchanged | Confirmed (`git -C /run/media/grzanka/777/projekty/NeuralEngine status --short` clean) |

### Implementation evidence

- Implementation commit: `674c8d6` (feat: enforce reviewer verification permissions)
- Merge commit: `22f7592` (Merge pull request #5 into main)
- Implementation review: `.agent-work/reviews/review-agent-pack-v0.3-reviewer-verification-permissions.md` (READY FOR REVIEW)
- Release preparation branch: `release/agent-pack-v0.3.0`
- Release checkpoint: `22f759237215dd57981d37a76c29100447c18ae4`

## Security boundary

All reviewer deny boundaries are preserved:

- `edit: deny` — cannot modify files.
- `task: deny` — cannot delegate to sub-agents.
- Git writes denied (add, commit, push, reset, restore, checkout, switch).
- Destructive commands denied (rm, mv, cp).
- In-place sed denied (`sed -i*`).
- Ruff mutation denied (check --fix, format).
- Fallback `bash "*": ask` retained — no unrestricted shell.
- No Brain write permission.

The eight new allow patterns are all read-only:
`find`, `test`, `wc`, `sha256sum`, `diff`, `cmp`, `grep` — and `sed` without `-i`
(in-place sed remains explicitly denied as `sed -i*`).

## Compatibility

- Shared contracts unchanged from v0.2.0.
- No new shared contracts, platform adapters, or MANIFEST entries.
- No breaking changes from v0.2.0.
- Active sync performed separately (controlled copy).
- Codex, Claude, Antigravity remain placeholders.

## Deferred work

The following items from the original v0.3.0 roadmap (Installation and
workstation rollout) are deferred:

- Deterministic OpenCode installation procedure.
- Backup and rollback procedure.
- Home workstation installation, verification, and certification.
- Office workstation installation, verification, and certification.
- Installation documentation in README.

## Release gate

Completed gates:

1. Repository validation — PASS (`ruff format --check`, `ruff check`, `mypy src tests`, `pytest` — 16 tests).
2. Quick Verification — PASS (31 files, 8/8 SHA-256, 3/3 body equality).
3. Standard Verification — PASS WITH NOTES (4 non-blocking grep false positives).

Remaining gate:

4. Release certification must be executed and return CERTIFIED or CERTIFIED WITH NOTES.

### Tag namespace

When the release is approved and merged, the tag must be:

```text
agent-pack-v0.3.0
```

Not `v0.3.0`. The `agent-pack-` prefix distinguishes Agent Pack releases from
NeuralEngine-Handbook releases.

This decision does not claim the release has already been tagged or published.
