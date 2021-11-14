import json
from pathlib import Path
import re
from datetime import datetime


def get_env_variable(key):
    with open("credentials.json", "r") as f:
        cred = json.loads(f.read())

        return cred[key]

def extract_date_from_zip_path(zip_path: Path) -> datetime.date:
    match = re.search(r"\d{4}-\d{2}-\d{2}", zip_path)
    date = datetime.strptime(match.group(), "%Y-%m-%d").date()
        
    return date
