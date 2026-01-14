import sys
import json
import importlib
from pathlib import Path


def load_agents_registry():
    config_path = Path(__file__).parent.parent / "config" / "agents.json"
    with open(config_path) as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m catalyst_agent_framework run <agent> <input>")
        return

    command = sys.argv[1]

    # Optional default agent
    if len(sys.argv) == 2:
        agent_name = "task"
        input_text = ""
    else:
        agent_name = sys.argv[2]
        input_text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""

    if command != "run":
        print("Unknown command")
        return

    registry = load_agents_registry()

    if agent_name not in registry:
        print(f"Unknown agent: {agent_name}")
        return

    agent_cfg = registry[agent_name]

    if not agent_cfg.get("enabled", False):
        print(f"Agent '{agent_name}' is disabled")
        return

    required_keys = ("module", "class")
    for key in required_keys:
        if key not in agent_cfg:
            print(f"Invalid agent config for '{agent_name}': missing '{key}'")
            return

    try:
        module = importlib.import_module(agent_cfg["module"])
        agent_class = getattr(module, agent_cfg["class"])
    except Exception as e:
        print(f"Failed to load agent '{agent_name}': {e}")
        return

    agent = agent_class(name=agent_name)
    result = agent.run(input_text)
    print(result)
