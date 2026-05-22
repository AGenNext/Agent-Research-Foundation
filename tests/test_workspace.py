from pathlib import Path

from agent_research.execution.workspace import PatchApplier


def test_patch_file_written(tmp_path):
    workspace = tmp_path / 'repo'
    workspace.mkdir()

    patch = 'diff --git a/a.txt b/a.txt'

    applier = PatchApplier()

    result = applier.apply_patch(str(workspace), patch)

    patch_file = Path(workspace) / 'agent.patch'

    assert patch_file.exists()
    assert 'diff --git' in patch_file.read_text()
