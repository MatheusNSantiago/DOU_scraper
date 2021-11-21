from datetime import date
import bs4
from bs4.element import CData
from .model import Publicacao

def scrape_xml(raw_xml: str, data: date):
    """Função auxiliar que que extrai os dados de um arquivo XML e retorna uma [Publicacao]"""

    soup_lxml = bs4.BeautifulSoup(raw_xml, "lxml")
    soup_html_parser = bs4.BeautifulSoup(raw_xml, "html.parser")

    return Publicacao(
        id=soup_lxml.article["id"],
        secao=soup_lxml.article["pubname"],
        tipo_normativo=soup_lxml.article["arttype"],
        escopo=soup_lxml.article["artcategory"],
        conteudo=soup_html_parser.find_all(text=lambda tag: isinstance(tag, CData))[
            -1
        ].text,
        data=data,
        titulo=soup_lxml.find("p", class_="identifica"),
        ementa=soup_lxml.find("p", class_="ementa"),
        assinatura=soup_lxml.find("p", class_="assina"),
    )

