from pathlib import Path

TICKER = "SSK.JO"
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
GENERATED_DIR = PROJECT_DIR / "generated"
FIGURES_DIR = GENERATED_DIR / "figures"


def csv_name(descriptor: str) -> str:
    return f"{TICKER.split('.')[0]}_{descriptor}.csv"


def csv_path(descriptor: str) -> str:
    output_dir = GENERATED_DIR / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir / csv_name(descriptor))
