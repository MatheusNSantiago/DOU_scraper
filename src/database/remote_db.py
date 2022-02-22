from typing import List
from ..publicacao import Publicacao
from tqdm import tqdm
from azure.cosmos import CosmosClient
import config
import concurrent
import logging

# Tirar o spam de logging que o cosmosDB + urlib3 faz
logger_urllib3= logging.getLogger("urllib3.connectionpool")
logger_urllib3.setLevel(logging.WARNING)
logger_azure = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
logger_azure.setLevel(logging.WARNING)

def inserir_publicacoes_remote_db(pubs: List[Publicacao]):
    """Coloca as publicações na database [dou] no (cosmosDB)"""

    client = CosmosClient(
        url=config.cosmos["ACCOUNT_URI"],
        credential=config.cosmos["ACCOUNT_KEY"],
    )
    db = client.get_database_client(config.cosmos["DATABASE_ID"])
    container = db.get_container_client("dou")

    def _upsert_pub(publicacao: Publicacao):
        publicacao = publicacao.to_json()

        try:
            container.upsert_item(publicacao)
        except:
            # As vezes a publicação é grande de mais pro cosmos
            publicacao["conteudo"] = publicacao["conteudo"][0:3000]
            container.upsert_item(publicacao)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for _ in tqdm(
            executor.map(_upsert_pub, pubs),
            total=len(pubs),
            desc="Inserindo publicações na base de dados",
        ):
            pass
