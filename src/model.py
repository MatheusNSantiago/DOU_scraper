from dataclasses import dataclass
from datetime import date

from bs4.element import Tag

@dataclass
class Publicacao:
    """Representa uma publicação no Diário Oficial da União

    - A ementa, título e assinatura podem ser None

    """

    id: str 
    secao: str
    tipo_normativo: str
    data: date
    escopo: str
    conteudo: str
    
    ementa: Tag
    titulo: Tag
    assinatura: Tag

    def __post_init__(self):
        if self.ementa is not None:
            self.ementa = self.ementa.text.strip()
        if self.titulo is not None:
            self.titulo = self.titulo.text
        if self.assinatura is not None:
            self.assinatura = self.assinatura.text
            

