from typing import List
import mysql.connector
from mysql.connector.errors import IntegrityError
from .publicacao import Publicacao
import logging
from azure.cosmos import CosmosClient
from azure.core.pipeline.policies import HttpLoggingPolicy
import config
import concurrent
from .utils import progressBar


logger_azure = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
# logger_azure.setLevel(logging.WARNING)
logger_azure.disabled = True

logger_urllib3 = logging.getLogger("urllib3.connectionpool")
# logger_urllib3.setLevel(logging.CRITICAL)
logger_urllib3.disabled = True


def upload_publicacoes_to_database(publicacoes: List[Publicacao]):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="matheus",
        password="oasuet10",
        database="test",
    )

    mycursor = conn.cursor()

    sql = "INSERT INTO publicacoes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for pub in publicacoes:
        try:
            mycursor.execute(
                sql,
                (
                    pub.id,
                    pub.secao,
                    pub.tipo_normativo,
                    pub.data,
                    pub.escopo,
                    pub.titulo,
                    pub.ementa,
                    pub.conteudo,
                    pub.assinatura,
                    pub.pdf,
                    pub.id_materia,
                ),
            )
            conn.commit()

        except IntegrityError as e:
            logging.error(
                f"{e}. Esse erro foi provavelmente obtido ao tentar inserir uma publicação que já existe na database (os ids delas são iguais)"
            )
    conn.close()


def inserir_publicacoes_dou_db(pubs: List[Publicacao]):
    """Coloca as publicações na database [dou] no (cosmosDB)"""

    client = CosmosClient(
        url=config.cosmos["ACCOUNT_URI"],
        credential=config.cosmos["ACCOUNT_KEY"],
    )
    db = client.get_database_client(config.cosmos["DATABASE_ID"])
    container = db.get_container_client("dou")

    def _upsert_pub(publicacao: Publicacao):
        publicacao.data = str(publicacao.data)
        publicacao = publicacao.__dict__

        try:
            container.upsert_item(publicacao)
        except:
            publicacao["conteudo"] = publicacao["conteudo"][0:2500]
            container.upsert_item(publicacao)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        def _print_progress_bar(iteration):
            length = 90  # Tamanho do progress bar
            total = len(pubs)
            filledLength = int(length * iteration // total)
            bar = "█" * filledLength + "-" * (length - filledLength)
            percent = "{0:.2f}".format(100 * (iteration / total))

            print(f"\r{iteration} |{bar}| {total} ({percent})%", end="\r")

        print("\nInserindo publicações na base de dados")
        iteration = 0
        for _ in executor.map(_upsert_pub, [pub for pub in pubs]):
            _print_progress_bar(iteration)

            iteration += 1
