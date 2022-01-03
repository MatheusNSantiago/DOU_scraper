from typing import List
import mysql.connector
from mysql.connector.errors import IntegrityError
from .model import Publicacao
import logging

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="matheus",
    password="oasuet10",
    database="test",
)

mycursor = mydb.cursor()


def upload_publicacoes_to_database(publicacoes: List[Publicacao]):

    sql = "INSERT INTO publicacoes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for pub in publicacoes:
        try:
            mycursor.execute(
                sql,
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
                    pub.id_materia,
                ),
            )
            mydb.commit()

        except IntegrityError as e:
            logging.error(
                f"{e}. Esse erro foi provavelmente obtido ao tentar inserir uma publicação que já existe na database (os ids delas são iguais)"
            )
