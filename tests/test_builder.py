from pathlib import Path
import shutil

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
    assert "These commands exist at commit `910f481e`" in skill
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
    assert "No Consigliere integration exists" in skill
    assert "no automatic persistence, ingestion, or learning" in skill
    assert "same key + equivalent semantic payload" in skill
    assert '(decision_id, "decision_acceptance", idempotency_key)' in skill
    assert '(decision_id, "decision_action", idempotency_key)' in skill
    assert "another action may be recorded" in skill
    assert "different key + Decision already accepted" in skill
    assert "There is no Evidence repository, service, or CLI" in skill
    assert "Do not add features" in skill


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


def test_handbook_contains_decision_review_lifecycle_and_learning_boundaries(
    tmp_path: Path,
) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    assert "NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f`" in handbook
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
    assert "There is no Evidence repository, service, or CLI" in handbook
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
    assert "explicit Experience creation" in handbook
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
