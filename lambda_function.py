from datetime import date
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from src.load_data import extract_publicacoes_from_zip
import pandas as pd
import os
from src.repository import upload_to_aws
import src.utils as utils


def lambda_handler(event, context):
    # Inicia o crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        "dou",
        email=utils.get_env_variable("EMAIL"),
        password=utils.get_env_variable("PASSWORD"),
    )

    process.start()

    ##########################################

    # junta todas as publicações extraidas dos arquivos zip
    all_publicacoes = []

    for zip_path in os.listdir("zips"):
        zip_path = f"zips/{zip_path}"
        publicacoes = extract_publicacoes_from_zip(zip_path)

        all_publicacoes.extend(publicacoes)

        os.remove(zip_path)

    # faz um dataframe com todas as publicações do dia
    df = pd.DataFrame(all_publicacoes)

    # Salvar o dataframe
    df_feather_file = str(date.today()) + ".feather"
    df.to_parquet(df_feather_file)  # feather é bem mais leve

    upload_to_aws(
        local_file=df_feather_file,
        bucket="dao-bucket",
        s3_file=df_feather_file,
    )
    
    os.remove(df_feather_file)
    
    return "👍"



lambda_handler()
