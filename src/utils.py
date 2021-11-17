import json
import os
from pathlib import Path
import re
from datetime import datetime

TEMP_FOLDER = "../../tmp"  # É usado só em lambda function
# TEMP_FOLDER = "./tmp" sss


def get_env_variable(key: str):
    with open("credentials.json", "r") as f:
        cred = json.loads(f.read())
        path = key.split("/")
        return cred[path[0]][path[1]]


def extract_date_from_zip_path(zip_path: Path) -> datetime.date:
    match = re.search(r"\d{4}-\d{2}-\d{2}", zip_path)
    date = datetime.strptime(match.group(), "%Y-%m-%d").date()

    return date


def get_proxy():
    file_name = "proxy-list.txt"
    os.system(
        f"curl -sSf 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt' > {TEMP_FOLDER}/{file_name}"
    )

    with open(file_name, "r") as f:
        content = f.read()
        proxies = "\n".join(["http://" + proxy for proxy in content.splitlines()])
    with open(file_name, "w") as f:
        f.write(proxies)