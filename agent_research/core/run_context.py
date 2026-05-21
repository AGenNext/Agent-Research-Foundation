from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class RunContext:
    run_id: str = field(default_factory=lambda: str(uuid4()))
    benchmark_id: str = "unknown"
    agent_team_id: str = "default"
    environment_id: str = "local"
