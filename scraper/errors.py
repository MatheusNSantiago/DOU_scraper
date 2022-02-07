import collections
from scrapy.exceptions import CloseSpider
from datetime import date

Raised_exceptions = collections.namedtuple("Raised_exceptions", ["exception", "reason"])
scraper_raised_exception: Raised_exceptions = None


class PastaNaoEncontrada(CloseSpider):
    """Exceção que força o fechamento do scraper quando a primeira pasta encontrada não é a do dia de hoje

    Essa exceção só é raised quando se trata de uma chamada programática pelo AWS Lambda
    """

    def __init__(self, last_folders_date: date = None):
        self.reason = f"""O scraper não encontrou a pasta do dia {date.today()} no inlabs (última pasta foi do dia {last_folders_date}).
        Possíveis causas são:
            1) O scraper foi chamado em um dia não úti.
            2) Um problema no Inlabs. * Esse é bem raro de acontecer, já que só houve uma ocasião (ver dia 28/12/2021 em 'Problemas com a Imprensa Nacional') em que eles deixaram de postar a pasta do dia"""

        super(Exception, self).__init__(self.reason)


class FaltandoSecoes(CloseSpider):
    """Exceção que força o fechamento do scraper quando está faltando seções no DOU de hoje

    Essa exceção só é raised quando se trata de uma chamada programática pelo AWS Lambda
    """

    def __init__(self, _zips_que_entraram = None):
        self.reason = f"""
             O scraper só achou {" e ".join(_zips_que_entraram)} na pasta do dia {str(date.today())}.
             Essa exceção foi provavelmente causada pelo fato da Imprensa Nacional ainda não ter postado as seções que faltam
            """

        super(Exception, self).__init__(self.reason)
