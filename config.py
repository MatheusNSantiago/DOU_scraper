import os

# No Lambda, a gente precisa colocar os zips no /tmp, mas localmente eu prefiro guardar aqui em ./tmp
# Solução foi por $TEMP_FOLDER na AWS, e localmente a gente usa o default ./tmp
TEMP_FOLDER = os.environ.get("TEMP_FOLDER", "./tmp")

inlabs = {
    "EMAIL": "matheus.nilo.santiago@gmail.com",
    "PASSWORD": "oasuet10",
}

local_mysql = {
    "HOST": "127.0.0.1",
    "USER": "matheus",
    "PASSWORD": "oasuet10",
    "DATABASE": "test",
}

cosmos = {
    "ACCOUNT_URI": "https://sumula-dou-db.documents.azure.com:443/",
    "ACCOUNT_KEY": "4sIVaLCH7R1eDdPleSZ5CvVEhoyqUs8NVtiDZR5CAwfYCjQWjjKPJiNMYdlsQvb5eNWdccjIbC0sCTplysEeqw==",
    "DATABASE_ID": "sumula-dou-db",
}
