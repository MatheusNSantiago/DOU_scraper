from datetime import datetime
from typing import List
from zipfile import ZipFile
from pathlib import Path
import re
import logging
from .scraper import scrape_xml
from .publicacao import Publicacao
from .utils import tirar_acentuacao
from tqdm import tqdm
import concurrent.futures


def extract_publicacoes_from_zip(path_zip: Path) -> List[Publicacao]:
    """Retorna uma lista das publicações extraidas do zip"""

    publicacoes = []

    data_publicacao = re.search(r"\d{4}-\d{2}-\d{2}", path_zip).group()
    data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d").date()

    # Para cada arquivo xml no zip, extrai os dados que constituem uma publicação e acrescenta essa publicação na lista
    with ZipFile(path_zip, "r") as zip:
        for file in tqdm(
            zip.filelist,
            desc=f'Extraindo publicações de "{path_zip}"',
        ):
            if file.filename.endswith(".xml"):
                raw_xml = zip.read(file).decode()

                # Esse try:except foi porque algumas publicações estavam vindo corrompidas ou vazias
                try:
                    publicacao = scrape_xml(raw_xml, data=data_publicacao)
                    publicacoes.append(publicacao)
                except Exception:
                    logging.error(
                        f"[scrape_xml] não conseguiu pegar os dados da publicação {path_zip}/{file.filename} (size = {file.file_size})"
                    )

    publicacoes = limpar_publicacoes(publicacoes)

    return publicacoes


def limpar_publicacoes(publicacoes: List[Publicacao]) -> List[Publicacao]:
    """Já que a inlabs faz o scrape direto do pdf, se uma publicação ocupa X páginas (X>1), a mesma publicação vai ser dividida em X xmls. Para consertar isso, basta encontrar as publicações com a id_materia repetida e junta conteúdos e a assinatura delas em uma publicação só"""

    pubs_por_id_materia = {}

    for pub in publicacoes:
        # Tirar acentos das assinaturas
        pub.assinatura = tirar_acentuacao(pub.assinatura)

        # Colocar a publicação numa lista de publicacoes com o mesmo id_materia
        pubs_por_id_materia.setdefault(pub.id_materia, []).append(pub)

    clean_pubs = []
    for _, pubs in pubs_por_id_materia.items():
        pub: Publicacao

        # Junta o conteudo e a assinatura das publicações repartidas
        if len(pubs) > 1:
            pubs[0].assinatura = pubs[-1].assinatura
            pubs[0].conteudo = "".join([pub.conteudo for pub in pubs])

            pub = pubs[0]

        else:
            pub = pubs[0]

        clean_pubs.append(pub)

    return clean_pubs
