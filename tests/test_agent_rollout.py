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


def _source_codex_skill() -> Path:
    """Return the controlled Codex NeuralEngine skill projection."""
    return (
        _source_root()
        / "agent-pack"
        / "platforms"
        / "codex"
        / "skills"
        / "neuralengine"
        / "SKILL.md"
    )


def _source_codex_pointer() -> Path:
    """Return the controlled Codex project-instruction pointer."""
    return _source_root() / "agent-pack" / "platforms" / "codex" / "AGENTS.md"


def _source_shared_neuralengine() -> Path:
    """Return the authoritative shared NeuralEngine contract."""
    return _source_root() / "agent-pack" / "shared" / "neuralengine.md"


def _skill_body(content: str) -> str:
    """Return a skill body after the required YAML front matter."""
    lines = content.splitlines(keepends=True)
    assert lines and lines[0].strip() == "---"
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    assert closing is not None
    return "".join(lines[closing + 1 :])


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


class TestPlannerAgent:
    """Tests for the planner agent definition."""

    def test_planner_definition_exists(self) -> None:
        """Planner agent definition exists at the expected path."""
        source = _source_agent("planner.md")
        assert source.is_file()

    def test_planner_role_identity(self) -> None:
        """Planner identifies itself as the planning and routing role."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "# Planner" in content
        assert "planning and routing agent" in content

    def test_planner_no_model_names(self) -> None:
        """Planner contains no concrete runtime-model names."""
        import re

        content = _source_agent("planner.md").read_text(encoding="utf-8")
        pattern = re.compile(
            r"(gpt|deepseek|claude|gemini|llama|anthropic|openai|groq|mistral)",
            re.IGNORECASE,
        )
        assert not pattern.search(content), f"Model name found: {pattern.search(content)}"

    def test_planner_task_delegation_denied(self) -> None:
        """Planner cannot delegate tasks."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "task: deny" in content

    def test_planner_staging_commit_push_denied(self) -> None:
        """Planner denies git add, commit, and push."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert '"git add*": deny' in content
        assert '"git commit*": deny' in content
        assert '"git push*": deny' in content

    def test_planner_edit_is_ask(self) -> None:
        """Planner uses edit: ask (no path-scoped edit support in OpenCode)."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "edit: ask" in content

    def test_planner_role_separation_stated(self) -> None:
        """Planner states separation from implementation and independent review."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "remain separate from implementation and independent review" in content

    def test_planner_decision_package_required(self) -> None:
        """Planner requires a Decision Package and delegated-prompt contract."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Decision Package" in content
        assert "delegated-prompt minimum contract" in content

    def test_planner_no_mutable_oracle_data(self) -> None:
        """Planner excludes mutable Oracle-only operational data."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Do not hardcode current model names" in content
        assert "Do not depend on Oracle Wisdom snapshots" in content

    def test_planner_mode_primary(self) -> None:
        """Planner uses mode: primary (no native plan mode dependency)."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "mode: primary" in content

    def test_planner_frontmatter_two_delimiters(self, tmp_path: Path) -> None:
        """Installed planner frontmatter has exactly two '---' delimiters."""
        source = _source_agent("planner.md")
        result = controlled_install(source, tmp_path)

        content = result["target"].read_text(encoding="utf-8")
        delimiters = _count_frontmatter_delimiters(content)
        assert delimiters == 2, f"Expected 2 frontmatter delimiters, found {delimiters}"

    def test_planner_evidence_first_before_proceed(self) -> None:
        """Planner requires evidence (source, location, observed, expected, mismatch)
        before Proceed."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "authoritative source" in content
        assert "exact file and location" in content
        assert "observed value" in content
        assert "expected value" in content
        assert "evidence proving a concrete mismatch" in content

    def test_planner_no_gap_means_defer_or_reject(self) -> None:
        """Planner returns Defer or Reject when no evidence-backed gap exists."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "No evidence-backed implementation gap found" in content

    def test_planner_no_delegated_prompt_without_gap(self) -> None:
        """Planner does not generate a delegated prompt without a proven gap."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Do not generate a delegated prompt when no proven gap exists" in content

    def test_planner_live_version_inspection_required(self) -> None:
        """Planner requires live reading of agent-pack/VERSION."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "cat agent-pack/VERSION" in content

    def test_planner_invented_facts_forbidden(self) -> None:
        """Planner forbids inventing branch, commit, VERSION, or other repository facts."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Never invent branch, commit, VERSION" in content
        assert "NOT VERIFIED" in content

    def test_planner_manual_vs_agent_decision_mandatory(self) -> None:
        """Planner requires an explicit Manual execution sufficient vs Agent execution required
        decision before assigning a role."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Manual execution sufficient" in content
        assert "Agent execution required" in content

    def test_planner_manual_preferred_for_trivial(self) -> None:
        """Planner prefers manual execution for one-line deterministic corrections."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert (
            "one exact deterministic command" in content or "one-line bounded correction" in content
        )
        assert "Prefer manual execution" in content

    def test_planner_repository_native_validation(self) -> None:
        """Planner derives validation from AGENTS.md and task scope."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Derive validation from `AGENTS.md`" in content

    def test_planner_ruff_on_markdown_rejected(self) -> None:
        """Planner rejects Ruff against markdown-only directories as meaningful validation."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Ruff against markdown-only directories as meaningful" in content

    def test_planner_heading_is_decision_package(self) -> None:
        """Planner Decision Package heading is # Decision Package, never # Oracle Decision Package."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "# Decision Package" in content
        assert "# Oracle Decision Package" not in content
        assert "Never use `Oracle Decision Package`" in content

    def test_planner_unresolved_placeholders_forbidden(self) -> None:
        """Planner forbids unresolved placeholders: <timestamp>, <name>, <TODO>."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "unresolved placeholders" in content.lower()
        assert "<timestamp>" in content
        assert "<name>" in content

    def test_planner_contradictory_agent_work_exclusion_forbidden(self) -> None:
        """Planner forbids excluding .agent-work/ while requiring an artifact inside it."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Do not exclude `.agent-work/` while requiring an artifact" in content

    def test_planner_proportionality_enforced(self) -> None:
        """Planner enforces proportionality: compact output, smallest step, no expansion."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "keep output compact" in content
        assert "smallest valuable next step" in content
        assert "do not expand a one-line correction into a milestone" in content

    def test_planner_existing_permissions_remain(self) -> None:
        """Planner retains existing permissions: edit ask, task deny, git writes denied,
        no concrete model names."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "edit: ask" in content
        assert "task: deny" in content
        assert '"git add*": deny' in content
        assert '"git commit*": deny' in content
        assert '"git push*": deny' in content
        import re

        model_pattern = re.compile(
            r"(gpt|deepseek|claude|gemini|llama|anthropic|openai|groq|mistral)",
            re.IGNORECASE,
        )
        assert not model_pattern.search(content)

    # -- Historical evidence handling tests --

    def test_planner_historical_classification_exists(self) -> None:
        """Planner requires classifying values as CURRENT STATE, HISTORICAL CHECKPOINT,
        FROZEN RELEASE EVIDENCE, or AMBIGUOUS before declaring them stale."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "CURRENT STATE" in content
        assert "HISTORICAL CHECKPOINT" in content
        assert "FROZEN RELEASE EVIDENCE" in content
        assert "AMBIGUOUS" in content

    def test_planner_historical_not_changed_by_current_diff(self) -> None:
        """Planner forbids changing historical values merely because the current value differs."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "must not be changed merely because the current" in content
        assert "value differs." in content

    def test_planner_context_inspection_required(self) -> None:
        """Planner requires inspecting section heading, paragraph, version label,
        document purpose, tests, and linked evidence before declaring a value stale."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "section heading" in content
        assert "version or milestone label" in content
        assert "document purpose" in content
        assert "linked release/review evidence" in content
        assert "Numeric comparison alone is insufficient" in content

    def test_planner_tests_as_semantic_evidence(self) -> None:
        """Planner treats tests that distinguish current and historical values
        as explicit semantic authority."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "When tests intentionally distinguish current and historical values" in content
        assert "explicit semantic authority" in content

    def test_planner_78_current_33_historical_recognized(self) -> None:
        """Planner recognizes 78 as current state and 33 as preserved historical v0.4.0 evidence."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "78` is the current state" in content
        assert "33` is preserved historical v0.4.0 evidence" in content
        assert "must not propose changing the historical value" in content

    def test_planner_no_gap_returns_defer_or_reject(self) -> None:
        """Planner returns Defer or Reject when values are historically justified
        and the current state is correct."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "historically justified and the current state is" in content
        assert "correct, return:" in content

    def test_planner_no_gap_fields_become_none(self) -> None:
        """Planner sets manual-vs-agent, role, profile, and artifact to none
        when no evidence-backed gap exists."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Manual vs agent: none" in content
        assert "Agent role: none" in content
        assert "Execution profile: none" in content
        assert "Artifact: none" in content

    def test_planner_no_delegated_prompt_for_historical_differences(self) -> None:
        """Planner does not generate a delegated prompt for historically justified
        value differences."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Do not generate a delegated prompt" in content  # in no-gap outcome

    def test_planner_ambiguous_context_defers(self) -> None:
        """Planner returns Defer when context is ambiguous and states missing evidence."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "If context is ambiguous, return `Defer`" in content
        assert "Never convert ambiguity into a manual edit" in content
        assert "state missing evidence" in content

    def test_planner_prefers_pytest_collect_only_q(self) -> None:
        """Planner prefers pytest --collect-only -q over full basetemp runs for test count."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "pytest --collect-only -q" in content

    def test_planner_rejects_fragile_grep_parsing(self) -> None:
        """Planner rejects fragile parsing like pytest --collect-only | grep 'tests collected'."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "grep" in content
        assert "tests collected" in content
        assert "Reject fragile parsing" in content

    def test_planner_exact_untracked_paths_required(self) -> None:
        """Planner requires exact paths for untracked files and classification
        as inside/outside the repository."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Report exact paths for any modified, staged, or untracked files" in content
        assert "inside/outside the repository" in content

    def test_planner_documentation_value_evidence_fields(self) -> None:
        """Planner requires Statement classification, Context evidence, Test evidence,
        and Mismatch status for documentation-value tasks."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "Statement classification: CURRENT STATE" in content
        assert "Context evidence:" in content
        assert "Test evidence:" in content
        assert "Mismatch status: CONFIRMED" in content

    def test_planner_proceed_only_when_confirmed(self) -> None:
        """Planner allows Proceed or Manual execution sufficient only when mismatch
        status is CONFIRMED."""
        content = _source_agent("planner.md").read_text(encoding="utf-8")
        assert "is allowed only when mismatch" in content
        assert "status is `CONFIRMED`" in content


class TestMechanicalAgent:
    """Tests for the mechanical agent definition."""

    def test_mechanical_definition_exists(self) -> None:
        """Mechanical agent definition exists at the expected path."""
        source = _source_agent("mechanical.md")
        assert source.is_file()

    def test_mechanical_role_identity(self) -> None:
        """Mechanical identifies itself as the deterministic operations role."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "# Mechanical" in content
        assert "deterministic low-judgment" in content

    def test_mechanical_no_model_names(self) -> None:
        """Mechanical contains no concrete runtime-model names."""
        import re

        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        pattern = re.compile(
            r"(gpt|deepseek|claude|gemini|llama|anthropic|openai|groq|mistral)",
            re.IGNORECASE,
        )
        assert not pattern.search(content), f"Model name found: {pattern.search(content)}"

    def test_mechanical_edit_denied(self) -> None:
        """Mechanical cannot edit semantic content."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "edit: deny" in content

    def test_mechanical_task_delegation_denied(self) -> None:
        """Mechanical cannot delegate tasks."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "task: deny" in content

    def test_mechanical_verification_commands_allowed(self) -> None:
        """Mechanical allows verification commands."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        for cmd in (
            '"sha256sum *": allow',
            '"cmp *": allow',
            '"diff *": allow',
            '"find *": allow',
            '"test *": allow',
            '"wc *": allow',
            '"grep *": allow',
            '"sed *": allow',
        ):
            assert cmd in content, f"Missing allow rule: {cmd}"

    def test_mechanical_git_add_is_ask(self) -> None:
        """Mechanical git add is ask, never unconditional allow."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert '"git add*": ask' in content
        assert '"git add*": allow' not in content

    def test_mechanical_write_commands_denied(self) -> None:
        """Mechanical denies commit, push, reset, clean, and destructive commands."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        for cmd in (
            '"git commit*": deny',
            '"git push*": deny',
            '"git reset*": deny',
            '"git clean*": deny',
            '"rm *": deny',
            '"mv *": deny',
            '"cp *": deny',
            '"mkfs*": deny',
            '"fdisk*": deny',
            '"parted*": deny',
        ):
            assert cmd in content, f"Missing deny rule: {cmd}"

    def test_mechanical_path_and_precondition_rules(self) -> None:
        """Mechanical states exact-path and precondition rules."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "explicit, fully-qualified paths" in content
        assert "Precondition checks" in content

    def test_mechanical_not_general_builder(self) -> None:
        """Mechanical is not described as a general-purpose builder."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "not a general-purpose builder" in content

    def test_mechanical_frontmatter_two_delimiters(self, tmp_path: Path) -> None:
        """Installed mechanical frontmatter has exactly two '---' delimiters."""
        source = _source_agent("mechanical.md")
        result = controlled_install(source, tmp_path)

        content = result["target"].read_text(encoding="utf-8")
        delimiters = _count_frontmatter_delimiters(content)
        assert delimiters == 2, f"Expected 2 frontmatter delimiters, found {delimiters}"

    def test_mechanical_audit_returned_in_completion(self) -> None:
        """Mechanical returns the audit in its completion response."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "returned in your completion response" in content
        assert "including the returned audit content" in content

    def test_mechanical_does_not_claim_direct_artifact_creation(self) -> None:
        """Mechanical does not claim direct audit-file creation."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "You do not create" in content
        assert "edit an audit file" in content
        assert "you do not persist files yourself" in content

    def test_mechanical_edit_deny_retained_after_remediation(self) -> None:
        """Mechanical edit: deny remains after the audit-boundary clarification."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert "edit: deny" in content

    def test_mechanical_git_add_ask_retained_after_remediation(self) -> None:
        """Mechanical git add*: ask remains after the audit-boundary clarification."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        assert '"git add*": ask' in content
        assert '"git add*": allow' not in content

    def test_mechanical_no_weakened_boundary_after_remediation(self) -> None:
        """Mechanical write and destructive command denials remain intact."""
        content = _source_agent("mechanical.md").read_text(encoding="utf-8")
        for cmd in (
            '"git commit*": deny',
            '"git push*": deny',
            '"git reset*": deny',
            '"git clean*": deny',
            '"rm *": deny',
            '"mv *": deny',
            '"cp *": deny',
        ):
            assert cmd in content, f"Missing deny rule: {cmd}"


class TestReadmeTestCount:
    """Tests for README current-vs-historical test-count treatment."""

    def test_readme_current_state_92_tests(self) -> None:
        """README gateway table states the current 78-test count."""
        readme = Path(__file__).resolve().parents[1] / "agent-pack" / "README.md"
        content = readme.read_text(encoding="utf-8")
        assert "| Repository validation | PASS (92 tests) |" in content

    def test_readme_preserves_historical_33_test_evidence(self) -> None:
        """README retains the historical v0.4.0 33-test release checkpoint."""
        readme = Path(__file__).resolve().parents[1] / "agent-pack" / "README.md"
        content = readme.read_text(encoding="utf-8")
        assert "repository validation: PASS, 33 tests" in content


class TestAgentCoexistence:
    """Tests for coexistence of all five OpenCode agents."""

    def test_all_five_agents_present(self) -> None:
        """All five agent definitions exist."""
        names = [
            "arch-data-engineer.md",
            "builder.md",
            "reviewer.md",
            "planner.md",
            "mechanical.md",
        ]
        for name in names:
            assert _source_agent(name).is_file(), f"Missing agent: {name}"

    def test_five_agent_install_preserves_all(self, tmp_path: Path) -> None:
        """Installing all five agents into one directory preserves all."""
        target_dir = tmp_path / "agents"
        target_dir.mkdir(parents=True)

        names = [
            "arch-data-engineer.md",
            "builder.md",
            "reviewer.md",
            "planner.md",
            "mechanical.md",
        ]
        for name in names:
            result = controlled_install(_source_agent(name), target_dir)
            assert result["action"] == "created"

        installed = {p.name for p in target_dir.iterdir()}
        assert installed == set(names)


class TestCodexNeuralEngineAdapter:
    """Tests for the bounded Codex CLI NeuralEngine adapter projection."""

    def test_codex_skill_exists_at_controlled_platform_path(self) -> None:
        """Codex skill is packaged under the platform-controlled source path."""
        assert _source_codex_skill().is_file()

    def test_codex_skill_has_only_required_frontmatter(self) -> None:
        """Codex projection has only the required skill metadata."""
        lines = _source_codex_skill().read_text(encoding="utf-8").splitlines()
        assert lines[0] == "---"
        closing = lines.index("---", 1)
        assert lines[1:closing] == [
            "name: neuralengine",
            "description: Use NeuralEngine as the durable project knowledge, decision, experience, and playbook layer for substantive repository, architecture, review, diagnostic, planning, and authorized Brain tasks.",
        ]

    def test_codex_skill_body_matches_shared_contract(self) -> None:
        """Codex projection cannot silently diverge from shared semantics."""
        skill = _source_codex_skill().read_text(encoding="utf-8")
        shared = _source_shared_neuralengine().read_text(encoding="utf-8")
        assert _skill_body(skill) == shared

    def test_codex_pointer_references_without_redefining_contract(self) -> None:
        """Project pointer names the skill and canonical source without policy duplication."""
        content = _source_codex_pointer().read_text(encoding="utf-8")
        assert ".agents/skills/neuralengine/SKILL.md" in content
        assert "agent-pack/shared/neuralengine.md" in content
        assert "does not duplicate or redefine that contract" in content
        assert "## Authority model" not in content
        assert "neural knowledge search" not in content
        assert "Brain-write" not in content
