from agent_research.core.events import EventType


def test_error_event_type_exists():
    assert EventType.ERROR.value == 'error'
