from scrapy import Spider, FormRequest
from scrapy.http.response.html import HtmlResponse
from ..items import ScraperItem
from src.utils import str_to_date


class DOUSpiderLocal(Spider):
    name = "dou_local"
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

        for folder in folders:
            f_name = folder.xpath(".//text()").get()
            f_date = str_to_date(f_name.strip())

            if (self.initial_date <= f_date) and (f_date <= self.last_date):
                yield response.follow(folder, callback=self.dou_page)

    def dou_page(self, response: HtmlResponse):
        files = response.xpath("//div[@class='filename']/a")

        for file in files:
            file_name = file.xpath(".//text()").get().strip()
            file_href = file.xpath(".//@href").get()

            if file_name.endswith(".zip"):
                item = ScraperItem()
                item["file_urls"] = [response.urljoin(file_href)]
                item["file_name"] = file_name

                yield item
