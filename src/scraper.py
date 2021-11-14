from datetime import date
from .model import Publicacao
import xml.etree.ElementTree as ET


def scrape_xml(raw_xml: str, data:date) -> Publicacao:
    """Função auxiliar que que extrai os dados de um arquivo XML e retorna uma [Publicacao]"""

    xtree = ET.fromstring(raw_xml)
    article = xtree.find("article")
    
    # Extrai os dados necessários
    _id = article.get("id") 
    secao = article.attrib.get("pubName")
    tipo_normativo = article.get("artType")
    escopo = article.attrib.get("artCategory")
    titulo = article.find("body/Identifica").text
    ementa = article.find("body/Ementa").text
    conteudo = article.find("body/Texto").text

    return Publicacao(_id, secao, tipo_normativo, data, escopo, titulo, ementa, conteudo)
