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
    assert "These commands exist at commit `7724342`" in skill
    assert "neural decision add" in skill
    assert "neural decision list" in skill
    assert "neural decision show DECISION_UUID" in skill
    assert "DecisionAcceptance foundation" in skill
    assert "future-only records" in skill
    assert "No Consigliere integration exists" in skill
    assert "no automatic persistence, ingestion, or learning exists" in skill
    assert "same key + equivalent semantic payload" in skill
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


def test_handbook_contains_decision_foundation_and_future_boundaries(tmp_path: Path) -> None:
    work_root = _copy_repo(tmp_path)
    build(work_root)

    handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
    assert "NeuralEngine source commit `7724342` implements the Decision foundation" in handbook
    assert "neural decision add" in handbook
    assert "neural decision list" in handbook
    assert "neural decision show DECISION_UUID" in handbook
    assert "DecisionAcceptance" in handbook
    assert "DecisionReview" in handbook
    assert "future-only records" in handbook
    assert '(project_key, "decision", idempotency_key)' in handbook
    assert "same key + different semantic payload" in handbook
    assert "There is no Evidence repository, service, or CLI" in handbook
    assert "No Consigliere integration exists" in handbook
    assert "no automatic persistence, ingestion, or learning exists" in handbook
    assert "ADR-0008" in handbook


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
