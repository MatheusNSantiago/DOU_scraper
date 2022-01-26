import unicodedata
from datetime import date, datetime

def tirar_acentuacao(string: str) -> str:
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )

def str_to_date(str: str) -> date:
    return datetime.strptime(str, "%Y-%m-%d").date()