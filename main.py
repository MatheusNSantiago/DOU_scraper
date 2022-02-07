from datetime import date, timedelta
import logging
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.spiders.dou_spider_local import DOUSpiderLocal
from src.load_data import extract_publicacoes_from_zip
from src.database.local_db import upload_publicacoes_to_local_db
from src.database.remote_db import inserir_publicacoes_remote_db
import os
import config
from src.utils import str_to_date

logging.basicConfig(level="WARNING")

last_date = date.today()
initial_date = date.today() - timedelta(days=0)
# initial_date = date.today() - timedelta(days=0)

# Começar o crawler
process = CrawlerProcess(get_project_settings())
process.crawl(
    DOUSpiderLocal,
    email=config.inlabs["EMAIL"],
    password=config.inlabs["PASSWORD"],
    last_date=last_date,
    initial_date=initial_date,
)
process.start()

folder_path = config.TEMP_FOLDER

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

zip_files = [
    i
    for i in os.listdir(folder_path)
    if (initial_date <= str_to_date(i[:10])) and (str_to_date(i[:10]) <= last_date)
]

publicacoes = []
for _zip in zip_files:
    publicacoes.extend(extract_publicacoes_from_zip(f"{folder_path}/{_zip}"))

upload_publicacoes_to_local_db(publicacoes)
# inserir_publicacoes_remote_db(publicacoes)
