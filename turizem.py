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
#rezultat = turizem_podatki(turizem_api_url)
#print(rezultat.keys())  # kateri so glavni ključi v odgovoru?
#print(rezultat['id'])      # vrstni red spremenljivk
#print(rezultat['size'])    # koliko vrednosti ima vsaka

def turizem_v_vrstice(podatki):
    # razčlemba podatkov
    obcine_dim = podatki['dimension']['OBČINE']['category']
    drzava_dim = podatki['dimension']['DRŽAVA']['category']
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

# print(turizem_v_vrstice(turizem_podatki(turizem_api_url)))

def write_csv(fieldnames, rows, directory, filename):
    # fieldnames - imena stolpcev, rows - seznam slovarjev, directory - mapa kamor shrani datoteko s podatki, filename - ime datoteke s podatki
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8', newline = "") as csv_file:
        #newline - zahteva csv za pravilne prelome vrstic
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return

def write_turizem_stevilke_to_csv(vrstice, directory, filename):
    assert vrstice and (all(j.keys() == vrstice[0].keys() for j in vrstice))
    fieldnames = list(vrstice[0].keys())
    write_csv(fieldnames, vrstice, directory, filename)
    
def main():
    # Podatki iz API-ja
    podatki = turizem_podatki(turizem_api_url)

    # Podatke pretvorimo v seznam slovarjev
    vrstice = turizem_v_vrstice(podatki)

    # Podatke shranimo v csv datoteko
    write_turizem_stevilke_to_csv(vrstice, turizem_directory, csv_filename)


if __name__ == '__main__':
    main()