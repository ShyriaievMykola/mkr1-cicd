from pathlib import Path
import sys

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))

from src.population_analysis import main

if __name__ == "__main__":
    main()
