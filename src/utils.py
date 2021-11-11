import json

def get_env_variable(key):
    with open("credentials.json", "r") as f:
        cred = json.loads(f.read())

        return cred[key]