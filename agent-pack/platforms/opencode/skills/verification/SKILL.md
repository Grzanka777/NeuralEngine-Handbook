---
name: verification
description: OpenCode adapter for the NeuralEngine Agent Pack Verification Framework. Implements Quick Verification (mechanical integrity, PASS/FAIL), Standard Verification (structural completeness, PASS/PASS WITH NOTES/BLOCKED/FAIL), and Certification Report (formal artifact from completed verification evidence, CERTIFIED/CERTIFIED WITH NOTES/NOT CERTIFIED). Read-only.
compatibility: opencode
metadata:
  workflow: verification
  audience: maintainers
  contract: agent-pack/shared/verification.md
---

# Agent Pack Verification (OpenCode)

Use this skill to run Quick Verification and Standard Verification against
the current NeuralEngine Agent Pack and active OpenCode configuration.

This skill implements Quick Verification and Standard Verification as defined
by the authoritative shared contract:

```text
agent-pack/shared/verification.md
```

This skill implements all three stages defined by the contract: Quick
Verification, Standard Verification, and Certification Report.

## Authority

The authoritative source is
[shared/verification.md](../../../shared/verification.md). This skill is an
OpenCode platform adapter. It maps the platform-neutral contract to
platform-native read-only commands.

In case of conflict, the shared contract is authoritative.

## Scope

This skill implements two verification levels:

**Quick Verification** — mechanical integrity check. Verifies:
1. Required file presence and count.
2. Exact-copy SHA-256 equality (8 OpenCode files vs active `~/.config/opencode/`).
3. Shared body equality (3 shared contracts vs OpenCode SKILL.md bodies).
4. Source coverage for `shared/neuralengine.md` (merged source, not byte equality).
5. Prohibited artifact absence (symlinks, scripts, generators, installers).
6. Git working-tree scope integrity.
7. MANIFEST target presence.

**Standard Verification** — structural completeness check. Adds:
8. Shared-contract mandatory audit (all five contracts).
9. Cross-document consistency audit.
10. MANIFEST mapping accuracy audit.
11. Platform support status audit.
12. Permission integrity audit.
13. Placeholder audit.
14. Review artifact presence and format audit.
15. NeuralEngine usage evidence audit.
16. Known limitations audit.

This skill does **not** verify:
- Semantic correctness of implementation (repository-review).
- Python code quality (python-validation).
- System health (arch-linux).
- NeuralEngine record validity (Brain authority).

## Prerequisites

Before running Quick Verification:

1. Run `neural status` and record the result.
2. Determine whether `neural search` is required.
3. Confirm the Agent Pack repository is at the expected path.
4. Confirm `~/.config/opencode/` is accessible.

## Quick Verification procedure

Run the following checks in order. Stop on the first FAIL.

### 1. Required files

Verify every file listed in `agent-pack/MANIFEST.md` plus additional
documentation files declared in `ARCHITECTURE.md` and `ROADMAP.md` exists at
its expected path.

```text
# List all expected files from MANIFEST.md shared-to-platform mapping
# plus documentation files: ARCHITECTURE.md, DEFINITION-OF-DONE.md, ROADMAP.md,
# MANIFEST.md, README.md, VERSION, DECISIONS/*.md
# plus platform-specific: opencode.json, neuralengine-usage.md, agent files,
# skill files, placeholder READMEs

# Count files under agent-pack/ (excluding .git, node_modules, etc.)
find agent-pack -type f -not -path '*/.git/*' -not -path '*/node_modules/*' | wc -l
```

Expected: file count matches the declared structure. Missing files → FAIL.

### 2. Exact-copy SHA-256 equality

Compare each exact-copy file against its active OpenCode configuration source.

```text
# opencode.json
sha256sum agent-pack/platforms/opencode/opencode.json \
         /home/grzanka/.config/opencode/opencode.json

# neuralengine-usage.md
sha256sum agent-pack/platforms/opencode/neuralengine-usage.md \
         /home/grzanka/.config/opencode/neuralengine-usage.md

# agents/arch-data-engineer.md
sha256sum agent-pack/platforms/opencode/agents/arch-data-engineer.md \
         /home/grzanka/.config/opencode/agents/arch-data-engineer.md

# agents/reviewer.md
sha256sum agent-pack/platforms/opencode/agents/reviewer.md \
         /home/grzanka/.config/opencode/agents/reviewer.md

# skills/neuralengine/SKILL.md
sha256sum agent-pack/platforms/opencode/skills/neuralengine/SKILL.md \
         /home/grzanka/.config/opencode/skills/neuralengine/SKILL.md

# skills/repository-review/SKILL.md
sha256sum agent-pack/platforms/opencode/skills/repository-review/SKILL.md \
         /home/grzanka/.config/opencode/skills/repository-review/SKILL.md

# skills/python-project-validation/SKILL.md
sha256sum agent-pack/platforms/opencode/skills/python-project-validation/SKILL.md \
         /home/grzanka/.config/opencode/skills/python-project-validation/SKILL.md

# skills/arch-linux-diagnostics/SKILL.md
sha256sum agent-pack/platforms/opencode/skills/arch-linux-diagnostics/SKILL.md \
         /home/grzanka/.config/opencode/skills/arch-linux-diagnostics/SKILL.md
```

Every pair must produce identical SHA-256 hashes. Any mismatch → FAIL.

### 3. Shared body equality

Compare shared contract bodies against OpenCode SKILL.md bodies after removing
YAML frontmatter.

```text
# repository-review
diff <(sed -n '/^---$/,/^---$/!p' agent-pack/platforms/opencode/skills/repository-review/SKILL.md | sed '/^---$/d' | sed '1{/^$/d}' | sed '1{/^$/d}') \
     agent-pack/shared/repository-review.md

# python-validation
diff <(sed -n '/^---$/,/^---$/!p' agent-pack/platforms/opencode/skills/python-project-validation/SKILL.md | sed '/^---$/d' | sed '1{/^$/d}' | sed '1{/^$/d}') \
     agent-pack/shared/python-validation.md

# arch-linux
diff <(sed -n '/^---$/,/^---$/!p' agent-pack/platforms/opencode/skills/arch-linux-diagnostics/SKILL.md | sed '/^---$/d' | sed '1{/^$/d}' | sed '1{/^$/d}') \
     agent-pack/shared/arch-linux.md
```

Each `diff` must produce no output (byte-for-byte equal after frontmatter
removal). Any difference → FAIL.

### 4. Source coverage for shared/neuralengine.md

`shared/neuralengine.md` merges two sources and is intentionally not
byte-identical to either. Quick Verification performs a minimal mandatory-rule
presence check rather than byte equality.

```text
# Verify key mandatory phrases are present
for phrase in \
  "neural status" \
  "search decision" \
  "one best query" \
  "record ID" \
  "authority model" \
  "explicit user authorization" \
  "no automatic promotion" \
  "Do not claim.*NeuralEngine.*based only on running" \
  "completion rules"; do
  grep -qi "$phrase" agent-pack/shared/neuralengine.md || echo "MISSING: $phrase"
done
```

All mandatory phrases must be present. Any missing → FAIL.

### 5. Prohibited artifacts

Verify no symlinks, scripts, generators, or installers exist.

```text
# Symlinks
find agent-pack -type l | wc -l  # must be 0

# Scripts (.py, .sh, .js, .ts)
find agent-pack -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.ts" \) | wc -l  # must be 0

# Generators or installers (Makefile, justfile, tox.ini, noxfile.py, package.json scripts)
find agent-pack -type f \( -name "Makefile" -o -name "justfile" -o -name "tox.ini" -o -name "noxfile.py" -o -name "package.json" \) | wc -l  # must be 0
```

Any non-zero count → FAIL.

### 6. Git scope

Verify no Agent Pack changes modified files outside `agent-pack/`.

```text
git status --short
```

Pre-existing dirty files (e.g., `handbook/domain/knowledge.md`,
`outputs/generated/HANDBOOK.md`) are reported separately but do not cause
FAIL unless they were modified by the current Agent Pack task.

Any file outside `agent-pack/` that was created or modified by the current
task → FAIL.

### 7. MANIFEST targets

Verify every OpenCode mapping target listed in MANIFEST.md exists.

```text
# Check that each MANIFEST target path is a real file or directory
for target in \
  "agent-pack/platforms/opencode/neuralengine-usage.md" \
  "agent-pack/platforms/opencode/skills/neuralengine/SKILL.md" \
  "agent-pack/platforms/opencode/skills/repository-review/SKILL.md" \
  "agent-pack/platforms/opencode/skills/python-project-validation/SKILL.md" \
  "agent-pack/platforms/opencode/skills/arch-linux-diagnostics/SKILL.md"; do
  test -f "$target" || echo "MISSING: $target"
done

# Placeholder platforms
for dir in agent-pack/platforms/codex agent-pack/platforms/claude agent-pack/platforms/antigravity; do
  test -d "$dir" || echo "MISSING: $dir"
  grep -q "Not implemented" "$dir/README.md" 2>/dev/null || echo "NOT PLACEHOLDER: $dir/README.md"
done

# Verification skill
test -f agent-pack/platforms/opencode/skills/verification/SKILL.md || echo "MISSING: verification skill"
```

Any missing target → FAIL.

## Verdict

After all checks pass:

```text
PASS
```

If any check fails:

```text
FAIL
```

Do not attempt repair. Report the exact failure and stop.

## Report format

```text
# Quick Verification

## Verdict
PASS | FAIL

## Checkpoint
- Agent Pack version: <version>
- Repository: <path>
- Git HEAD: <sha>
- Platform: OpenCode

## Checks
| Check | Result |
|---|---|
| Required files | <count> (PASS/FAIL) |
| Exact-copy equality | 8/8 (PASS/FAIL) |
| Shared body equality | 3/3 (PASS/FAIL) |
| NeuralEngine source coverage | PASS/FAIL |
| Prohibited artifacts | 0/0/0 (PASS/FAIL) |
| Git scope | clean/dirty (PASS/FAIL) |
| MANIFEST targets | <N>/<N> (PASS/FAIL) |

## Evidence
<concise hashes, counts, and comparison results>

## NeuralEngine usage
- neural status: <output>
- Search decision: <used/not used>
- Queries: <list or None>
- Results: <list or None>

## Failures
None | <exact blocking failures>
```

## Read-only boundary

This skill uses only read-only commands. It does **not**:

- Edit files.
- Format or fix code.
- Regenerate files.
- Commit or push.
- Perform Brain writes.
- Run destructive shell operations.
- Repair detected drift.

## Standard Verification

Standard Verification extends Quick Verification with structural and
contractual completeness checks. It is read-only, evidence-complete, and
dependent on Quick Verification passing first.

### Prerequisites

1. Quick Verification must have passed (PASS).
2. `neural status` must have been run and recorded.
3. NeuralEngine search decision must be documented.

If Quick Verification was not run or returned FAIL, do not proceed.
Report `FAIL` with the reason.

### Standard Verification procedure

Run these checks in addition to the Quick Verification evidence already
collected. Order findings by severity (blockers first).

#### 8. Shared-contract audit

For each of the five shared contracts, verify structural completeness:

```text
contracts="
agent-pack/shared/neuralengine.md
agent-pack/shared/repository-review.md
agent-pack/shared/python-validation.md
agent-pack/shared/arch-linux.md
agent-pack/shared/verification.md
"

for c in $contracts; do
  echo "=== $c ==="
  test -f "$c" || { echo "MISSING: $c"; continue; }
  # Check for required structural sections
  for section in "Purpose" "Scope" "workflow\|procedure\|sequence" "evidence\|report" "verdict\|failure\|PASS\|FAIL"; do
    grep -qi "$section" "$c" || echo "  SECTION GAP: $section not found"
  done
done
```

For `shared/neuralengine.md` specifically, verify mandatory rule presence
(the same set checked by Quick Verification plus additional operational rules):

```text
for phrase in \
  "substantive task" \
  "search decision" \
  "query construction\|one best query" \
  "search result handling\|record type" \
  "provenance" \
  "conflict" \
  "read boundary\|read-only" \
  "write boundary\|write requires" \
  "lifecycle\|no automatic promotion" \
  "do not collapse" \
  "required evidence\|NeuralEngine usage" \
  "completion rules" \
  "do not claim.*NeuralEngine.*based only on running"; do
  grep -qi "$phrase" agent-pack/shared/neuralengine.md || echo "MISSING: $phrase"
done
```

Any missing mandatory phrase → finding.

For `shared/verification.md`, confirm it contains all required sections:
Purpose, Scope, Exclusions, Quick Verification, Standard Verification,
Certification Report, Workflow, Relationship, Platform capability model,
Evidence model, Verdict criteria, NeuralEngine boundary, Read-only boundary,
Extensibility.

#### 9. Cross-document consistency

Check consistency across documentation files:

```text
# Architecture: Agent Pack is part of NeuralEngine-Handbook
grep -qi "part of.*NeuralEngine-Handbook\|component of.*NeuralEngine-Handbook" \
  agent-pack/ARCHITECTURE.md || echo "FINDING: Architecture does not state Agent Pack is part of Handbook"

# README: shared contract count is five
shared_count=$(grep -c "shared/" agent-pack/README.md | head -1)
echo "Shared contract references in README: $shared_count"

# ROADMAP: v0.2.0 status check
grep -qi "completed" agent-pack/ROADMAP.md && echo "v0.2.0 status: completed" || echo "FINDING: v0.2.0 status unclear"

# Certification implemented
grep -qi "certification" agent-pack/shared/verification.md && echo "Certification: contract present" || echo "FINDING: Certification contract missing"

# Codex/Claude/Antigravity status
for platform in Codex Claude Antigravity; do
  grep -qi "$platform.*placeholder\|$platform.*not implemented" agent-pack/README.md || echo "FINDING: $platform status unclear in README"
done

# No separate product lifecycle
grep -qi "separate.*product\|independent.*product\|standalone.*product" agent-pack/ARCHITECTURE.md && echo "FINDING: Architecture may reference separate product" || echo "No separate product lifecycle"

# Controlled-copy model
grep -qi "controlled.copy\|controlled copy\|not independent.*source" agent-pack/ARCHITECTURE.md || echo "FINDING: Controlled-copy model not documented"
grep -qi "controlled.copy\|controlled copy\|not independent.*source" agent-pack/README.md || echo "FINDING: Controlled-copy model not in README"

# Current shared contract count is five
grep -c "shared/.*\.md" agent-pack/ARCHITECTURE.md | head -1
```

Any contradiction → finding.

#### 10. MANIFEST mapping accuracy

Verify MANIFEST.md is accurate:

```text
# Check all shared contracts are mapped
for contract in neuralengine repository-review python-validation arch-linux verification; do
  grep -q "shared/$contract" agent-pack/MANIFEST.md || echo "FINDING: $contract not mapped in MANIFEST"
done

# Check MANIFEST states no platform copy is independent source of truth
grep -qi "not independent source" agent-pack/MANIFEST.md || echo "FINDING: MANIFEST does not state boundary"
```

#### 11. Platform support audit

Verify support status for each platform:

```text
# OpenCode: supported
grep -qi "opencode.*supported" agent-pack/README.md || echo "FINDING: OpenCode support status unclear"

# Codex, Claude, Antigravity: placeholder
for platform in codex claude antigravity; do
  dir="agent-pack/platforms/$platform"
  test -d "$dir" || { echo "MISSING: $dir"; continue; }
  grep -qi "not implemented" "$dir/README.md" 2>/dev/null || echo "FINDING: $platform placeholder status unclear"
  # Count files in directory - should be exactly 1 (README.md)
  count=$(find "$dir" -type f | wc -l)
  if [ "$count" -ne 1 ]; then
    echo "FINDING: $platform has $count files (expected 1 - placeholder README only)"
  fi
done
```

Any mismatch between README support matrix and actual platform state → finding.

#### 12. Permission audit

Verify reviewer and verification permissions against documented requirements:

```text
# Reviewer edit/task denied
grep -q "edit: deny" agent-pack/platforms/opencode/agents/reviewer.md || echo "FINDING: Reviewer does not deny edit"
grep -q "task: deny" agent-pack/platforms/opencode/agents/reviewer.md || echo "FINDING: Reviewer does not deny task"

# Destructive commands denied
for cmd in "git add" "git commit" "git push" "rm \*" "sed -i"; do
  grep -q "\"$cmd.*deny" agent-pack/platforms/opencode/agents/reviewer.md || echo "FINDING: Reviewer missing deny for: $cmd"
done

# Auto-fix denied
grep -q "ruff check --fix.*: deny\|ruff format.*: deny" agent-pack/platforms/opencode/agents/reviewer.md || echo "FINDING: Auto-fix not denied"

# bash "*" is not allow
grep -q '"\*": allow' agent-pack/platforms/opencode/agents/reviewer.md && echo "FINDING: reviewer has unrestricted bash" || echo "Reviewer bash: restricted (correct)"

# Verification permissions document exists
test -f agent-pack/platforms/opencode/verification-permissions.md || echo "MISSING: verification-permissions.md"

# Verification permissions prohibits bash "*"
grep -q 'bash "\*".*allow' agent-pack/platforms/opencode/verification-permissions.md && echo "FINDING: verification-permissions allows unrestricted bash" || echo "Permission doc: prohibits unrestricted bash (correct)"

# Required verification commands classified
grep -qi "required read-only" agent-pack/platforms/opencode/verification-permissions.md || echo "FINDING: Required command list missing"
grep -qi "currently allowed" agent-pack/platforms/opencode/verification-permissions.md || echo "FINDING: Allowlist analysis missing"
```

Any missing deny, unsafe allow → finding.

#### 13. Placeholder audit

Verify placeholder directories contain only README.md:

```text
for dir in agent-pack/platforms/codex agent-pack/platforms/claude agent-pack/platforms/antigravity; do
  count=$(find "$dir" -type f -not -name "README.md" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "FINDING: $dir contains non-placeholder files:"
    find "$dir" -type f -not -name "README.md"
  fi
done
```

Any non-README.md file → finding.

#### 14. Review artifact audit

Verify required review artifacts exist and have minimum structure:

```text
reviews="
.agent-work/reviews/review-implement-agent-pack-handbook-extension-v1.md
.agent-work/reviews/review-independent-agent-pack-v0.1.0.md
.agent-work/reviews/review-formalize-agent-pack-architecture-and-dod.md
.agent-work/reviews/review-decide-verification-framework-architecture.md
.agent-work/reviews/review-implement-verification-shared-contract-v0.2.md
.agent-work/reviews/review-implement-opencode-quick-verification-v0.2.md
"

for r in $reviews; do
  echo "=== $r ==="
  test -f "$r" || { echo "  MISSING"; continue; }
  # Check for minimum structure
  for section in "Verdict\|verdict" "Checkpoint\|checkpoint" "Validation\|validation" "Scope audit\|scope audit" "Blockers\|blockers" "NeuralEngine usage\|NeuralEngine"; do
    grep -qi "$section" "$r" || echo "  SECTION GAP: $section"
  done
done
```

Do not re-review semantic conclusions. Check only structural presence.

#### 15. NeuralEngine evidence audit

Verify review artifacts contain NeuralEngine usage evidence:

```text
for r in $reviews; do
  test -f "$r" || continue
  # Check neural status output present
  grep -qi "neural.*status\|Neural Engine" "$r" || echo "FINDING: No neural status in $r"
  # Check search decision present
  grep -qi "search decision\|Search decision" "$r" || echo "FINDING: No search decision in $r"
  # Check no unauthorized Brain writes
  grep -qi "Brain write.*performed\|Brain write.*authorized" "$r" && echo "NOTE: Brain write mentioned in $r"
done
```

Any missing evidence → finding.

#### 16. Known limitations audit

Verify current limitations are documented:

```text
# Certification not implemented
grep -qi "certification.*not.*implemented\|certification.*planned" agent-pack/shared/verification.md || echo "FINDING: Certification status not documented in verification.md"

# No verifier agent
test -f agent-pack/platforms/opencode/agents/verifier.md && echo "FINDING: verifier agent exists (should not)" || echo "No verifier agent (correct)"

# Codex/Claude/Antigravity not implemented
for platform in codex claude antigravity; do
  grep -qi "not implemented" "agent-pack/platforms/$platform/README.md" 2>/dev/null || echo "FINDING: $platform limitation not documented"
done

# No automatic installer, generator, or symlink sync
grep -qi "no.*automatic install\|no.*generator\|no.*symlink" agent-pack/ARCHITECTURE.md || echo "FINDING: Architecture does not document absence of automation"
```

### Standard Verification verdict criteria

| Verdict | Criteria |
|---|---|
| `PASS` | Quick PASS + all Standard checks SATISFIED + no blockers + no contradictions + no misrepresented capabilities |
| `PASS WITH NOTES` | All required criteria SATISFIED + only non-blocking findings + limitations accurately documented |
| `BLOCKED` | Required evidence cannot be obtained OR permissions prevent required checks OR environment failure OR ambiguous checkpoint |
| `FAIL` | Quick FAIL OR missing required files/mappings OR documented contradiction OR unsafe permission boundary OR false support status OR absent required evidence |

### Standard Verification report format

```text
# Standard Verification

## Verdict
PASS | PASS WITH NOTES | BLOCKED | FAIL

## Checkpoint
- Agent Pack version: <version>
- Repository: <path>
- Git HEAD: <sha>
- Platform: OpenCode
- Verifier: <identity>
- Timestamp: <iso>

## Quick Verification prerequisite
- Result: PASS (ran at <timestamp>)
- Summary: <file count, 8/8 SHA-256, 3/3 body equality>

## Shared contracts
| Contract | File | Purpose | Scope | Workflow | Evidence | Verdict | Findings |
|---|---|---|---|---|---|---|---|
| neuralengine | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | <notes> |
| repository-review | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | <notes> |
| python-validation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | <notes> |
| arch-linux | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | <notes> |
| verification | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | <notes> |

## Documentation consistency
| Document | Check | Result |
|---|---|---|
| ARCHITECTURE | Part of Handbook | <result> |
| ARCHITECTURE | Controlled-copy model | <result> |
| README | Shared contract count (5) | <result> |
| ROADMAP | v0.2.0 status | <result> |
| ROADMAP | Certification not implemented | <result> |
| ... | ... | ... |

## Platform support
| Platform | Status | Directory | Placeholder verified |
|---|---|---|---|
| OpenCode | Supported | ✓ | N/A |
| Codex | Placeholder | ✓ | ✓ |
| Claude Code | Placeholder | ✓ | ✓ |
| Antigravity | Placeholder | ✓ | ✓ |

## Permissions
| Check | Result |
|---|---|
| Reviewer edit denied | <result> |
| Reviewer task denied | <result> |
| Destructive commands denied | <result> |
| Auto-fix denied | <result> |
| bash "*" not allow | <result> |
| Verification permissions documented | <result> |

## Review evidence

<per-review-artifact table with verdict, checkpoint, validation, scope, NeuralEngine presence>

## NeuralEngine usage
- neural status: <output>
- Search decision: <used/not used>
- Queries: <list or None>
- Results: <list or None>
- Effect on work: <explanation>

## Findings
Ordered by severity:
1. BLOCKERS: <list or None>
2. DEFECTS: <list or None>
3. RISKS: <list or None>
4. DEVIATIONS: <list or None>
5. NOTES: <list or None>

## Blockers and deviations
None | <exact items>
```

Readiness score is optional and secondary. Do not include by default. If
included, state that it is optional and cannot override the verdict.

## Certification Report

Certification Report is a **formal artifact**, not a verification level.
It is produced from already-completed Quick Verification and Standard
Verification evidence. It does not re-run verification checks or introduce
new verification logic.

### Prerequisites

1. Quick Verification must have returned PASS.
2. Standard Verification must have returned PASS or PASS WITH NOTES.
3. All evidence must be available from the completed verification runs.
4. `neural status` must have been run.

### Certification Report verdicts

| Verdict | Criteria |
|---|---|
| `CERTIFIED` | Quick PASS + Standard PASS + all evidence present + no blockers + no unsupported capabilities misrepresented |
| `CERTIFIED WITH NOTES` | Quick PASS + Standard PASS WITH NOTES (or PASS) + non-blocking findings documented + all limitations accurately declared |
| `NOT CERTIFIED` | Quick FAIL or Standard FAIL or Standard BLOCKED or evidence incomplete or blockers present or false support status |

Note: `CERTIFIED` and `CERTIFIED WITH NOTES` are distinct from Standard
Verification verdicts. A Standard PASS WITH NOTES can result in a
`CERTIFIED WITH NOTES` report, not a degraded Standard verdict.

### Certification Report template

```text
# Certification Report

## Certification verdict
CERTIFIED | CERTIFIED WITH NOTES | NOT CERTIFIED

## Checkpoint
- Agent Pack version: <version>
- Repository: NeuralEngine-Handbook
- Git HEAD: <sha>
- Branch: <branch>
- Platform: OpenCode
- Timestamp: <iso>
- Certifier: <identity>

## Quick Verification summary
- Result: PASS
- File count: <N>
- Exact-copy SHA-256: 8/8 PASS
- Shared body equality: 3/3 PASS
- Prohibited artifacts: 0
- Git scope: clean
- MANIFEST targets: all present

## Standard Verification summary
- Result: PASS | PASS WITH NOTES
- Shared contracts: 5/5 structurally complete
- Cross-document consistency: <summary>
- MANIFEST accuracy: <summary>
- Platform support: <summary>
- Permission integrity: <summary>
- Placeholder audit: <summary>
- Review artifacts: <summary>
- NeuralEngine evidence: <summary>
- Known limitations: <summary>

## Shared contract summary
| Contract | Structural | Mandatory rules | Evidence |
|---|---|---|---|
| neuralengine.md | ✓ | ✓ | ✓ |
| repository-review.md | ✓ | ✓ | ✓ |
| python-validation.md | ✓ | ✓ | ✓ |
| arch-linux.md | ✓ | ✓ | ✓ |
| verification.md | ✓ | ✓ | ✓ |

## Platform capability summary
| Capability | Status |
|---|---|
| File listing | AVAILABLE |
| SHA-256 hashing | AVAILABLE |
| Byte comparison | AVAILABLE |
| Text search | AVAILABLE |
| Git read-only | AVAILABLE |
| NeuralEngine CLI | AVAILABLE |
| Permission introspection | AVAILABLE |

## Permission summary
- Reviewer: edit/task denied, destructive commands denied, auto-fix denied
- Verification: read-only commands documented, unrestricted bash prohibited
- No verifier agent exists

## NeuralEngine usage
- neural status: <output>
- Search decision: <used/not used>
- Queries: <list or None>
- Results: <list or None>
- Effect on work: <explanation>

## Known limitations
- Certification Report is a formal artifact, not a verification level
- No verifier agent exists
- Codex: not implemented (placeholder)
- Claude Code: not implemented (placeholder)
- Antigravity: not implemented (placeholder)
- No automatic installation, generators, or symlink synchronization

## Blockers and deviations
None | <exact items>

## Certification decision
CERTIFIED: The Agent Pack at checkpoint <sha> meets all structural integrity
and contractual completeness criteria defined by shared/verification.md.
No blockers. All evidence present and verified.
```

### Certification Report rules

- Does **not** re-run Quick or Standard Verification.
- Does **not** introduce new verification checks.
- Does **not** perform semantic review.
- Does **not** execute pytest, ruff, mypy, or diagnostics.
- Is **read-only** — does not modify any file.
- Does **not** perform Brain writes.
- Produces a file under `.agent-work/certifications/` with the naming
  convention: `certification-agent-pack-v<version>-<date>.md`.

