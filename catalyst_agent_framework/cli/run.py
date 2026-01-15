import sys
import json
import importlib
from pathlib import Path

def print_response(response):
    print("\n=== Agent Output ===")
    print(response.output)

    if response.steps:
        print("\n--- Steps ---")
        for i, step in enumerate(response.steps, start=1):
            print(f"{i}. {step['role']}: {step['content']}")

    if response.metadata:
        print("\n--- Metadata ---")
        for k, v in response.metadata.items():
            print(f"{k}: {v}")

def load_agents_registry():
    config_path = Path(__file__).parent.parent / "config" / "agents.json"
    with open(config_path) as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m catalyst_agent_framework run <agent> <input>")
        return 1

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
        return 1

    registry = load_agents_registry()

    if agent_name not in registry:
        print(f"Unknown agent: {agent_name}")
        return 1

    agent_cfg = registry[agent_name]

    if not agent_cfg.get("enabled", False):
        print(f"Agent '{agent_name}' is disabled")
        return 1

    required_keys = ("module", "class")
    for key in required_keys:
        if key not in agent_cfg:
            print(f"Invalid agent config for '{agent_name}': missing '{key}'")
            return 1

    try:
        module = importlib.import_module(agent_cfg["module"])
        agent_class = getattr(module, agent_cfg["class"])
    except Exception as e:
        print(f"Failed to load agent '{agent_name}': {e}")
        return 1

    agent = agent_class(name=agent_name)
    result = agent.run(input_text)
    print_response(result)
    return 0