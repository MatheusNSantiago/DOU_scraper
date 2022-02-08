from datetime import date, timedelta
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.spiders.dou_spider_local import DOUSpiderLocal
from src.load_data import extract_publicacoes_from_zip
from src.database.local_db import upload_publicacoes_to_local_db
from src.database.remote_db import inserir_publicacoes_remote_db
import os
import config
from src.utils import str_to_date

# |─────────────────────────────────────────────| Config |─────────────────────────────────────────────|

last_date = date.today()
initial_date = date.today() - timedelta(days=2)

zip_folder_path = config.TEMP_FOLDER

# |────────────────────────────────────────────| Crawler |─────────────────────────────────────────────|

process = CrawlerProcess(get_project_settings())
process.crawl(
    DOUSpiderLocal,
    email=config.inlabs["EMAIL"],
    password=config.inlabs["PASSWORD"],
    last_date=last_date,
    initial_date=initial_date,
)
process.start()

# |────────────────────────────────────────| Extração/Limpeza |────────────────────────────────────────|

if not os.path.exists(zip_folder_path):
    os.mkdir(zip_folder_path)

zip_files = [
    i
    for i in os.listdir(zip_folder_path)
    if (initial_date <= str_to_date(i[:10])) and (str_to_date(i[:10]) <= last_date)
]

publicacoes = []
for _zip in zip_files:
    publicacoes.extend(extract_publicacoes_from_zip(f"{zip_folder_path}/{_zip}"))

# |─────────────────────────────────────────| Inserção na DB |─────────────────────────────────────────|

upload_publicacoes_to_local_db(publicacoes)
# inserir_publicacoes_remote_db(publicacoes)
