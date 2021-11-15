from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from src.load_data import extract_publicacoes_from_zip
import os

from src.repository import upload_publicacoes_to_database
import src.utils as utils


def handler(event, context):
    # Inicia o crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        "dou",
        email=utils.get_env_variable("INLABS/EMAIL"),
        password=utils.get_env_variable("INLABS/PASSWORD"),
    )

    process.start()

#     # |-----------------------------------------||-----------------------------------------|

    if not os.path.exists("zips"):
        os.mkdir("zips")

    for zip_path in os.listdir("zips"):
        zip_path = f"zips/{zip_path}"
        publicacoes = extract_publicacoes_from_zip(zip_path)
        
        upload_publicacoes_to_database(publicacoes)
        
        os.remove(zip_path)
        