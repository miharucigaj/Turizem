import csv
import os
import json
import requests

prebivalstvo_api_url = 'https://pxweb.stat.si:443/SiStatData/api/v1/sl/Data/05C5003S.px'
# mapa, v katero bomo shranili podatke
prebivalstvo_directory = 'podatki'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'prebivalstvo_obcine.json'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'prebivalstvo_obcine.csv'

# print(requests.get(prebivalstvo_api_url).json())

meta = requests.get(prebivalstvo_api_url).json()
obcina_naselje = meta['variables'][0]
vse_kode_obcine = obcina_naselje['values']
pravilne_obcinske_kode = [koda for koda in vse_kode_obcine if len(koda) <= 3]

leta = meta['variables'][1]
vse_kode_leta = leta['values']
pravilna_leta = [leto for leto in vse_kode_leta if leto >= '2018' and leto <= '2025']


def prebivalstvo_podatki(url):
   poizvedba = {
       "query": [
           {
               "code": "OBČINA/NASELJE",
               "selection": {"filter": "item", "values": pravilne_obcinske_kode},
           },
           {
               "code": "LETO",
               "selection": {"filter": "item", "values": pravilna_leta},
           },
           {
               "code": "MERITVE",
               "selection": {"filter": "item", "values": ['0']},
           }
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

# print(prebivalstvo_podatki(prebivalstvo_api_url))

#rezultat = prebivalstvo_podatki(prebivalstvo_api_url)
#print(rezultat.keys())  # kateri so glavni ključi v odgovoru?
#print(rezultat['id'])      # vrstni red spremenljivk
#print(rezultat['size'])    # koliko vrednosti ima vsaka

def prebivalstvo_v_vrstice(podatki):
    
    obcine_naselja_dim = podatki['dimension']['OBČINE']['category']
    meritve_dim = podatki['dimension']['MERITVE']['category']
    leto_dim = podatki['dimension']['LETO']['category']

    # zamenjava ključev in vrednosti npr. namesto {'0': 0, '001': 1, '213': 2, '195': 3, ...} v {0: '0', 1: '001', 2: '213', 3: '195', ...}
    obcine_po_indeksu = {}
    for k, v in obcine_dim['index'].items():
       obcine_po_indeksu[v] = k
    drzave_po_indeksu = {}
    for k, v in drzava_dim['index'].items():
       drzave_po_indeksu[v] = k
    meritve_po_indeksu = {}
    for k, v in meritve_dim['index'].items():
       meritve_po_indeksu[v] = k
    leta_po_indeksu = {}
    for k, v in leto_dim['index'].items():
       leta_po_indeksu[v] = k

    #stevila turistov / prenočitev
    vrednosti = podatki['value']

    #grajenje vrstic
    vrstice = []
    stevec = 0
    for obcina_indeks in range(213):
        for drzava_indeks in range(2):
            for meritev_indeks in range(2):
                for leto_indeks in range(8):  
                    vrednost = vrednosti[stevec]
                    stevec += 1

                    obcina_koda = obcine_po_indeksu[obcina_indeks]
                    drzava_koda = drzave_po_indeksu[drzava_indeks]
                    meritev_koda = meritve_po_indeksu[meritev_indeks]
                    leto_koda = leta_po_indeksu[leto_indeks]

                    vrstica = {
                        "obcina": obcine_dim['label'][obcina_koda],
                        "poreklo": drzava_dim['label'][drzava_koda],
                        "meritev": meritve_dim['label'][meritev_koda],
                        "leto": leto_dim['label'][leto_koda],
                        "vrednost": vrednost,
                    }
                    vrstice.append(vrstica)

    return vrstice
