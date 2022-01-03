import unicodedata

def tirar_acentuacao(string: str | None) -> str | None:
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )
