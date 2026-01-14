import json
import importlib
from pathlib import Path

import sys
from ..agents.task_agent import TaskAgent

def load_agents_registry():
    config_path = Path(__file__).parent.parent / "config" / "agents.json"
    with open(config_path) as f:
        return json.load(f)


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m catalyst_agent_framework run <agent> <input>")
        return

    command = sys.argv[1]
    agent_name = sys.argv[2]
    input_text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""

    if command == "run":
        registry = load_agents_registry()

        if agent_name not in registry:
            print(f"Unknown agent: {agent_name}")
            return

        agent_cfg = registry[agent_name]
        module = importlib.import_module(agent_cfg["module"])
        agent_class = getattr(module, agent_cfg["class"])

        agent = agent_class(name=agent_name)
        result = agent.run(input_text)
        print(result)
    
    else:
        print("Unknown command")
