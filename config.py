
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output_amazon_technologies"

TECH_CATEGORY_URL = "https://www.amazon.com/s?k=ordinateur+portable"

WAIT_TIMEOUT = 15

OUTPUT_DIR.mkdir(exist_ok=True)