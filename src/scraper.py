from datetime import date
import bs4
from bs4.element import CData

from .model import Publicacao

def scrape_xml(raw_xml: str, data: date) -> Publicacao:
    """Função auxiliar que que extrai os dados de um arquivo XML e retorna uma [Publicacao]"""

    soup_lxml = bs4.BeautifulSoup(raw_xml, "lxml")
    soup_html_parser = bs4.BeautifulSoup(raw_xml, "html.parser")
    _conteudo = soup_html_parser.find_all(text=lambda tag: isinstance(tag, CData))[
        -1
    ].text
    conteudo_soup = bs4.BeautifulSoup(_conteudo, "lxml")

    _id = soup_lxml.article["id"]
    _secao = soup_lxml.article["pubname"]
    _tipo_normativo = soup_lxml.article["arttype"]
    _escopo = soup_lxml.article["artcategory"]

    _titulo = conteudo_soup.find("p", class_="identifica")
    _ementa = conteudo_soup.find("p", class_="ementa")
    _assinatura = conteudo_soup.find("p", class_="assina"),
        
    return Publicacao(
        id=_id,
        secao=_secao,
        tipo_normativo=_tipo_normativo,
        escopo=_escopo,
        conteudo=_conteudo,
        data=data,
        titulo=_titulo,
        ementa=_ementa,
        assinatura=_assinatura,
    )
