from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(frozen=True)
class BuildPaths:
    root: Path

    @property
    def handbook(self) -> Path:
        return self.root / "handbook"

    @property
    def templates(self) -> Path:
        return self.root / "templates"

    @property
    def outputs(self) -> Path:
        return self.root / "outputs"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _render(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{ " + key + " }}", value)
    return rendered.rstrip() + "\n"


def _read_many(paths: list[Path]) -> list[str]:
    return [_read(path) for path in paths]


def _write_compilation(target: Path, title: str, sections: list[str]) -> None:
    target.write_text(
        f"# {title}\n\n" + "\n\n---\n\n".join(sections) + "\n",
        encoding="utf-8",
    )


def build(root: Path) -> list[Path]:
    paths = BuildPaths(root=root)
    values = {
        "constitution": _read(paths.handbook / "constitution/CONSTITUTION.md"),
        "architecture": _read(paths.handbook / "architecture/architecture.md"),
        "domain_chain": _read(paths.handbook / "domain/domain-chain.md"),
        "workflow": _read(paths.handbook / "workflow/development-workflow.md"),
        "validation": _read(paths.handbook / "workflow/validation.md"),
        "agent_policy": _read(paths.handbook / "agents/agent-policy.md"),
        "definition_of_done": _read(paths.handbook / "checklists/definition-of-done.md"),
        "review_checklist": _read(paths.handbook / "checklists/review.md"),
    }

    generated = paths.outputs / "generated"
    skill = paths.outputs / "claude-skill"
    generated.mkdir(parents=True, exist_ok=True)
    skill.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []

    skill_path = skill / "SKILL.md"
    skill_path.write_text(
        _render(_read(paths.templates / "SKILL.md.j2"), values),
        encoding="utf-8",
    )
    outputs.append(skill_path)

    agents_path = generated / "AGENTS.generated.md"
    agents_path.write_text(
        _render(_read(paths.templates / "AGENTS.generated.md.j2"), values),
        encoding="utf-8",
    )
    outputs.append(agents_path)

    for source_name, output_name in (
        ("codex-task.md", "codex-task-template.md"),
        ("deepseek-task.md", "deepseek-task-template.md"),
        ("review.md", "review-template.md"),
    ):
        target = generated / output_name
        shutil.copyfile(paths.templates / source_name, target)
        outputs.append(target)

    domain_files = [
        paths.handbook / "domain/observation.md",
        paths.handbook / "domain/experience.md",
        paths.handbook / "domain/knowledge.md",
        paths.handbook / "domain/playbook.md",
        paths.handbook / "domain/playbook-run.md",
        paths.handbook / "domain/playbook-evaluation.md",
        paths.handbook / "domain/evolution-proposal.md",
        paths.handbook / "domain/playbook-revision.md",
    ]

    application_files = [
        paths.handbook / "application/services.md",
        paths.handbook / "application/errors.md",
        paths.handbook / "ports/ports.md",
        paths.handbook / "ports/repository-ports.md",
        paths.handbook / "infrastructure/adapters.md",
        paths.handbook / "infrastructure/repositories.md",
        paths.handbook / "container/dependency-injection.md",
        paths.handbook / "container/lifecycle.md",
        paths.handbook / "patterns/add-application-service.md",
        paths.handbook / "patterns/add-repository.md",
        paths.handbook / "patterns/add-adapter.md",
        paths.handbook / "patterns/wire-container.md",
        paths.handbook / "antipatterns/fat-service.md",
        paths.handbook / "antipatterns/god-repository.md",
        paths.handbook / "antipatterns/service-locator.md",
        paths.handbook / "antipatterns/adapter-business-logic.md",
        paths.handbook / "checklists/application-service.md",
        paths.handbook / "checklists/repository.md",
        paths.handbook / "checklists/adapter.md",
        paths.handbook / "checklists/container.md",
        paths.handbook / "decisions/ADR-0005-constructor-injection.md",
        paths.handbook / "decisions/ADR-0006-port-minimalism.md",
        paths.handbook / "decisions/ADR-0007-adapter-boundaries.md",
    ]

    handbook_sections = [
        values["constitution"],
        values["architecture"],
        _read(paths.handbook / "architecture/responsibility-matrix.md"),
        values["domain_chain"],
        *_read_many(domain_files),
        *_read_many(application_files),
        values["workflow"],
        values["validation"],
        values["agent_policy"],
        _read(paths.handbook / "patterns/new-feature.md"),
        _read(paths.handbook / "patterns/bugfix.md"),
        values["definition_of_done"],
        values["review_checklist"],
        _read(paths.handbook / "checklists/domain-change.md"),
        _read(paths.handbook / "checklists/new-cli-command.md"),
        _read(paths.handbook / "decisions/ADR-0001-service-owned-navigation.md"),
        _read(paths.handbook / "decisions/ADR-0002-domain-chain.md"),
        _read(paths.handbook / "decisions/ADR-0003-agent-assignment.md"),
        _read(paths.handbook / "decisions/ADR-0004-review-artifacts.md"),
    ]
    handbook_path = generated / "HANDBOOK.md"
    _write_compilation(
        handbook_path,
        "NeuralEngine Engineering Handbook",
        handbook_sections,
    )
    outputs.append(handbook_path)

    decision_path = generated / "DECISION_ENGINE.md"
    _write_compilation(
        decision_path,
        "NeuralEngine Decision Engine",
        [
            _read(paths.handbook / "architecture/decision-engine.md"),
            _read(paths.handbook / "architecture/responsibility-matrix.md"),
            _read(paths.handbook / "checklists/domain-change.md"),
            _read(paths.handbook / "checklists/new-cli-command.md"),
            _read(paths.handbook / "checklists/application-service.md"),
            _read(paths.handbook / "checklists/repository.md"),
            _read(paths.handbook / "checklists/adapter.md"),
            _read(paths.handbook / "checklists/container.md"),
        ],
    )
    outputs.append(decision_path)

    application_path = generated / "APPLICATION_ARCHITECTURE.md"
    _write_compilation(
        application_path,
        "NeuralEngine Application Architecture",
        _read_many(application_files),
    )
    outputs.append(application_path)

    return outputs
