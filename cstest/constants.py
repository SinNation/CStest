from datetime import datetime
from pathlib import Path

TIMESTAMP = datetime.now().strftime("%H:%M:%S")

CS_PATH = Path.cwd()
PROJECTS_PATH = CS_PATH.parents[0]
