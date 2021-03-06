import mysql.connector
from mysql.connector.errors import IntegrityError
from typing import List
from ..publicacao import Publicacao
from tqdm import tqdm



def upload_publicacoes_to_local_db(publicacoes: List[Publicacao]):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="matheus",
        password="oasuet10",
        database="test",
    )

    mycursor = conn.cursor()

    sql = "INSERT INTO publicacoes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for pub in tqdm(publicacoes, desc="Inserindo publicação na base de dados"):
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
            conn.commit()

        except IntegrityError as e:
            print(
                f"{e}. Esse erro foi provavelmente obtido ao tentar inserir uma publicação que já existe na database (os ids delas são iguais)", 
            )


            
    conn.close()
