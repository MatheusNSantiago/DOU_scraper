from .utils import get_env_variable
from typing import List
import mysql.connector

from .model import Publicacao


# mydb = mysql.connector.connect(
#     host=get_env_variable("MYSQL/ENDPOINT"),
#     user=get_env_variable("MYSQL/USER"),
#     password=get_env_variable("MYSQL/PASSWORD"),
#     database=get_env_variable("MYSQL/DATABASE"),
# )
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="oasuet10",
    database="dou_db_local",
)

mycursor = mydb.cursor()


def upload_publicacoes_to_database(publicacoes: List[Publicacao]):

    sql = "INSERT INTO publicacoes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    val = [
        (
            pub.id,
            pub.secao,
            pub.tipo_normativo,
            pub.data,
            pub.escopo,
            pub.titulo,
            pub.ementa,
            pub.conteudo,
            pub.assinatura,
            pub.pdf,
        )
        for pub in publicacoes
    ]

    mycursor.executemany(sql, val)

    mydb.commit()
