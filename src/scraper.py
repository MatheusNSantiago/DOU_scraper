from .model import Publicacao
import xml.etree.ElementTree as ET

def scrape_xml(raw_xml: str) -> Publicacao:
    """Função auxiliar que que extrai os dados de um arquivo XML e retorna uma [Publicacao]"""

    xtree = ET.fromstring(raw_xml)
    article = xtree.find("article")
    
    # Extrai os dados necessários
    secao = article.attrib.get("pubName")
    tipo_normativo = article.get("artType")
    data = article.get("pubDate"),
    data = data[0].replace("/", "-") 
    escopo = article.attrib.get("artCategory")
    titulo = article.find("body/Identifica").text
    ementa = article.find("body/Ementa").text
    conteudo = article.find("body/Texto").text

    return Publicacao(secao, tipo_normativo, data, escopo, titulo, ementa, conteudo)
