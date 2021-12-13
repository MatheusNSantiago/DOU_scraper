from dataclasses import dataclass
from datetime import date

from bs4.element import Tag


@dataclass
class Publicacao:
    """Representa uma publicação no Diário Oficial da União"""

    id: str
    secao: str
    tipo_normativo: str
    data: date
    escopo: str
    conteudo: str
    pdf: str
    id_materia: str

    ementa: str | None
    titulo: str | None
    assinatura: str | None

    def __post_init__(self):
        if self.ementa is not None:
            self.ementa = self.ementa.text.strip()
        if self.titulo is not None:
            self.titulo = self.titulo.text
        if self.assinatura[0] is not None:
            self.assinatura = self.assinatura[0].text
        else:
            self.assinatura = None
