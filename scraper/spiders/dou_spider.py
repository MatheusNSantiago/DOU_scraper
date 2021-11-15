from scrapy import Spider, FormRequest
from scrapy.http.response.html import HtmlResponse
from datetime import datetime
from ..items import ScraperItem


class DOU_Spider(Spider):
    name = "dou"
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
        """ Caso o DOU tenha a mesma data que o dia de hoje, vá pra página desse DOU  """

        first_folder = response.xpath("//div[@class='filename']/a")[0]
        first_folder_name = first_folder.xpath(".//text()").get()
        first_folder_date = datetime.strptime(first_folder_name.strip(), "%Y-%m-%d").date()

        if first_folder_date == datetime.today().date():
            yield response.follow(first_folder, callback=self.dou_page)

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
