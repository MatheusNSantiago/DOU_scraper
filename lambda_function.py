import logging
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.spiders.dou_spider_remote import DOUSpiderRemote
from src.load_data import extract_publicacoes_from_zip
from src.database.remote_db import inserir_publicacoes_remote_db
import os
import re
import config
import scraper.errors as errors

logging.basicConfig(level="WARNING")

def lambda_handler(event, context):

    # Começar o crawler
    process = CrawlerProcess(get_project_settings())

    process.crawl(
        DOUSpiderRemote,
        email=config.inlabs["EMAIL"],
        password=config.inlabs["PASSWORD"],
    )

    process.start()

    teve_algum_erro = errors.scraper_raised_exception != None

    if teve_algum_erro:
        erro_no_scraper = errors.scraper_raised_exception
        
        if erro_no_scraper.exception is errors.PastaNaoEncontrada:
            # TODO se for dia útil => Sucesso, se for problema do inlabs => roda dnv mais tarde
            # Esperar 30 minutos e ir dnv
            return {
                "body": erro_no_scraper.reason,
                "status": "PastaNaoEncontrada",
            }
        elif erro_no_scraper.exception is errors.FaltandoSecoes:
            # TODO refazer o scrape mais tarde
            return {
                "body": erro_no_scraper.reason,
                "status": "FaltandoSecoes",
            }
        else:
            # TODO pensar em outros erros possíveis e tentar resolvelos
            return {
                "body": "Outra parada aconteceu",
                "status": "ERRO",
            }

    else:
        folder_path = config.TEMP_FOLDER

        # Lista os zips que foram baixados
        zip_files = [
            file
            for file in os.listdir(folder_path)
            if re.search("\d{4}-\d{2}-\d{2}.+\.zip", file)  # formato do zip do DOU
        ]

        # Extrai e insere as publicações
        publicacoes = []
        for _zip in zip_files:
            publicacoes.extend(extract_publicacoes_from_zip(f"{folder_path}/{_zip}"))

        inserir_publicacoes_remote_db(publicacoes)

        return {
            "body": f"{len(publicacoes)} foram inseridas na database com sucesso",
            "status": "OK",  # Sucesso
        }