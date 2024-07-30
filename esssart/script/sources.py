import json

import requests
from ..app import app

def pull_sources_list():
    data_sources = [
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.bns.json",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.collectibles-snapshot",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.population-global.json",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.population-publics.json",
        "https://raw.githubusercontent.com/Unbundlesss/OUROVEON/main/bin/shared/endlesss.publics.json",
    ]

    for data_source in data_sources:
        cut = data_source.split("/")[-1]
        file_name = f'./data/json/{cut}'
        data = requests.get(data_source).text
        print(f'{file_name}')
        with open(file_name, "w") as file:
            file.write(data)


