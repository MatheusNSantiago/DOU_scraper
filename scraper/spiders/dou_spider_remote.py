from datetime import date
from scrapy import Spider, FormRequest
from scrapy.http.response.html import HtmlResponse
from ..items import ScraperItem
from src.utils import str_to_date
import scraper.errors as errors
import re


class DOUSpiderRemote(Spider):
    name = "dou_remote"
    start_urls = ["https://inlabs.in.gov.br/acessar.php"]

    def parse(self, response: HtmlResponse):

        formdata = {
            "email": self.email,
            "password": self.password,
        }

        return FormRequest.from_response(
            response,
            formdata=formdata,
            formxpath="//form[@action='logar.php']",
            callback=self.dou_list,
        )

    def dou_list(self, response: HtmlResponse):
        """Página que lista as pastas dos DOUs por dia no Inlabs"""

        folders = response.xpath("//div[@class='filename']/a")
        first_folder_date = str_to_date(folders.xpath(".//text()").get().strip())

        # | Fecha o scraper caso a última pasta não seja a de hoje
        if first_folder_date != date.today():
            raise errors.PastaNaoEncontrada(last_folders_date=first_folder_date)

        # | Vai pra pasta do DOU de hoje e o da edição anterior
        yield from response.follow_all(folders[0:2], callback=self.dou_page)

    def dou_page(self, response: HtmlResponse):
        """Página que lista os zips das seções do DOU para serem baixados"""

        dou_date = str_to_date(re.search("\d{4}-\d{2}-\d{2}", response.url).group())

        secoes = dict()

        files = response.xpath("//div[@class='filename']/a")
        for file in files:
            file_name = file.xpath(".//text()").get().strip()
            file_href = response.urljoin(file.xpath(".//@href").get())

            # | Se for a pasta de hoje, pega os zips da seção 1, 2 ou 3
            if dou_date == date.today():
                if re.search("\d{4}-\d{2}-\d{2}-DO[123]\.zip", file_name):
                    secoes[file_name] = file_href

            # | Se for o da edição anterior, pega só as seções extras
            else:
                if re.search("\d{4}-\d{2}-\d{2}-DO[123]\w+\.zip", file_name):
                    secoes[file_name] = file_href

        if (dou_date == date.today()) and (len(secoes.keys()) < 3):
            raise errors.FaltandoSecoes(secoes.keys())

        for file_name, file_url in secoes.items():
            item = ScraperItem()

            item["file_urls"] = [file_url]
            item["file_name"] = file_name

            yield item
