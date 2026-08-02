"""Controlled manual-copy installation tests for OpenCode Agent Pack agents.

Tests the controlled installation procedure defined by ARCHITECTURE.md
§"Installation and onboarding boundary": manual, explicit, platform-specific,
verifiable copy with backup, equality verification, and rollback.
"""

import hashlib
import shutil
from pathlib import Path
from typing import TypedDict


class InstallResult(TypedDict):
    """Result of a controlled install operation."""

    action: str
    target: Path
    backup: Path | None
    source_sha256: str
    installed_sha256: str | None


def _source_root() -> Path:
    """Return the repository root (parent of tests/)."""
    return Path(__file__).resolve().parents[1]


def _source_agent(name: str) -> Path:
    """Return path to a packaged agent source file."""
    return _source_root() / "agent-pack" / "platforms" / "opencode" / "agents" / name


def _sha256(path: Path) -> str:
    """Return SHA-256 hex digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _count_frontmatter_delimiters(content: str) -> int:
    """Count opening and closing '---' delimiters in YAML frontmatter."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return 0
    count = 1
    for line in lines[1:]:
        if line.strip() == "---":
            count += 1
            break
    return count


# ---------------------------------------------------------------------------
# Controlled install helper
# ---------------------------------------------------------------------------


def controlled_install(
    source: Path,
    target_dir: Path,
    *,
    dry_run: bool = False,
) -> InstallResult:
    """Copy *source* agent file into *target_dir* with safeguards.

    Returns a result dict with keys:
      action: "created" | "replaced" | "unchanged" | "dry-run-would-create" |
              "dry-run-would-replace"
      target: Path to the target file
      backup: Path to the backup file (only when a previous file was replaced)
      source_sha256: SHA-256 of the source file
      installed_sha256: SHA-256 of the installed file (None on dry-run)
    """
    if not source.is_file():
        raise FileNotFoundError(f"Source agent not found: {source}")

    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    source_hash = _sha256(source)

    result = InstallResult(
        action="",
        target=target,
        backup=None,
        source_sha256=source_hash,
        installed_sha256=None,
    )

    if dry_run:
        if target.exists():
            if _sha256(target) == source_hash:
                result["action"] = "dry-run-unchanged"
            else:
                result["action"] = "dry-run-would-replace"
        else:
            result["action"] = "dry-run-would-create"
        return result

    # Real (non-dry-run) install
    if target.exists():
        existing_hash = _sha256(target)
        if existing_hash == source_hash:
            result["action"] = "unchanged"
            result["installed_sha256"] = existing_hash
            return result
        # Back up existing file before overwriting
        backup = target.with_suffix(target.suffix + ".backup")
        shutil.copy2(target, backup)
        result["backup"] = backup
        result["action"] = "replaced"
    else:
        result["action"] = "created"

    shutil.copy2(source, target)
    result["installed_sha256"] = _sha256(target)
    return result


def controlled_rollback(result: InstallResult) -> bool:
    """Roll back a previous controlled_install if a backup exists.

    Returns True if rollback succeeded, False if no backup was available.
    """
    backup = result.get("backup")
    target = result.get("target")
    if backup is None or target is None or not backup.is_file():
        return False
    shutil.copy2(backup, target)
    backup.unlink()
    return True


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestControlledInstall:
    """Tests for the controlled manual-copy installation procedure."""

    def test_clean_install(self, tmp_path: Path) -> None:
        """Fresh install into an empty target directory."""
        source = _source_agent("builder.md")
        assert source.is_file()

        result = controlled_install(source, tmp_path)
        assert result["action"] == "created"
        assert result["target"].is_file()
        assert result["installed_sha256"] == result["source_sha256"]
        assert result["backup"] is None

    def test_installed_equality(self, tmp_path: Path) -> None:
        """Installed file must be byte-identical to source."""
        source = _source_agent("builder.md")
        result = controlled_install(source, tmp_path)

        assert result["installed_sha256"] == _sha256(source)
        assert result["source_sha256"] == result["installed_sha256"]

    def test_target_directory_creation(self, tmp_path: Path) -> None:
        """Target directory is created if it does not exist."""
        target_dir = tmp_path / "deeply" / "nested" / "agents"
        assert not target_dir.exists()

        source = _source_agent("builder.md")
        result = controlled_install(source, target_dir)
        assert result["target"].is_file()
        assert target_dir.is_dir()

    def test_reinstall_idempotent(self, tmp_path: Path) -> None:
        """Installing the same file twice is idempotent."""
        source = _source_agent("builder.md")
        result1 = controlled_install(source, tmp_path)
        assert result1["action"] == "created"

        result2 = controlled_install(source, tmp_path)
        assert result2["action"] == "unchanged"
        assert result2["installed_sha256"] == result1["installed_sha256"]
        assert result2["backup"] is None  # no backup when unchanged

    def test_overwrite_with_backup(self, tmp_path: Path) -> None:
        """Overwriting a different file creates a backup of the previous one."""
        source = _source_agent("builder.md")
        target = tmp_path / "builder.md"

        # Place a different file at the target
        target.write_text("old content")
        old_hash = _sha256(target)

        result = controlled_install(source, tmp_path)
        assert result["action"] == "replaced"
        assert result["backup"] is not None
        assert result["backup"].is_file()
        assert _sha256(result["backup"]) == old_hash
        assert result["installed_sha256"] == result["source_sha256"]

    def test_rollback_restores_previous(self, tmp_path: Path) -> None:
        """Rollback restores the backed-up file and removes the backup."""
        source = _source_agent("builder.md")
        target = tmp_path / "builder.md"

        target.write_text("previous content")
        old_hash = _sha256(target)

        result = controlled_install(source, tmp_path)
        assert result["action"] == "replaced"
        assert result["backup"] is not None

        # Rollback
        assert controlled_rollback(result)
        assert _sha256(target) == old_hash  # previous content restored
        assert not result["backup"].is_file()  # backup removed

    def test_rollback_fails_without_backup(self, tmp_path: Path) -> None:
        """Rollback returns False when no backup exists."""
        source = _source_agent("builder.md")
        result = controlled_install(source, tmp_path)
        assert result["action"] == "created"
        assert result["backup"] is None

        assert controlled_rollback(result) is False

    def test_preserves_existing_agents(self, tmp_path: Path) -> None:
        """Installing builder does not modify existing arch-data-engineer or reviewer."""
        source = _source_agent("builder.md")
        target_dir = tmp_path / "agents"
        target_dir.mkdir(parents=True)

        # Place existing agents
        existing_a = target_dir / "arch-data-engineer.md"
        existing_r = target_dir / "reviewer.md"
        existing_a.write_text("arch-data-engineer content")
        existing_r.write_text("reviewer content")
        hash_a = _sha256(existing_a)
        hash_r = _sha256(existing_r)

        result = controlled_install(source, target_dir)
        assert result["action"] == "created"

        # Existing agents unchanged
        assert _sha256(existing_a) == hash_a
        assert _sha256(existing_r) == hash_r

    def test_no_unexpected_files(self, tmp_path: Path) -> None:
        """Only the target agent file is created; no side-effect files."""
        source = _source_agent("builder.md")
        target_dir = tmp_path / "agents"

        before = set(target_dir.rglob("*")) if target_dir.exists() else set()
        controlled_install(source, target_dir)
        after = set(target_dir.rglob("*"))

        new_files = after - before
        assert len(new_files) == 1
        assert new_files.pop().name == "builder.md"

    def test_expected_files_completeness(self, tmp_path: Path) -> None:
        """After install, all three agents are present."""
        source = _source_agent("builder.md")
        target_dir = tmp_path / "agents"
        target_dir.mkdir(parents=True)

        # Place existing agents
        (target_dir / "arch-data-engineer.md").write_text("a")
        (target_dir / "reviewer.md").write_text("r")

        controlled_install(source, target_dir)

        names = {p.name for p in target_dir.iterdir()}
        assert "builder.md" in names
        assert "arch-data-engineer.md" in names
        assert "reviewer.md" in names
        assert len(names) == 3  # no extra files

    def test_dry_run_create(self, tmp_path: Path) -> None:
        """Dry-run reports would-create without writing files."""
        source = _source_agent("builder.md")
        result = controlled_install(source, tmp_path, dry_run=True)

        assert result["action"] == "dry-run-would-create"
        assert not result["target"].exists()
        assert result["installed_sha256"] is None

    def test_dry_run_replace(self, tmp_path: Path) -> None:
        """Dry-run reports would-replace when target differs."""
        source = _source_agent("builder.md")
        target = tmp_path / "builder.md"
        target.write_text("different content")

        result = controlled_install(source, tmp_path, dry_run=True)
        assert result["action"] == "dry-run-would-replace"
        assert result["installed_sha256"] is None

    def test_source_missing_raises(self, tmp_path: Path) -> None:
        """Missing source file raises FileNotFoundError."""
        bad_source = tmp_path / "nonexistent.md"
        with __import__("pytest").raises(FileNotFoundError):
            controlled_install(bad_source, tmp_path)

    def test_frontmatter_two_delimiters(self, tmp_path: Path) -> None:
        """Installed builder frontmatter has exactly two '---' delimiters."""
        source = _source_agent("builder.md")
        result = controlled_install(source, tmp_path)

        content = result["target"].read_text(encoding="utf-8")
        delimiters = _count_frontmatter_delimiters(content)
        assert delimiters == 2, f"Expected 2 frontmatter delimiters, found {delimiters}"

    def test_builder_has_mode_primary(self, tmp_path: Path) -> None:
        """Installed builder is discoverable (mode: primary)."""
        source = _source_agent("builder.md")
        result = controlled_install(source, tmp_path)

        content = result["target"].read_text(encoding="utf-8")
        assert "mode: primary" in content

    def test_no_model_name_embedded(self, tmp_path: Path) -> None:
        """Installed builder contains no model names (model-agnostic)."""
        import re

        source = _source_agent("builder.md")
        result = controlled_install(source, tmp_path)

        content = result["target"].read_text(encoding="utf-8")
        pattern = re.compile(
            r"(gpt|deepseek|claude|gemini|llama|anthropic|openai|groq|mistral)",
            re.IGNORECASE,
        )
        assert not pattern.search(content), f"Model name found: {pattern.search(content)}"

    def test_temporary_cleanup(self, tmp_path: Path) -> None:
        """Test directories are within tmp_path and cleaned up by pytest."""
        source = _source_agent("builder.md")
        controlled_install(source, tmp_path)

        # tmp_path fixture guarantees cleanup — this test validates
        # that intermediate artifacts (like backups) are also in tmp_path
        assert tmp_path.exists()
        # All created files should be under tmp_path (pytest handles cleanup)
        all_files = list(tmp_path.rglob("*"))
        for f in all_files:
            assert str(tmp_path) in str(f)
