from dataclasses import dataclass
from datetime import date


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

    ementa: str  # Pode ser None
    titulo: str  # Pode ser None
    assinatura: str  # Pode ser None

    def __post_init__(self):
        if self.ementa is not None:
            self.ementa = self.ementa.text.strip()
        if self.titulo is not None:
            self.titulo = self.titulo.text
        if self.assinatura[0] is not None:
            self.assinatura = self.assinatura[0].text
        else:
            self.assinatura = None

    def to_json(self):
        return {
            "id": self.id,
            "secao": self.secao,
            "tipo_normativo": self.tipo_normativo,
            "data": str(self.data),
            "escopo": self.escopo,
            "conteudo": self.conteudo,
            "pdf": self.pdf,
            "id_materia": self.id_materia,
            "ementa": self.ementa,  # Pode ser None
            "titulo": self.titulo,  # Pode ser None
            "assinatura": self.assinatura,  # Pode ser None
        }
