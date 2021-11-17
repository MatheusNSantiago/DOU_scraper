from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.spiders.dou_spider import DOU_Spider
from src.load_data import extract_publicacoes_from_zip
from src.repository import upload_publicacoes_to_database
import src.utils as utils
import os


def lambda_handler(event, context):
    # Começar o crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        DOU_Spider,
        email=utils.get_env_variable("INLABS/EMAIL"),
        password=utils.get_env_variable("INLABS/PASSWORD"),
    )
    process.start()

    # # |-----------------------------------------||-----------------------------------------|

    # extrair dados e passar pra database
    folder_path = utils.TEMP_FOLDER

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    folder = os.listdir(folder_path)

    zips_processed = 0
    for zip_filename in folder:
        publicacoes = extract_publicacoes_from_zip(f"{folder_path}/{zip_filename}")

        upload_publicacoes_to_database(publicacoes)

        pct_complete = (
            f"({round((zips_processed/len(os.listdir(folder_path)) * 100),2)}%)"
        )
        print(pct_complete, zip_filename)
        zips_processed += 1

    return


if __name__ == "__main__":
    lambda_handler(None, None)