from dataclasses import dataclass

@dataclass
class Publicacao:
    """Representa uma publicação no Diário Oficial da União

    - A ementa pode ser None
    - O titulo pode ser None

    """

    secao: str
    tipo_normativo: str
    data: str
    escopo: str
    titulo: str
    ementa: str
    conteudo: str

