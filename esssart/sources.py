import json

import requests
from .db import db

def pull_sources_list():
    data_sources = [
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.bns.json",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.population-global.json",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.publics.json",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.population-publics.json",
    ]

    for data_source in data_sources:
        cut = data_source.split("/")[-1]
        file_name = f'./data/{cut}'
        data = requests.get(data_source).text
        print(f'{file_name}')
        with open(file_name, "w") as file:
            file.write(data)

def seed_db():
    file_name = f'data/endlesss.population-global.json'
    with open(file_name, "r") as file:
        data = json.load(file)

    names = [(i, "") for i in data['users']]
    db.user.name_create_many(names)
