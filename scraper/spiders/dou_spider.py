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
        """ Caso o DOU tenha sido lançado numa data maior ou igual ao [self.date], vá pra página desses DOUs  """

        folders = response.xpath("//div[@class='filename']/a")
        
        for folder in folders:
            folder_name = folder.xpath(".//text()").get()
            folder_date = datetime.strptime(folder_name.strip(), "%Y-%m-%d").date()
            
            if folder_date >= self.scrape_after_date:
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
