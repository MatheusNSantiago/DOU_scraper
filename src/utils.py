import unicodedata
from datetime import date, datetime
from zoneinfo import ZoneInfo


def tirar_acentuacao(string: str) -> str:
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )

def str_to_date(str: str) -> date:
    return datetime.strptime(str, "%Y-%m-%d").date()

def today_brasil_tz() -> date:
    return datetime.now(ZoneInfo("Brazil/East")).date()