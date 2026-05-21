from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    RUN_STARTED = "run_started"
    RUN_COMPLETED = "run_completed"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    HANDOFF_CREATED = "handoff_created"
    LOOP_STARTED = "loop_started"
    LOOP_ITERATION = "loop_iteration"
    LOOP_COMPLETED = "loop_completed"
    TOOL_CALLED = "tool_called"
    TOOL_COMPLETED = "tool_completed"
    GRADER_STARTED = "grader_started"
    GRADER_COMPLETED = "grader_completed"
    POLICY_VIOLATION = "policy_violation"
    ERROR = "error"


class EvaluationEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    run_id: str
    task_id: Optional[str] = None
    attempt_id: Optional[str] = None
    agent_id: Optional[str] = None
    source_agent_id: Optional[str] = None
    target_agent_id: Optional[str] = None
    loop_id: Optional[str] = None
    parent_event_id: Optional[str] = None

    input_ref: Optional[str] = None
    output_ref: Optional[str] = None
    value_ref: Optional[str] = None

    score: Optional[float] = None
    trust_score: Optional[float] = None
    passed: Optional[bool] = None
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    tokens_input: int = 0
    tokens_output: int = 0

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_json_line(self) -> str:
        return self.model_dump_json() + "\n"
