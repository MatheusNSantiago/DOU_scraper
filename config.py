import os

# No Lambda, a gente precisa colocar os zips no /tmp, mas localmente eu prefiro guardar aqui em ./tmp
# Solução foi por $TEMP_FOLDER na AWS, e localmente a gente usa o default ./tmp
TEMP_FOLDER = os.environ.get("TEMP_FOLDER", "./tmp")

inlabs = {
    "EMAIL": "matheus.nilo.santiago@gmail.com",
    "PASSWORD": "oasuet10",
}

mysql = {
    "ENDPOINT": "dou-db.cyg7qmc7z4nk.sa-east-1.rds.amazonaws.com",
    "PORT": 3306,
    "USER": "admin",
    "PASSWORD": "oasuet10",
    "DATABASE": "dou_db",
}

cosmos = {
    "ACCOUNT_URI": "https://sumula-dou-db.documents.azure.com:443/",
    "ACCOUNT_KEY": "4sIVaLCH7R1eDdPleSZ5CvVEhoyqUs8NVtiDZR5CAwfYCjQWjjKPJiNMYdlsQvb5eNWdccjIbC0sCTplysEeqw==",
    "DATABASE_ID": "sumula-dou-db",
}
