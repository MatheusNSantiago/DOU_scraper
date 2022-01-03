import json
import unicodedata

TEMP_FOLDER = "./tmp"


def get_env_variable(key: str):
    with open("credentials.json", "r") as f:
        cred = json.loads(f.read())
        path = key.split("/")
        return cred[path[0]][path[1]]


def tirar_acentuacao(string: str | None) -> str | None:
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )
