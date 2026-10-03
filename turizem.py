import csv
import os
import json
import requests

turizem_api_url = 'https://pxweb.stat.si:443/SiStatData/api/v1/sl/Data/2164525S.px'
# mapa, v katero bomo shranili podatke
turizem_directory = 'podatki'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'turizem_prihodi.json'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'turizem_prihodi.csv'


# print(requests.get(turizem_api_url).json()) - preverjanje imen ključev

def turizem_podatki(url):
    poizvedba = {
        "query": [
            {
                "code": "OBČINE",
                "selection": {"filter": "all", "values": ["*"]},
            },
            {
                "code": "DRŽAVA",
                "selection": {"filter": "item", "values": ["1", "2"]},
            },
            {
                "code": "MERITVE",
                "selection": {"filter": "all", "values": ["*"]},
            },
            {
                "code": "LETO",
                "selection": {"filter": "all", "values": ["*"]},
            },
        ],
        "response":{
            "format" : "json-stat2"
        }
    }
    try:
        page_content = requests.post(url, json = poizvedba).json()
    except requests.exceptions.RequestException:
        print("Spletna stran ni dosegljiva.")
        return None
    return page_content

#print(turizem_podatki(turizem_api_url))

# struktura seznama
# rezultat = turizem_podatki(turizem_api_url)
# print(rezultat['id'])      # vrstni red spremenljivk
# print(rezultat['size'])    # koliko vrednosti ima vsaka
