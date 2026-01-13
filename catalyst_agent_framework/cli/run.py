import sys
from ..agents.task_agent import TaskAgent

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m catalyst_agent_framework run <agent> <input>")
        return

    command = sys.argv[1]
    agent_name = sys.argv[2]
    input_text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""

    if command == "run" and agent_name == "task":
        agent = TaskAgent(name="task")
        result = agent.run(input_text)
        print(result)
    else:
        print("Unknown command or agent")
