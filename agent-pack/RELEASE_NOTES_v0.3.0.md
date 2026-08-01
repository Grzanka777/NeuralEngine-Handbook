# Agent Pack v0.3.0 Release Notes

## Highlights

Agent Pack v0.3.0 is a permission-enforcement release. It adds eight narrow
read-only shell command permissions to the OpenCode reviewer agent, allowing
Quick Verification to run without manual permission prompts. The reviewer
remains read-only, no dedicated verifier agent was introduced, and shared
contracts are unchanged from v0.2.0.

## Reviewer verification enforcement

The v0.2.0 Verification Framework was functionally complete but blocked at
runtime: the reviewer agent could not execute 7 of 14 required Quick
Verification commands without manual `ask` prompts. v0.3.0 closes that gap.

### What changed

- Eight read-only shell command permission patterns added to the reviewer:
  `find *`, `test *`, `wc *`, `sha256sum *`, `diff *`, `cmp *`, `grep *`,
  `sed *`.
- `verification` added to the reviewer's required skills list.
- No other files, agents, skills, or configuration changed.

### What did not change

- `edit: deny` retained.
- `task: deny` retained.
- All seven Git write patterns retained as deny.
- `rm *`, `mv *`, `cp *` retained as deny.
- `sed -i*` retained as deny.
- `uv run ruff check --fix*` and `uv run ruff format *` retained as deny.
- Fallback `bash "*": ask` retained.
- No unrestricted shell allow (`bash "*": allow` is absent).
- No dedicated verifier agent exists.

## Permission delta

Eight allow patterns inserted between `uv run pytest *` and `git add*`:

```yaml
    "find *": allow
    "test *": allow
    "wc *": allow
    "sha256sum *": allow
    "diff *": allow
    "cmp *": allow
    "grep *": allow
    "sed *": allow
```

Total diff: 1 file changed, 9 insertions (8 permissions + 1 skill reference).

## Read-only boundary

The reviewer's read-only boundary is preserved and strengthened:

| Boundary | Status |
|---|---|
| Edit files | Denied |
| Delegate tasks | Denied |
| Git writes (add, commit, push, reset, restore, checkout, switch) | Denied |
| Destructive commands (rm, mv, cp) | Denied |
| In-place sed (`sed -i*`) | Denied |
| Ruff mutation (check --fix, format) | Denied |
| Brain writes | Prohibited by skill contract |
| Unrestricted bash (`"*": allow`) | Absent |

## Runtime verification

After explicit active controlled-copy synchronization, Quick Verification runs
through the reviewer without permission prompts. The eight new allow patterns
cover all commands required by:

- `find` (file presence, artifact detection)
- `test` (path existence checks)
- `wc` (file/line counting)
- `sha256sum` (exact-copy equality)
- `diff` (byte comparison)
- `cmp` (byte comparison alternative)
- `grep` (text search, placeholder and mandatory-rule detection)
- `sed` (YAML frontmatter stripping, without `-i`)

## Compatibility

- Base release: Agent Pack v0.2.0.
- Release checkpoint before release preparation: `22f759237215dd57981d37a76c29100447c18ae4`.
- Implementation commit: `674c8d6`.
- Merge commit: `22f7592`.
- Shared contracts unchanged from v0.2.0.
- No new shared contracts, platform adapters, or MANIFEST entries.
- Quick Verification PASS at checkpoint `22f759237215dd57981d37a76c29100447c18ae4`.
  - 31 Agent Pack files.
  - 8/8 exact-copy equality.
  - 3/3 shared body equality.
  - No permission prompts during Quick Verification.
- Standard Verification PASS WITH NOTES at release preparation checkpoint (4 non-blocking grep false positives).
- No Brain write.
- No breaking changes from v0.2.0.

## Known limitations

- Codex, Claude Code, and Antigravity adapters remain placeholders.
- No automatic installation.
- No generators.
- No symlink synchronization.
- No dedicated verifier agent.
- Installation and workstation rollout (originally planned for v0.3.0) are
  deferred to a future milestone.
- Certification remains explicit and is not part of routine Quick Verification.
- Certification not yet executed for v0.3.0.

## Upgrade notes

No breaking changes from v0.2.0. All existing shared contracts and platform
files are unchanged (SHA-256 verified against v0.2.0 certification).

To upgrade:

1. Pull the latest `agent-pack/` content from branch `release/agent-pack-v0.3.0`.
2. Copy the updated reviewer to `~/.config/opencode/agents/reviewer.md`:
   ```text
   cp agent-pack/platforms/opencode/agents/reviewer.md /home/grzanka/.config/opencode/agents/reviewer.md
   ```
3. Verify SHA-256 equality:
   ```text
   sha256sum agent-pack/platforms/opencode/agents/reviewer.md \
            /home/grzanka/.config/opencode/agents/reviewer.md
   ```
4. Run Quick Verification to confirm the reviewer can execute all checks
   without permission prompts.
5. Run Certification for formal release acceptance.
