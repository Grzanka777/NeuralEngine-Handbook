# NeuralEngine Agent Pack Architecture

## Why Agent Pack exists

The NeuralEngine Agent Pack extends `NeuralEngine-Handbook` with agent guidance that agents can
use across platforms. Without it, each agent platform would require independent,
potentially divergent copies of the same workflows. The Agent Pack defines a
single authoritative source for shared workflow contracts and a controlled
mechanism for adapting them to each platform.

## Role within NeuralEngine-Handbook

The Agent Pack is a component of `NeuralEngine-Handbook`, not a separate
repository or product. It lives under `agent-pack/` and follows the same
governance rules as the rest of the Handbook:

- `handbook/` and `templates/` are source files.
- `outputs/` are generated files.
- `agent-pack/` is a source directory that extends the Handbook with
  platform-agnostic agent contracts and platform-specific adapters.

The Agent Pack does not modify NeuralEngine runtime behavior, Brain persistence,
schemas, migrations, user data, or public APIs.

## Architectural boundaries

```
NeuralEngine-Handbook/
├── agent-pack/                     # This component
│   ├── shared/                     # Authoritative shared contracts
│   │   ├── neuralengine.md
│   │   ├── repository-review.md
│   │   ├── python-validation.md
│   │   ├── arch-linux.md
│   │   └── verification.md
│   └── platforms/                  # Platform adapters (controlled copies)
│       ├── opencode/               # OpenCode reference implementation
│       │   ├── opencode.json
│       │   ├── neuralengine-usage.md
│       │   ├── agents/
│       │   ├── skills/
│       │   └── verification-permissions.md
│       ├── codex/                  # Placeholder (v1 roadmap)
│       ├── claude/                 # Placeholder (v1 roadmap)
│       └── antigravity/            # Placeholder (v1 roadmap)
```

Boundaries:

- `shared/` contains the authoritative contract text. No platform logic,
  configuration, or adapter code belongs here.
- `platforms/<name>/` contains platform-specific files. Each platform adapter is
  a controlled copy of active configuration, not an independent source of truth.
- `DECISIONS/` contains Architecture Decision Records (ADRs) for binding
  architectural choices. See
  [DECISIONS/verification-framework-architecture.md](DECISIONS/verification-framework-architecture.md)
  for the Verification Framework decision.
- The Agent Pack does not reach outside `agent-pack/` to modify files.
- The Agent Pack does not modify `~/.config/opencode/` or any other installed
  configuration. Installation is always manual and explicit.

## Architecture Freeze

The Architecture Freeze for v1.0 is recorded at:

```text
agent-pack/DECISIONS/architecture-freeze-v1.0.md
```

It freezes the five shared contracts, the verification hierarchy, the Adapter
API, the release workflow, and the v1.0 platform scope (OpenCode + Codex CLI).
Changes to frozen elements require an Architecture Change Proposal.

The platform capability matrix is at:

```text
agent-pack/CAPABILITY_MATRIX.md
```

## Source-of-truth rules

1. The `shared/` files are the single source of truth for workflow contract
   content.
2. Platform-specific copies under `platforms/` are derived from the active
   platform configuration at the time of copy. They must remain byte-equal
   (for exact copies) or semantically equivalent (for merged sources) to their
   shared origin.
3. Platform-specific configuration files that have no shared equivalent
   (e.g., `opencode.json`, `agents/reviewer.md`) are themselves the source of
   truth for that platform.
4. The active `~/.config/opencode/` directory is the runtime authority.
   Agent Pack copies are a snapshot, not a live reference.

## Relationship between `shared/` and `platforms/`

| Direction | Rule |
|---|---|
| Authoritative source → platform | `shared/` defines the contract. Platform adapters derive from it. |
| Platform → authoritative source | Never. A platform adapter is not a source of truth. |
| Equality requirement | Exact-copy files must be SHA-256 byte-equal to the active configuration source. Skill-body files must be byte-equal after YAML frontmatter removal. Merged sources are not byte-equal by design but must preserve all mandatory rules. |
| Drift | Detected during verification. Resolved by updating the platform copy from the authoritative source, never the reverse. |

## Controlled-copy synchronization

The current synchronization model is manual and explicit:

1. Edit the authoritative `shared/` source.
2. Update the controlled platform copy to match.
3. Verify equality or semantic equivalence.
4. Do not edit a platform copy independently.

The Agent Pack does not currently include generators, synchronization scripts,
watch mechanisms, or automatic installers. Future versions may introduce
generators or include mechanisms if manual drift becomes a maintenance burden.

## Platform-specific responsibility

Each platform adapter is responsible for:

- Mapping shared contracts to its native configuration format.
- Preserving the substantive body of each contract.
- Defining permissions appropriate for the platform's security model.
- Documenting limitations where full contract fidelity is not achievable.
- Declaring its support status (supported, placeholder, unsupported).

The Agent Pack does not force feature parity across platforms. A platform
adapter may omit a contract only if it is not applicable to that platform's
capability model.

## Contract ownership

| Contract | Owner | Last updated |
|---|---|---|
| `shared/neuralengine.md` | NeuralEngine global policy + NeuralEngine skill | v0.1.0 |
| `shared/repository-review.md` | repository-review skill | v0.1.0 |
| `shared/python-validation.md` | python-project-validation skill | v0.1.0 |
| `shared/arch-linux.md` | arch-linux-diagnostics skill | v0.1.0 |
| `shared/verification.md` | Verification Framework (new in v0.2.0) | v0.2.0 |

Contracts are owned by their originating source. The Agent Pack copies them;
it does not author them independently.

## Lifecycle of a shared-contract change

1. The originating source (global instruction or skill body) is updated.
2. The corresponding `shared/` contract is updated to match.
3. Every platform adapter that copies that contract is updated.
4. Equality or semantic equivalence is verified for each platform.
5. The MANIFEST and VERSION are updated if the change is material.
6. A review confirms the change is complete and correct.

## Lifecycle of a platform-adapter change

1. A platform adapter is created or updated to reflect the current shared
   contracts.
2. Equality or semantic equivalence is verified.
3. Platform-specific permissions are reviewed.
4. The MANIFEST mapping is updated.
5. The support matrix in README is updated.
6. A review confirms the adapter is complete and correct.

## Rules for adding a new shared contract

1. The contract must have a well-defined purpose, scope, and exclusions.
2. The originating source must exist (global instruction, skill, or
   authoritative document).
3. The contract must be added to `shared/` with a clear filename.
4. The MANIFEST mapping must be updated.
5. Every supported platform adapter must be updated or a documented exclusion
   provided.
6. A review must confirm the contract is complete and correctly copied.

## Rules for adding a new platform

1. The platform must have a configuration format capable of representing the
   shared contracts or a documented limitation explaining why it cannot.
2. A `platforms/<name>/` directory must be created with the required adapter
   files.
3. The MANIFEST mapping must be updated.
4. The support matrix in README must be updated.
5. Permissions understandable to the platform must be defined.
6. A review must confirm the adapter is complete and correctly mapped.
7. If the platform cannot support a contract, a documented placeholder is
   acceptable.

## Compatibility guarantees

- **v0.x**: No compatibility guarantee. Contracts, mappings, and platform
  support may change without notice.
- **v1.0**: The four shared contracts are stable. A contract may be extended
  with backward-compatible additions but not removed or substantively rewritten
  without a major version increment.
- Platform-specific configuration files are versioned with the pack but are
  not independently versioned.

## Versioning rules

- `VERSION` contains the current Agent Pack version.
- The version follows the `MAJOR.MINOR.PATCH` convention:
  - **MAJOR**: Contract removal, substantive rewrite, or platform removal.
  - **MINOR**: New contract, new platform, or new verification capability.
  - **PATCH**: Correction, formatting, or non-substantive update.
- Pre-v1.0, the convention is `0.MINOR.PATCH`.
- The version is the single source of truth for the Agent Pack release.

## Review and verification expectations

Every Agent Pack change must be reviewed:

- **Implementation review**: Confirms the change matches the task contract.
- **Independent review**: Confirms correctness, equality, and scope independently
  of the implementation review.
- **Equality/hash verification**: Confirms byte-level integrity of exact-copy
  files.
- **Repository validation**: Confirms the Handbook test suite passes.
- **Scope audit**: Confirms no files outside `agent-pack/` were modified.

Reviews must not rely on the implementation review as proof. Each review is
independent.

## Installation and onboarding boundary

The Agent Pack does not install itself. Installation is always:

1. Manual.
2. Explicit.
3. Platform-specific (the user copies files to the target agent configuration
   directory).
4. Verifiable (the user runs verification after installation).

The Agent Pack defines what to install. It does not automate the installation.

## Relationship with NeuralEngine Brain

- The Agent Pack includes NeuralEngine usage instructions as a shared contract
  and platform-specific instruction file.
- The Agent Pack does not perform Brain reads or writes automatically.
- The Agent Pack does not depend on Brain availability for structural integrity.
- Verification of the Agent Pack may use `neural status` and `neural search`
  as part of read-only inspection but never writes to the Brain without
  explicit user authorization.

## Brain read/write authorization boundary

| Operation | Allowed without authorization | Requires authorization |
|---|---|---|
| `neural status` | Yes | — |
| `neural search` | Yes | — |
| Reading record details | Yes | — |
| Inspecting provenance | Yes | — |
| Creating a record | — | Yes |
| Updating a record | — | Yes |
| Promoting a record | — | Yes |
| Creating a PlaybookRun | — | Yes |
| Any lifecycle transition | — | Yes |

The Agent Pack never performs Brain writes automatically. Any write requires
preview and explicit user authorization under the global NeuralEngine policy.

## Explicit exclusions

The Agent Pack does not:

- Modify NeuralEngine runtime behavior.
- Modify Brain persistence, schemas, or data.
- Modify active OpenCode configuration under `~/.config/opencode/`.
- Create symlinks, scripts, generators, or wrapper layers.
- Include automatic installers or synchronization tools in the current
  architecture.
- Automatically commit or push repository changes.
- Automatically perform Brain writes.
- Create a separate product lifecycle independent of NeuralEngine-Handbook.
- Introduce a new source-of-truth layer above or beside the shared contracts.

## Operating assumptions

- One maintainer.
- A small number of platforms (currently one supported, three planned).
- Manual synchronization is acceptable for the current scale.
- Verification is explicit, not continuous.
- Drift is a manageable risk at this scale; generators or include mechanisms may
  be introduced later if the number of platforms or contracts grows.
