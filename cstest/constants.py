from datetime import datetime
from pathlib import Path

TIMESTAMP = datetime.now().strftime("%Y%M%d-%H%M%S")

CS_PATH = Path.cwd()
DATA_PATH = CS_PATH / "data"
PROJECTS_PATH = CS_PATH.parents[0]
