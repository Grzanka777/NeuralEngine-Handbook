# Agent Pack Verification Framework

Use this contract to verify the structural integrity of the NeuralEngine
Agent Pack. It defines what to verify, not how to implement verification on a
specific platform.

## Purpose

The Verification Framework exists to prove that the Agent Pack is structurally
intact at a given checkpoint:

- Every required file exists.
- Every exact-copy file is byte-identical to its source.
- Every shared contract maps correctly to its platform copies.
- No document contradicts another.
- No prohibited artifacts (symlinks, generators, scripts, installers) have been
  introduced.
- Mandatory evidence (NeuralEngine usage, review artifacts) is present.

Structural verification is separate from semantic review. A file can be
structurally present and hash-verified while being semantically incorrect.
[repository-review.md](repository-review.md) handles semantic correctness.
This contract handles structural integrity.

This contract is platform-neutral. It defines *what* must be verified and the
evidence standard. Platform adapters define *how* to perform verification using
platform-native tools.

Evidence matters because prose assertions are not auditable. Every claim must
be traceable to a specific file, hash, command output, or review artifact.

## Scope

The Verification Framework verifies:

1. **Required file presence** — every file listed in
   [MANIFEST.md](../MANIFEST.md) exists at its expected path.
2. **Exact-copy equality** — platform-specific files marked as exact copies
   match their source by SHA-256.
3. **Shared-to-platform body equality** — shared contract bodies match
   platform SKILL.md bodies after YAML frontmatter removal, where applicable.
4. **MANIFEST mapping accuracy** — every shared contract is mapped to the
   correct platform adapter paths.
5. **Agent Pack structural consistency** — no contradiction between
   ARCHITECTURE.md, README.md, MANIFEST.md, ROADMAP.md,
   DEFINITION-OF-DONE.md, and DECISIONS/ records.
6. **Platform support status accuracy** — the support matrix in README.md
   matches the actual state of `platforms/` directories.
7. **Reviewer and verifier permission integrity** — reviewer agent permissions
   remain intact (edit: deny, task: deny, destructive commands denied).
   Verification skill permissions match the read-only model.
8. **Absence of prohibited artifacts** — no symlinks, scripts (`.py`, `.sh`,
   `.js`, `.ts`), generators, automatic installers, or CI files exist under
   `agent-pack/`.
9. **Required review and certification evidence** — review artifacts exist at
   expected paths with correct verdict format.
10. **Git scope integrity** — no files outside `agent-pack/` were modified by
    Agent Pack work.
11. **NeuralEngine usage evidence presence** — every review artifact contains
    a NeuralEngine usage section with `neural status` output and search
    decision.

## Explicit exclusions

The Verification Framework does **not** verify:

| Excluded responsibility | Assigned to |
|---|---|
| Semantic correctness of implementation | [repository-review.md](repository-review.md) |
| Task-contract compliance | [repository-review.md](repository-review.md) |
| Python code quality | [python-validation.md](python-validation.md) |
| Linux system health | [arch-linux.md](arch-linux.md) |
| NeuralEngine record validity | NeuralEngine Brain (authority) |
| Brain data integrity beyond availability evidence | NeuralEngine Brain |
| Model quality | Out of scope (platform concern) |
| Model benchmark performance | Out of scope |
| API cost | Out of scope |

Do not expand the scope of verification to cover these exclusions. If an
exclusion overlaps with a structural concern (e.g., Python test results being
absent from a review artifact), verify only that the evidence is *present*,
not that it is *correct*.

## Quick Verification

Quick Verification is:

- **Mechanical** — no human judgment required.
- **Read-only** — does not modify any file.
- **Deterministic** — same input produces the same output every time.
- **Fast** — completes in seconds.

### What Quick Verification checks

1. File count matches the expected Agent Pack file count.
2. Every file listed in MANIFEST.md exists at its mapped path.
3. Every exact-copy file matches its active configuration source by SHA-256.
4. Every shared-to-platform body comparison passes (byte-for-byte after YAML
   frontmatter removal).
5. No symlinks exist under `agent-pack/`.
6. No script files (`.py`, `.sh`, `.js`, `.ts`) exist under `agent-pack/`.
7. No generators or installers exist under `agent-pack/`.
8. Git working tree shows no Agent Pack files modified outside `agent-pack/`.

### Quick Verification verdicts

| Verdict | Meaning |
|---|---|
| `PASS` | All mechanical checks passed. Proceed to Standard Verification or ordinary review. |
| `FAIL` | One or more mechanical checks failed. Drift detected. Do not proceed. Do not repair automatically. |

A `FAIL` blocks Standard Verification. Correct the drift before retrying.

### When to run Quick Verification

- **Optional** before an ordinary implementation review.
- **Mandatory** before Standard Verification.
- **Mandatory** before creating a Certification Report.
- **Recommended** after any platform-file copy or update.

## Standard Verification

Standard Verification is:

- **Structural and contractual** — covers mechanical integrity plus
  completeness and consistency.
- **Read-only** — does not modify any file.
- **Evidence-complete** — every finding references specific evidence.
- **Dependent on Quick Verification** — Standard Verification must not run if
  Quick Verification failed.

### What Standard Verification checks (includes all Quick checks plus)

1. **Mandatory-rule audit** for each shared contract:
   - [neuralengine.md](neuralengine.md): all mandatory global and operational
     rules present without material omission.
   - [repository-review.md](repository-review.md): required review format
     sections present.
   - [task-execution-policy.md](task-execution-policy.md): all 11 required
     sections present (Purpose, Scope, Task classes, Execution profiles, Role
     separation, Runtime substitution invariant, Supplied-routing validation,
     Delegated-prompt minimum, Explicit exclusions, Relationship to existing
     contracts, Compliance requirements). No concrete model identifiers appear.
     Cross-reference consistency with repository-review.md §Risk classification
     confirmed. No silent safeguard weakening is permitted.
   - Other shared contracts: core sections present and complete.

2. **Cross-document consistency** — no contradiction between:
   - ARCHITECTURE.md ↔ README.md ↔ MANIFEST.md ↔ ROADMAP.md ↔
     DEFINITION-OF-DONE.md ↔ DECISIONS/ records.

3. **MANIFEST accuracy** — every listed mapping matches actual files. No
   undocumented mappings. No orphaned entries.

4. **Platform support matrix accuracy** — README.md support status matches
   actual `platforms/` directory contents.

5. **Permission audit** — reviewer agent permissions intact. Verification
   skill (when implemented) has read-only permissions aligned with the reviewer
   model.

6. **Placeholder audit** — unsupported platform directories contain only
   documented placeholders with "Not implemented" status. No accidental partial
   implementation.

7. **Review artifact presence and format** — required review files exist.
   Verdict format matches the repository-review model (PASS, PASS WITH NOTES,
   BLOCKED, FAIL). NeuralEngine usage section present.

8. **NeuralEngine usage evidence audit** — every review artifact within scope
   contains:
   - `neural status` output.
   - Search decision (whether search was used and why).
   - Exact queries when search was used.
   - Record IDs and provenance when results were returned.

9. **Documented limitations** — any platform limitation is explicitly
   documented, not silently omitted.

10. **Findings ordered by severity** — blockers first, then defects, risks,
    deviations, notes.

### Standard Verification verdicts

| Verdict | Meaning |
|---|---|
| `PASS` | All applicable criteria SATISFIED. No findings. |
| `PASS WITH NOTES` | All applicable criteria SATISFIED. Non-blocking findings present. |
| `BLOCKED` | Verification could not complete. Missing dependency, permission failure, or other environmental blocker. |
| `FAIL` | One or more criteria NOT SATISFIED. At least one finding is a blocker. |

### When to run Standard Verification

- **Required** before release or certification.
- **Required** before accepting a new shared contract.
- **Required** before accepting a new platform adapter.
- **Optional** for ordinary implementation changes.

## Certification Report

A Certification Report is:

- **A formal artifact** — not a third verification level.
- **Produced from a completed Standard Verification** that passed (PASS or
  PASS WITH NOTES).
- **Checkpoint-specific** — tied to a specific Agent Pack version, git HEAD,
  and timestamp.
- **Evidence-complete** — every criterion cites a specific evidence source.
- **Suitable for release and readiness decisions.**

### Required sections

1. **Verdict** — PASS, PASS WITH NOTES, BLOCKED, or FAIL.
2. **Checkpoint** — Agent Pack version, git HEAD, branch, timestamp.
3. **Platform** — the platform on which verification was performed.
4. **Verifier identity** — human or agent that performed the verification.
5. **Quick Verification summary** — file count result, SHA-256 summary table,
   PASS/FAIL per category.
6. **Standard Verification findings** — per-criterion evidence with
   SATISFIED/NOT SATISFIED/NOT APPLICABLE determinations.
7. **SHA-256 and equality evidence** — full table of all exact-copy files with
   their SHA-256 values and source references.
8. **Platform capability summary** — which capabilities were available and
   which were NOT SUPPORTED or NOT APPLICABLE.
9. **Support status** — agent platform status per the README support matrix
   (Supported, Placeholder, Assessed — Unsupported).
10. **NeuralEngine usage** — `neural status` output, search decision, queries,
    results, and effect on work.
11. **Blockers and deviations** — none, or enumerated.

### When to produce a Certification Report

- After a Standard Verification that passed (PASS or PASS WITH NOTES).
- Before a release decision.
- As archival evidence of pack integrity at a checkpoint.

### Certification Report and Repository Review

A Certification Report does not require a completed Repository Review to
exist. For release workflows, follow the sequence defined in
[DECISIONS/verification-framework-architecture.md](../DECISIONS/verification-framework-architecture.md).

## Workflow

### Ordinary implementation change

```text
Implementation
    → Quick Verification (optional pre-check)
    → Repository Review
```

Quick Verification is optional because ordinary changes to documentation
rarely introduce drift. The reviewer may choose to run Quick Verification
as a fast sanity check before beginning semantic review.

### Release or certification workflow

```text
Implementation
    → Quick Verification (mandatory)
    → Standard Verification (mandatory)
    → Certification Report
    → Independent Review
```

Quick Verification is mandatory here because a failed mechanical check would
waste the time spent on Standard Verification. Standard Verification is
mandatory because release decisions require evidence of structural
completeness.

### New shared contract or platform adapter

```text
Implementation
    → Quick Verification (mandatory)
    → Standard Verification (mandatory)
    → Implementation Review
    → Independent Review
```

Certification Report is optional after a passed Standard Verification in this
case but recommended if the change is part of a milestone release.

## Relationship to existing contracts

### repository-review.md

- Verification Framework verifies **structural integrity** (file exists,
  hash matches, documents consistent, evidence present).
- Repository review verifies **semantic correctness** (implementation
  satisfies the task contract, design is sound).
- Repository review may use Quick Verification as a pre-check but is not
  blocked by its absence for ordinary changes.
- The reviewer may delegate structural verification to the Verification
  Framework.

### neuralengine.md

- Verification Framework checks that NeuralEngine usage evidence is present
  in review artifacts.
- Verification Framework produces its own NeuralEngine usage evidence in
  Certification Reports.
- Verification Framework follows the same Brain authorization boundary:
  read-only operations allowed, writes require explicit authorization.
- Verification Framework never performs Brain writes.

### python-validation.md

- No direct relationship. Verification Framework does not run `ruff`,
  `mypy`, or `pytest`.
- Verification Framework may check that Python validation results are
  recorded in review artifacts but does not validate Python code itself.

### arch-linux.md

- No direct relationship. Verification Framework verifies Agent Pack files,
  not system health or diagnostics.

## Platform capability model

To implement this contract, a platform needs these minimum capabilities:

| Capability | Required for | Notes |
|---|---|---|
| File listing (`ls`, `find`) | Quick | Universal |
| SHA-256 hashing (`sha256sum`) | Quick, Standard, Certification | Universal |
| Byte comparison (`diff`, `cmp`) | Quick, Standard | Universal |
| Text search (`grep`) | Standard | Universal |
| Git read-only commands | Quick, Standard | Available where git is installed |
| `neural status` and `neural search` | Standard | Available where NeuralEngine is installed |
| Permission introspection | Standard | Platform-specific; varies by agent model |
| YAML frontmatter parsing | Quick, Standard | Universal via `sed` or equivalent |

### Unsupported capability handling

When a platform cannot provide a required capability, use one of:

- `NOT APPLICABLE` — the check is not relevant to this platform (e.g., git
  scope check on a platform that does not use git).
- `NOT SUPPORTED` — the platform cannot provide this capability. Document the
  limitation.
- `BLOCKED` — the platform cannot provide this capability and it prevents
  verification from completing.

Do not silently treat unsupported capabilities as passing. Document every
limitation.

### Platform permission models

Not all platforms expose identical native permission models (deny lists,
capability gating, sandboxing). A platform adapter must verify the
permissions it *can* inspect and document what it *cannot*.

## Evidence model

Accepted evidence types, in order of strength:

1. **SHA-256 hash** — proves byte-level identity of a file.
2. **Command output** — raw output from a verification command.
3. **Byte comparison result** — `diff` exit code or equivalent.
4. **Exact path** — confirms a file exists at the expected location.
5. **Review artifact** — a completed review file that itself contains evidence.
6. **Platform configuration excerpt** — relevant section of an agent or skill
   configuration file.
7. **Explicit support-status declaration** — a documented statement of
   platform capability or limitation.

Prose assertion alone is **not** evidence. "The file looks correct" is not
acceptable. "SHA-256 of opencode.json is `99b53948...`" is.

Every finding in a Standard Verification or Certification Report must cite at
least one evidence source from this model.

## Verdict criteria

### Quick Verification

| Verdict | Criteria |
|---|---|
| `PASS` | All mechanical checks passed. File count matches, all SHA-256 hashes match, no prohibited artifacts, git scope clean. |
| `FAIL` | Any mechanical check failed. At least one file missing, hash mismatch, prohibited artifact detected, or scope violation. |

### Standard Verification and Certification Report

| Verdict | Criteria |
|---|---|
| `PASS` | All applicable criteria SATISFIED. No findings of any severity. |
| `PASS WITH NOTES` | All applicable criteria SATISFIED. One or more non-blocking findings present (e.g., optional improvement recommended, minor formatting deviation, transient environment warning that resolved). |
| `BLOCKED` | Verification could not complete. Missing dependency, insufficient permissions, environment capacity failure (e.g., `/tmp` full), or NeuralEngine unavailable when required. |
| `FAIL` | One or more criteria NOT SATISFIED. At least one finding is a blocker (missing file, hash mismatch, contract violation, missing mandatory evidence). |

### Readiness score

A 0–100 readiness score is **optional** and **secondary**. It may supplement
a Certification Report but:

- Must not override the verdict.
- Must not hide blockers (a score of 95 with one blocker is still FAIL).
- Must document the calculation method if used.
- Should not be used as the primary decision signal.

## NeuralEngine boundary

The Verification Framework must:

- Run `neural status` at the start of every Standard Verification and
  Certification Report.
- Record the exact output.
- Decide whether `neural search` is required for the verification task.
- If search is used, record exact queries, returned record IDs, and provenance.
- Explain how retrieved knowledge affected the verification.
- Include a NeuralEngine usage section in every Certification Report.

The Verification Framework must **not**:

- Perform Brain writes.
- Promote records between lifecycle stages.
- Create, update, or evaluate Brain records.
- Require Brain availability for Quick Verification.

The Framework both **produces** its own NeuralEngine usage evidence and
**checks** that required NeuralEngine evidence is present in artifacts within
its scope.

## Read-only boundary

The Verification Framework is strictly read-only. It must **not**:

- Edit files.
- Format or reformat code or documentation.
- Apply fixes or corrections.
- Regenerate generated files.
- Mutate configuration.
- Commit or push.
- Perform Brain writes.
- Run destructive shell operations (`rm`, `mv`, `sed -i`, `chmod`, `chown`).

If verification detects drift, it **reports** the drift and **stops**. It does
not repair it. Drift correction is a separate task outside the scope of
verification.

## Extensibility

### Adding a new shared contract

1. Create the contract under `shared/`.
2. Update MANIFEST.md with the shared-to-platform mapping.
3. Add verification checks to Standard Verification for the new contract's
   mandatory rules and required structure.
4. Add the contract's exact-copy or body-equality mappings to Quick
   Verification.
5. Recompute the expected file count.

### Adding a new platform

1. Create the platform directory under `platforms/<name>/`.
2. Create the platform adapter files per the controlled-copy model.
3. Update MANIFEST.md with platform-specific mappings.
4. Add the platform's exact-copy and body-equality checks to Quick
   Verification.
5. Add the platform to the support matrix check in Standard Verification.
6. Document the platform's permission model for the permission audit.
7. Recompute the expected file count.

### Adding a new exact-copy mapping

1. Add the mapping to MANIFEST.md.
2. Add the SHA-256 comparison to Quick Verification for the new file pair.
3. Update the Certification Report SHA-256 table template.

### Adding a new verification criterion

1. Add the criterion to Standard Verification with a SATISFIED/NOT SATISFIED
   test.
2. Define the evidence standard for the criterion.
3. If the criterion is mechanical, add it to Quick Verification.
4. Update the Certification Report template.
5. Do not add criteria that overlap with existing contract responsibilities.

The rule is preserved: the shared contract defines *what* to verify. The
platform adapter defines *how*.

## Automation threshold

**Current (v0.2)**: Verification uses platform-native read-only commands
and controlled manual procedures. No generators, scripts, or automatic
installers are introduced.

**Future reassessment trigger**: Consider introducing generators or automated
verification when:

- The number of shared contracts exceeds 8.
- The number of supported platforms exceeds 3.
- The total Agent Pack file count exceeds 100.
- Manual verification takes more than 15 minutes per Standard run.

Until any of these triggers is reached, manual verification with platform-native
commands is appropriate and preferred over introducing a dependency on
generation or automation tooling.

## Required report formats

### Quick Verification result

```text
Quick Verification — <timestamp>

File count: <N> (expected <N>)
Exact-copy SHA-256: <N>/<N> PASS
Body equality: <N>/<N> PASS
Symlinks: 0
Scripts/generators/installers: 0
Git scope: clean / <N> files outside agent-pack/

Verdict: PASS | FAIL
```

### Standard Verification report

```text
# Standard Verification — <timestamp>

## Verdict
PASS | PASS WITH NOTES | BLOCKED | FAIL

## Quick prerequisite
Quick Verification: PASS (ran at <timestamp>)

## Scope
Agent Pack version <version>, commit <sha>, branch <branch>

## Findings
### SATISFIED
- <criterion>: <evidence reference>
...

### NOT SATISFIED
- <criterion>: <evidence reference>, <impact>
...

## NeuralEngine usage
- neural status: <result>
- Search decision: <used/not used, reason>
- Queries: <list or None>
- Results: <list or None>

## Blockers and deviations
None | <list>
```

### Certification Report

```text
# Certification Report — <timestamp>

## Verdict
PASS | PASS WITH NOTES | BLOCKED | FAIL

## Checkpoint
- Agent Pack version: <version>
- Git HEAD: <sha>
- Branch: <branch>
- Platform: <platform name>
- Verifier: <identity>

## Quick Verification summary
File count: <N>/<N>
SHA-256: <N>/<N> PASS
Body equality: <N>/<N> PASS
Artifact audit: clean

## SHA-256 and equality evidence
| File | Source | SHA-256 | Match |
|---|---|---|---|
| opencode.json | ~/.config/opencode/opencode.json | 99b539... | ✓ |
| ... | ... | ... | ... |

## Standard Verification findings
<per-criterion evidence>

## Platform capability summary
| Capability | Status |
|---|---|
| SHA-256 | AVAILABLE |
| Git | AVAILABLE |
| NeuralEngine | AVAILABLE |
| ... | ... |

## Support status
- OpenCode: Supported
- Codex: Placeholder
- Claude Code: Placeholder
- Antigravity: Placeholder

## NeuralEngine usage
- neural status: <output>
- Search decision: <used/not used>
- Queries: <list or None>
- Effect on work: <explanation>

## Blockers and deviations
None | <list>
```

Templates are platform-neutral. Platform adapters may adjust the format to
their native reporting conventions as long as all required sections are
present and evidence standards are met.
