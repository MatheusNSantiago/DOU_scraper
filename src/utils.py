import json

TEMP_FOLDER = "./tmp"  # É usado só em lambda function

def get_env_variable(key: str):
    with open("credentials.json", "r") as f:
        cred = json.loads(f.read())
        path = key.split("/")
        return cred[path[0]][path[1]]