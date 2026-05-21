from agent_research.agents.echo_agent import EchoAgent
from agent_research.agents.openai_agent import OpenAIAgent
from agent_research.agents.anthropic_agent import AnthropicAgent


AGENTS = {
    "echo": EchoAgent,
    "openai": OpenAIAgent,
    "anthropic": AnthropicAgent,
}


def create_agent(name: str):
    try:
        return AGENTS[name]()
    except KeyError as exc:
        available = ", ".join(sorted(AGENTS.keys()))
        raise ValueError(f"Unknown agent '{name}'. Available agents: {available}") from exc
