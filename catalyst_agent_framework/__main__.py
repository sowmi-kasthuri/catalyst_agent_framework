from dotenv import load_dotenv
load_dotenv()

from catalyst_agent_framework.cli.run import main
import sys

if __name__ == "__main__":
    sys.exit(main())