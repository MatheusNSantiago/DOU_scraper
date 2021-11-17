from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.spiders.dou_spider import DOU_Spider
from src.load_data import extract_publicacoes_from_zip
from src.repository import upload_publicacoes_to_database
import src.utils as utils
import os

TEMP_FOLDER = "../../tmp"  # É usado só em lambda function
# TEMP_FOLDER = "./tmp" sss


def lambda_handler(event, context):
 
    utils.get_proxy()
    
    # Começar o crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        DOU_Spider,
        email=utils.get_env_variable("INLABS/EMAIL"),
        password=utils.get_env_variable("INLABS/PASSWORD"),
    )
    process.start()

    # # |-----------------------------------------||-----------------------------------------|

    # # extrair dados e passar pra database
    # zip_folder_path = TEMP_FOLDER

    # if not os.path.exists(zip_folder_path):
    #     os.mkdir(zip_folder_path)

    # for zip_filename in os.listdir(zip_folder_path):
    #     publicacoes = extract_publicacoes_from_zip(zip_folder_path+'/'+zip_filename)

    #     upload_publicacoes_to_database(publicacoes)

    #     os.remove(zip_filename)
    # return


if __name__ == "__main__":
    lambda_handler(1, 2)
