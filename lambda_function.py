from datetime import date, datetime
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.spiders.dou_spider import DOU_Spider
from src.load_data import extract_publicacoes_from_zip
from src.repository import upload_publicacoes_to_database
import src.utils as utils
import os


def lambda_handler(event, context):
    scrape_after_date = date.today()
    # scrape_after_date = date(2021,12,6)

    # Começar o crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        DOU_Spider,
        email=utils.get_env_variable("INLABS/EMAIL"),
        password=utils.get_env_variable("INLABS/PASSWORD"),
        scrape_after_date=scrape_after_date,
    )
    process.start()

    # |-----------------------------------------||-----------------------------------------|
    # extrair dados e passar pra database

    folder_path = utils.TEMP_FOLDER

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    folder = [
        i
        for i in os.listdir(folder_path)
        if datetime.strptime(i[:10], "%Y-%m-%d").date() >= scrape_after_date
    ]

    zips_processed = 0
    for zip_filename in folder:
        publicacoes = extract_publicacoes_from_zip(f"{folder_path}/{zip_filename}")

        upload_publicacoes_to_database(publicacoes)

        pct_complete = f"({round((zips_processed/len(folder) * 100),2)}%)"
        print(pct_complete, zip_filename)
        zips_processed += 1

    return


if __name__ == "__main__":
    lambda_handler(None, None)
