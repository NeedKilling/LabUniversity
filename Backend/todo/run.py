import os
import sys
from pathlib import Path


# Allow `python run.py` without installing the project as an editable package.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from todo_app import create_app


app = create_app()


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes", "on"}
    app.run("0.0.0.0", debug=debug)
