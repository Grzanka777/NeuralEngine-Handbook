"""Drift and scope checks for the bounded Claude Code adapter."""

from pathlib import Path


def _source_root() -> Path:
    """Return the Handbook repository root."""
    return Path(__file__).resolve().parents[1]


def _claude_root() -> Path:
    """Return the controlled Claude platform source directory."""
    return _source_root() / "agent-pack" / "platforms" / "claude"


def _skill() -> Path:
    """Return the controlled Claude NeuralEngine skill projection."""
    return _claude_root() / "skills" / "neuralengine" / "SKILL.md"


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


class TestClaudeNeuralEngineAdapter:
    """Tests for the single Claude Code CLI/Desktop Code projection."""

    def test_expected_platform_paths(self) -> None:
        """The adapter contains only its pointer, README, and one skill."""
        paths = sorted(
            path.relative_to(_claude_root()).as_posix()
            for path in _claude_root().rglob("*")
            if path.is_file()
        )
        assert paths == [
            "CLAUDE.md",
            "README.md",
            "skills/neuralengine/SKILL.md",
        ]

    def test_skill_has_only_required_frontmatter(self) -> None:
        """The provider adds only the required Agent Skills metadata."""
        lines = _skill().read_text(encoding="utf-8").splitlines()
        assert lines[0] == "---"
        closing = lines.index("---", 1)
        assert lines[1:closing] == [
            "name: neuralengine",
            "description: Use NeuralEngine as the durable project knowledge, decision, experience, and playbook layer for substantive repository, architecture, review, diagnostic, planning, and authorized Brain tasks.",
        ]

    def test_skill_body_matches_shared_contract(self) -> None:
        """Claude cannot silently diverge from the canonical semantic source."""
        assert _body(_skill().read_text(encoding="utf-8")) == _shared().read_text(encoding="utf-8")

    def test_pointer_is_minimal_and_canonical(self) -> None:
        """The project pointer refers to the skill without duplicating policy."""
        content = (_claude_root() / "CLAUDE.md").read_text(encoding="utf-8")
        assert ".claude/skills/neuralengine/SKILL.md" in content
        assert "agent-pack/shared/neuralengine.md" in content
        assert "does not duplicate or redefine that contract" in content
        assert "## Authority model" not in content
        assert "neural knowledge search" not in content
        assert "Brain-write" not in content

    def test_readme_describes_cli_desktop_code_boundary(self) -> None:
        """Documentation states the bounded shared CLI/Desktop Code boundary."""
        content = (_claude_root() / "README.md").read_text(encoding="utf-8")
        assert "Claude Code CLI and the" in content
        assert ".claude/skills/<name>/SKILL.md" in content
        assert "project skill is shared by Claude Code CLI" in content
        assert "same underlying engine" in content
        assert "AGENTS.md is not natively consumed" in content
        assert "No automatic installation or Brain write is performed." in content

    def test_adapter_does_not_claim_provider_independent_authority(self) -> None:
        """The Claude files preserve host permissions and publication boundaries."""
        content = "\n".join(
            path.read_text(encoding="utf-8") for path in _claude_root().rglob("*") if path.is_file()
        )
        for phrase in (
            "no additional read",
            "Brain-write",
            "staging",
            "commit",
            "push",
            "publication",
        ):
            assert phrase in content
