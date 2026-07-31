import importlib.metadata
from pathlib import Path
import shutil

import neuralengine_handbook
from neuralengine_handbook.builder import build


def _copy_repo(tmp_path: Path) -> Path:
    source_root = Path(__file__).resolve().parents[1]
    work_root = tmp_path / "handbook"
    shutil.copytree(source_root, work_root)
    return work_root


def test_build_generates_expected_outputs(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    outputs = build(work_root)

    names = {path.name for path in outputs}
    assert "SKILL.md" in names
    assert "AGENTS.generated.md" in names
    assert "HANDBOOK.md" in names
    assert "DECISION_ENGINE.md" in names
    assert "APPLICATION_ARCHITECTURE.md" in names
    assert "codex-task-template.md" in names
    assert "deepseek-task-template.md" in names
    assert "review-template.md" in names


def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    assert "Observation" in skill
    assert "PlaybookRevision" in skill
    assert "PlaybookRevisionActivation" in skill
    assert "PlaybookRevisionApplication" in skill
    assert "Activation does not imply application" in skill
    assert "Application CLI commands do not" in skill
    assert "Playbook content mutation" in skill
    assert "# Decision Learning Architecture" in skill
    assert "These commands exist at commit `1b45beb`" in skill
    assert "neural decision add" in skill
    assert "neural decision list" in skill
    assert "neural decision show DECISION_UUID" in skill
    assert "neural decision accept DECISION_UUID" in skill
    assert "neural decision acceptance-history DECISION_UUID" in skill
    assert "neural decision action add DECISION_UUID" in skill
    assert "neural decision action-history DECISION_UUID" in skill
    assert "neural decision action-show ACTION_UUID" in skill
    assert "neural decision outcome add DECISION_UUID" in skill
    assert "neural decision outcome-history DECISION_UUID" in skill
    assert "neural decision outcome-show OUTCOME_UUID" in skill
    assert "neural decision outcome-summary DECISION_UUID" in skill
    assert "neural decision review add DECISION_UUID" in skill
    assert "neural decision review history DECISION_UUID" in skill
    assert "neural decision review show REVIEW_UUID" in skill
    assert "neural experience from-review REVIEW_UUID" in skill
    assert "neural decision state DECISION_UUID" in skill
    assert "DecisionOutcome foundation" in skill
    assert "DecisionReview` remains future-only" not in skill
    assert "DecisionReview does not" not in skill
    assert "immutable, append-only authorized interpretation" in skill
    assert "`sound`, `flawed`, `mixed`, or `inconclusive`" in skill
    assert "confidence accepts `low`, `medium`, or" in skill
    assert "`high`" in skill
    assert "DecisionReviewIdempotencyAmbiguityError" in skill
    assert "DecisionOutcomeIdempotencyAmbiguityError" in skill
    assert "DecisionReviewPromotionSourceStatement" in skill
    assert "kind is exactly `finding`" in skill
    assert "`candidate_lesson`" in skill
    assert '(decision_review_id, "review_experience_promotion", idempotency_key)' in skill
    assert "DecisionReviewPromotionIdempotencyConflictError" in skill
    assert "DecisionReviewPromotionIdempotencyAmbiguityError" in skill
    assert "CLI ordinals are positive and one-based" in skill
    assert "durable zero-based indexes" in skill
    assert "Old JSON without the field loads with `None`" in skill
    assert "fails closed without" in skill
    assert "Durable Playbook-scoped Knowledge use and Run feedback already exist" in skill
    assert "PlaybookEvaluation.run_id" in skill
    assert "DecisionAction.playbook_run_id?" in skill
    assert "PlaybookRun -> zero or one PlaybookRevision" in skill
    assert (
        "durable operational Knowledge use and feedback remain a separate future gap" not in skill
    )
    assert "No Consigliere integration exists" in skill
    assert "no automatic persistence, ingestion, or learning" in skill
    assert "same key + equivalent semantic payload" in skill
    assert '(decision_id, "decision_acceptance", idempotency_key)' in skill
    assert '(decision_id, "decision_action", idempotency_key)' in skill
    assert "another action may be recorded" in skill
    assert "different key + Decision already accepted" in skill
    assert "There is no persisted Evidence aggregate or Evidence repository" in skill
    assert "Do not add features" in skill


def test_generated_outputs_contain_neural_home_selection_contract(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill):
        assert "`NEURAL_HOME` is the sole public selector" in artifact
        assert 'Path.home() / ".neural"' in artifact
        assert "no failure path falls back to `~/.neural`" in artifact
        assert "all 15 default JSON record-store directories" in artifact
        assert "`neural status` is read-only" in artifact
        assert "user-managed portable Neural home is supported" in artifact
        assert (
            "`neural doctor` is the bounded, intrinsically read-only readiness companion"
            in artifact
        )
        assert "Selection`, `Home`, `Brain`, `Stores`, `Integrity`, `Manifest`," in artifact
        assert "A `READY` report exits" in artifact
        assert "`NOT READY` exits `1`" in artifact
        assert "NEURAL_HOME=/path/to/NeuralEngine-State neural doctor" in artifact
        assert "does not repair, initialize, migrate, back up, mount" in artifact

    assert "Explicit `directory=...` injection remains supported" in application
    assert "every default JSON repository in the graph" in application
    assert "invalid_configuration" in application
    assert "brain_unavailable" in application


def test_generated_outputs_preserve_run_revision_execution_provenance(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill):
        assert "PlaybookRun -> zero or one PlaybookRevision" in artifact
        assert "authority -> explicit Run caller" in artifact
        assert "revision_id=None" in artifact
        assert "Corrupt linked provenance fails closed" in artifact
        assert "neural run add --revision-id REVISION_UUID" in artifact
        assert "neural revision runs REVISION_UUID" in artifact
        assert "Run-to-PlaybookRevisionApplication binding" in artifact
        assert "automatic active-revision selection" in artifact
        assert "Run identifies a Playbook, not a PlaybookRevision" not in artifact

    assert "PlaybookRunReader.get_by_id()" in application
    assert "No failure path writes" in application
    assert "Old JSON without `revision_id` loads with `None`" in application


def test_handbook_contains_all_domain_entities(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    entities = [
        "Observation",
        "Experience",
        "Knowledge",
        "Playbook",
        "PlaybookRun",
        "PlaybookEvaluation",
        "EvolutionProposal",
        "PlaybookRevision",
        "PlaybookRevisionActivation",
        "PlaybookRevisionApplication",
        "DecisionOutcome",
        "DecisionReview",
    ]
    for entity in entities:
        assert f"# {entity}" in handbook
    assert "# DecisionReview-to-Experience Promotion" in handbook
    # Prove generated section order: DecisionReview precedes DecisionReview-to-Experience Promotion
    assert handbook.index("# DecisionReview\n") < handbook.index(
        "# DecisionReview-to-Experience Promotion\n"
    )


def test_handbook_preserves_revision_application_boundaries(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    assert "Activation does not imply application" in handbook
    assert "get_active_revision_for_playbook(playbook_id)" in handbook
    assert "no CLI apply command" in handbook
    assert "no PlaybookRevision materialization" in handbook
    assert "content_changed" in handbook


def test_decision_engine_contains_agent_and_repository_rules(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    decision_engine = (work_root / "outputs/generated/DECISION_ENGINE.md").read_text(
        encoding="utf-8"
    )
    assert "Use Codex GPT-5.5 medium" in decision_engine
    assert "DeepSeek is allowed only when all are true" in decision_engine
    assert "Do not add it to a repository" in decision_engine
    assert "# Decision Learning Architecture" in decision_engine
    assert "ADR-0008" in decision_engine


def test_handbook_contains_decision_review_experience_promotion_boundaries(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    assert "NeuralEngine source commit `0ffdda6bfdbadd5952c1066fddd303185939d643`" in handbook
    assert "neural decision add" in handbook
    assert "neural decision list" in handbook
    assert "neural decision show DECISION_UUID" in handbook
    assert "neural decision accept DECISION_UUID" in handbook
    assert "neural decision acceptance-history DECISION_UUID" in handbook
    assert "neural decision action add DECISION_UUID" in handbook
    assert "neural decision action-history DECISION_UUID" in handbook
    assert "neural decision action-show ACTION_UUID" in handbook
    assert "neural decision outcome add DECISION_UUID" in handbook
    assert "neural decision outcome-history DECISION_UUID" in handbook
    assert "neural decision outcome-show OUTCOME_UUID" in handbook
    assert "neural decision outcome-summary DECISION_UUID" in handbook
    assert "neural decision review add DECISION_UUID" in handbook
    assert "neural decision review history DECISION_UUID" in handbook
    assert "neural decision review show REVIEW_UUID" in handbook
    assert "neural experience from-review REVIEW_UUID" in handbook
    assert "neural decision state DECISION_UUID" in handbook
    assert "DecisionAcceptance" in handbook
    assert "DecisionAcceptance foundation" in handbook
    assert "Only one acceptance per Decision is allowed" in handbook
    assert "Decision without acceptance" in handbook
    assert "Decision with one valid acceptance" in handbook
    assert "DecisionReview" in handbook
    assert "# DecisionReview" in handbook
    assert "DecisionReview` remains future-only" not in handbook
    assert "DecisionReview does not. Records" not in handbook
    assert '(project_key, "decision", idempotency_key)' in handbook
    assert "same key + different semantic payload" in handbook
    assert '(decision_id, "decision_acceptance", idempotency_key)' in handbook
    assert "different key + Decision already accepted" in handbook
    assert "There is no persisted Evidence aggregate or Evidence repository" in handbook
    assert "DecisionAction" in handbook
    assert "## DecisionAction foundation" in handbook
    assert "DecisionLifecycleService` is the only canonical owner" in handbook
    assert "Decision with one valid acceptance and at least one valid action" in handbook
    assert "completed_at` means only" in handbook
    assert '(decision_id, "decision_action", idempotency_key)' in handbook
    assert "another action may be recorded" in handbook
    assert "PlaybookRun and Playbook currently expose no project_key" in handbook
    assert "DecisionOutcome" in handbook
    assert "DecisionOutcome foundation" in handbook
    assert "# DecisionOutcome" in handbook
    assert "`succeeded`, `failed`, `partial`, and `unknown`" in handbook
    assert '(decision_id, "decision_outcome", idempotency_key)' in handbook
    assert "DecisionOutcomeIdempotencyAmbiguityError" in handbook
    assert "another outcome may be recorded" in handbook
    assert "DecisionOutcomeSummary" in handbook
    assert "(validated_at, outcome.id)" in handbook
    assert "outcome_unknown" in handbook
    assert '(decision_id, "decision_review", idempotency_key)' in handbook
    assert "DecisionReviewIdempotencyAmbiguityError" in handbook
    assert "immutable, append-only authorized interpretation" in handbook
    assert "`sound`, `flawed`, `mixed`, or `inconclusive`" in handbook
    assert "confidence accepts `low`, `medium`, or" in handbook
    assert "`high`" in handbook
    assert "Action IDs are not persisted" in handbook
    assert "(reviewed_at, review.id)" in handbook
    assert "no `reviewed` state" in handbook
    assert "explicitly promoted Experience" in handbook
    assert "decision_review_promotion: DecisionReviewPromotion | None" in handbook
    assert "DecisionReviewPromotionSourceStatement" in handbook
    assert "finding | candidate_lesson" in handbook
    assert "CLI ordinals are positive and one-based" in handbook
    assert "durable zero-based indexes" in handbook
    assert '(decision_review_id, "review_experience_promotion", idempotency_key)' in handbook
    assert "DecisionReviewPromotionIdempotencyConflictError" in handbook
    assert "DecisionReviewPromotionIdempotencyAmbiguityError" in handbook
    assert "Old JSON without `decision_review_promotion` remains valid" in handbook
    assert "Missing or malformed provenance fails closed" in handbook
    assert "a promoted Experience is not Knowledge" in handbook
    assert "Durable Playbook-scoped Knowledge use and Run feedback already exist" in handbook
    assert "separate explicit Experience creation from DecisionReview" not in handbook
    assert "No Consigliere integration exists" in handbook
    assert "no automatic persistence, ingestion, or learning" in handbook
    assert "ADR-0008" in handbook
    assert "partially_successful" not in handbook
    assert "DecisionOutcome` and `DecisionReview` remain future-only" not in handbook


def test_application_architecture_contains_core_boundaries(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )
    assert "# Application Services" in application
    assert "# Ports" in application
    assert "# Repository Ports" in application
    assert "# Infrastructure Adapters" in application
    assert "# Dependency Injection and Container" in application
    assert "# Anti-pattern: God Repository" in application
    assert "DecisionReviewService.add()" in application
    assert "DecisionReviewRepository` is likewise limited" in application
    assert "JsonDecisionReviewRepository" in application
    assert "Container.decision_review_service()" in application
    assert "DecisionReviewIdempotencyAmbiguityError" in application
    assert "DecisionOutcomeIdempotencyAmbiguityError" in application
    assert "ExperienceService.add_from_decision_review(...)" in application
    assert "DecisionReviewPromotionIdempotencyConflictError" in application
    assert "DecisionReviewPromotionIdempotencyAmbiguityError" in application
    assert "ExperienceRepository` remains limited" in application
    assert "Old JSON without that field loads with `None`" in application
    assert "Container.experience_service()" in application


def test_application_architecture_includes_accepted_adrs(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )
    assert "ADR-0005" in application
    assert "ADR-0006" in application
    assert "ADR-0007" in application
    assert application.count("Status: Accepted") >= 3


def test_generated_outputs_preserve_knowledge_create_once_integrity(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill):
        assert "one Knowledge UUID binds to one complete modeled" in artifact
        assert "identical complete same-ID replay" in artifact
        assert "without rewriting existing bytes" in artifact
        assert "different same-ID payload conflicts without writing" in artifact
        assert "filename/request UUID" in artifact
        assert "mismatches fail visibly" in artifact
        assert "Direct filesystem mutation remains out-of-band corruption" in artifact
        assert "Valid old JSON remains readable" in artifact
        assert "not tamper-proof storage" in artifact
        assert "Knowledge versioning" in artifact
        assert "historical reconstruction" in artifact
        assert "payload snapshotting" in artifact

    assert "same-directory temporary file" in handbook
    assert "KnowledgePersistenceConflictError without modifying existing bytes" in handbook
    assert "filename or requested UUID differs from embedded" in handbook
    assert "Missing `get_by_id()` retains `None`" in handbook
    assert "stored for an ID is authoritative going forward" in handbook

    assert "The repository port owns create-once persistence semantics" in application
    assert "KnowledgeRepositoryError" in application
    assert "controlled exit-code-1 output" in application
    assert "no schema, path, or repository-method change" in application


def test_generated_outputs_preserve_playbook_revision_create_once_integrity(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill):
        assert "one Revision UUID binds to one complete validated modeled payload" in artifact
        assert "identical complete same-ID replay" in artifact
        assert "without rewriting the existing bytes" in artifact
        assert "PlaybookRevisionPersistenceConflictError" in artifact
        assert "PlaybookRevisionIdentityMismatchError" in artifact
        assert "Direct filesystem mutation remains out-of-band corruption" in artifact
        assert "not tamper-proof or cryptographically immutable" in artifact
        assert "pre-hardening" in artifact
        assert "payload history" in artifact
        assert "does not deeply freeze nested in-memory lists" in artifact
        assert "None snapshots the Revision payload" in artifact

    assert "same content under a new UUID remains a distinct valid Revision" in handbook
    assert "`PlaybookRevisionService.add()` continues to create a fresh UUID" in handbook
    assert "Activation or application state" in handbook
    assert "not required" in handbook
    assert "missing `get_by_id()` still returns `None`" in handbook

    assert "The `PlaybookRevisionRepository` port owns create-once persistence" in application
    assert "PlaybookRevisionRepositoryError" in application
    assert "non-replacing local filesystem publication operation" in application
    assert "no command, option, or normal success output changed" in application


def test_generated_outputs_preserve_playbook_run_create_once_integrity(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill):
        assert "One Run UUID binds to one complete validated modeled payload" in artifact
        assert "identical complete same-ID replay" in artifact
        assert "bytes, inode, size, mtime, and ctime" in artifact
        assert "PlaybookRunPersistenceConflictError" in artifact
        assert "PlaybookRunStoredDataError" in artifact
        assert "PlaybookRunIdentityMismatchError" in artifact
        assert "Repository replay is not ordinary creation" in artifact
        assert "generate a fresh Run UUID and timestamp" in artifact
        assert "Content equality under different generated UUIDs is not idempotent" in artifact
        assert (
            "Activation, application, timestamps, tags, and repository order never infer"
            in artifact
        )
        assert "No other record automatically creates a Run" in artifact
        assert "creates no automatic additional Run" in artifact
        assert "generalized crash-recovery" in artifact
        assert "direct filesystem mutation remains out-of-band" in artifact

    assert "Missing `get_by_id()` retains `None`" in handbook
    assert "Invalid records are not skipped" in handbook
    assert "same-directory temporary file" in handbook
    assert "Old JSON without `revision_id` loads with `None`" in handbook

    assert (
        "The `PlaybookRunRepository` port separately owns exact create-once persistence"
        in application
    )
    assert "PlaybookRunRepositoryError" in application
    assert "adds no dedicated PlaybookRun repository-error mapping to the CLI" in application
    assert "no schema, path, or repository-method change" in application


def test_generated_outputs_preserve_development_evidence_dogfooding_boundaries(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill):
        assert "frozen non-persisted candidate preview" in artifact
        assert "Preview is the default and performs no durable write" in artifact
        assert "explicit authority-confirmed apply" in artifact
        assert "prompt path + NeuralEngine + prompt SHA-256" in artifact
        assert "full commit SHA + NeuralEngine + Git tree" in artifact
        assert "Validation-tree strength is exactly one of" in artifact
        assert "replay identity is `NeuralEngine:<full commit SHA>`" in artifact
        assert "Apply is resumable, not transactional" in artifact
        assert "automatic Observation or Knowledge creation" in artifact
        assert "No persisted evidence or candidate aggregate" in artifact
        assert "GitHub or CI integration" in artifact
        assert "background ingestion" in artifact

    assert "DevelopmentEvidenceService" in application
    assert "DevelopmentEvidenceSource" in application
    assert "LocalDevelopmentEvidenceSource" in application
    assert "resumable but non-transactional" in application
    assert "adds no evidence or candidate repository port" in application


def test_generated_outputs_preserve_knowledge_experience_integrity_boundary(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    skill = (work_root / "outputs/claude-skill/SKILL.md").read_text(encoding="utf-8")
    decision_engine = (work_root / "outputs/generated/DECISION_ENGINE.md").read_text(
        encoding="utf-8"
    )
    application = (work_root / "outputs/generated/APPLICATION_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )

    for artifact in (handbook, skill, decision_engine):
        assert "ExperienceReader" in artifact
        assert "ExperienceService.get_by_id()" in artifact
        assert "neural knowledge from-experience EXPERIENCE_UUID" in artifact
        assert "neural experience knowledge" in artifact
        assert "read-only navigation" in artifact
        assert "Durable Playbook-scoped Knowledge use and Run feedback already exist" in artifact
        assert "PlaybookEvaluation.run_id" in artifact
        assert "DecisionAction.playbook_run_id?" in artifact
        assert (
            "durable operational Knowledge use and feedback remain a separate future gap"
            not in (artifact)
        )
        assert (
            "next controlled downstream step remains a separate explicit Experience-to-Knowledge"
        ) not in artifact

    assert "Knowledge.experience_ids" in handbook
    assert "does not validate unrelated Knowledge records" in handbook
    assert "Storing Knowledge proves explicit durable capture only" in handbook
    assert "including duplicates" in handbook

    assert "KnowledgeService does not depend on `ExperienceRepository`" in application
    assert "per stored relation, including duplicates" in application
    assert "does not inject a raw" in application
    assert "No repository port changed for this boundary" in application


def test_package_and_module_version_consistency() -> None:
    dist_version = importlib.metadata.version("neuralengine-handbook")
    assert dist_version == "0.4.1"
    assert neuralengine_handbook.__version__ == "0.4.1"
    assert dist_version == neuralengine_handbook.__version__
