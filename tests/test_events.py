from agent_research.core.artifacts import ArtifactStore
from agent_research.core.events import EvaluationEvent, EventType


def test_event_creation():
    event = EvaluationEvent(
        event_type=EventType.TASK_STARTED,
        run_id="run-1",
        task_id="task-1",
    )

    assert event.run_id == "run-1"
    assert event.task_id == "task-1"


def test_artifact_store_text(tmp_path):
    store = ArtifactStore(str(tmp_path))

    path = store.write_text("hello world")

    assert path.endswith(".txt")
