from datetime import datetime
from typing import List
from zipfile import ZipFile
from pathlib import Path
from .scraper import scrape_xml
import re
from .model import Publicacao


def extract_publicacoes_from_zip(path_zip: Path) -> List[Publicacao]:
    """Retorna uma lista das publicações extraidas do zip"""

    publicacoes = []

    data_publicacao = re.search(r"\d{4}-\d{2}-\d{2}", path_zip).group()
    data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d").date()

    # Para cada arquivo xml no zip, extrai os dados que constituem uma publicação e acrescenta essa publicação na lista
    with ZipFile(path_zip, "r") as zip:
        for file in zip.filelist:
            if file.filename.endswith(".xml"):
                raw_xml = zip.read(file).decode()

                publicacao = scrape_xml(raw_xml, data=data_publicacao)
                publicacoes.append(publicacao)

    return publicacoes
