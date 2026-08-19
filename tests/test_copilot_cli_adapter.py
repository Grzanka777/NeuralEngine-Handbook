"""Drift and scope checks for the bounded Copilot CLI adapter."""

from pathlib import Path


def _source_root() -> Path:
    """Return the Handbook repository root."""
    return Path(__file__).resolve().parents[1]


def _copilot_root() -> Path:
    """Return the controlled Copilot CLI platform source directory."""
    return _source_root() / "agent-pack" / "platforms" / "copilot"


def _skill() -> Path:
    """Return the controlled Copilot CLI NeuralEngine skill projection."""
    return _copilot_root() / "skills" / "neuralengine" / "SKILL.md"


def _shared() -> Path:
    """Return the authoritative shared NeuralEngine contract."""
    return _source_root() / "agent-pack" / "shared" / "neuralengine.md"


def _body(content: str) -> str:
    """Return a skill body after its front matter."""
    lines = content.splitlines(keepends=True)
    assert lines and lines[0].strip() == "---"
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    assert closing is not None
    return "".join(lines[closing + 1 :])


class TestCopilotNeuralEngineAdapter:
    """Tests for the shared GitHub Copilot CLI and VS Code projection."""

    def test_expected_platform_paths(self) -> None:
        """The adapter contains only its README and one skill."""
        paths = sorted(
            path.relative_to(_copilot_root()).as_posix()
            for path in _copilot_root().rglob("*")
            if path.is_file()
        )
        assert paths == [
            "README.md",
            "skills/neuralengine/SKILL.md",
        ]

    def test_skill_has_required_frontmatter_only(self) -> None:
        """The provider adds only required name and description metadata."""
        lines = _skill().read_text(encoding="utf-8").splitlines()
        assert lines[0] == "---"
        closing = lines.index("---", 1)
        assert lines[1:closing] == [
            "name: neuralengine",
            "description: Use NeuralEngine as the durable project knowledge, decision, experience, and playbook layer for substantive repository, architecture, review, diagnostic, planning, and authorized Brain tasks.",
        ]
        assert "allowed-tools:" not in "\n".join(lines[1:closing])

    def test_skill_body_matches_shared_contract(self) -> None:
        """Copilot cannot silently diverge from the canonical semantic source."""
        assert _body(_skill().read_text(encoding="utf-8")) == _shared().read_text(encoding="utf-8")

    def test_no_extra_pointer_is_required(self) -> None:
        """Native skill discovery means no duplicate instruction pointer exists."""
        paths = {path.name for path in _copilot_root().iterdir()}
        assert paths == {"README.md", "skills"}

    def test_readme_describes_cli_and_vscode_reuse(self) -> None:
        """Documentation states the bounded host reuse and support boundary."""
        content = (_copilot_root() / "README.md").read_text(encoding="utf-8")
        assert "GitHub Copilot CLI and VS Code" in content
        assert ".github/skills/neuralengine/SKILL.md" in content
        assert "The existing skill is deliberately reused by both hosts" in content
        assert "No additional project instruction pointer" in content
        assert (
            "This bounded support covers GitHub Copilot CLI and GitHub Copilot in VS Code"
            in content
        )
        assert "No JetBrains, Visual Studio, GitHub.com Copilot Chat" in content

    def test_vscode_reuses_cli_skill_without_second_copy(self) -> None:
        """VS Code reuses the existing project skill without a semantic fork."""
        skill_paths = sorted(_copilot_root().rglob("SKILL.md"))
        assert skill_paths == [_skill()]
        content = (_copilot_root() / "README.md").read_text(encoding="utf-8")
        assert "there is no second semantic Copilot skill copy" in content
        assert "No additional project instruction pointer" in content

    def test_adapter_does_not_claim_provider_independent_authority(self) -> None:
        """The Copilot files preserve host permissions and publication boundaries."""
        content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in _copilot_root().rglob("*")
            if path.is_file()
        )
        for phrase in (
            "grants no additional",
            "Brain-write",
            "staging",
            "commit",
            "push",
            "publication",
        ):
            assert phrase in content
