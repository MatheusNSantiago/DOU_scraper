from datetime import date
from typing import List
from zipfile import ZipFile
from pathlib import Path
from .model import Publicacao
from .scraper import scrape_xml


def extract_publicacoes_from_zip(path_zip: Path) -> List[Publicacao]:
    """Retorna uma lista das publicações extraidas do zip"""

    publicacoes = []
    data_de_publicacao = date.today();

    # Para cada arquivo xml no zip, extrai os dados que constituem uma publicação e acrescenta essa publicação na lista
    with ZipFile(path_zip, "r") as zip:
        for file in zip.filelist:
            if file.filename.endswith(".xml"):
                raw_xml = zip.read(file)
                
                publicacao = scrape_xml(raw_xml, data=data_de_publicacao)
                publicacoes.append(publicacao)
                
    return publicacoes   

