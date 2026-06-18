
from pathlib import Path
import json

CATEGORY_FILE = Path("vendors.json")


def load_categories():
    try:
        if CATEGORY_FILE.exists():
            with open(CATEGORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return {}
    return {}

def save_categories(data):
    with open(CATEGORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
 



