# Turizem
V okviru projektne naloge pri predmetu Uvod v programiranje sem analiziral turistične trende v slovenskih občinah med letoma 2018 in 2025.
Podatke o prihodu turistov sem zajel iz spletne strani: https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/2164525S.px,
podatke o številu prebivalcev v občinah pa sem zajel iz spletne strani: https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/05C5003S.px
Podatke pa sem s pomočjo pythona shranil v csv datoteki s pomočjo [turizem.py](turizem.py) in [prebivalstvo.py](prebivalstvo.py).

V mapi [podatki](podatki/) sta shranjeni datoteki:
- [prebivalstvo_obcine.csv](podatki/prebivalstvo_obcine.csv), ki vsebuje ime občine, leto ter število prebivalcev v občini tistega leta,
- [turizem_prihodi.csv](turizem_prihodi.csv), ki vsebuje podatke o občini, poreklu turista (domačin / tujec), podatek o prihodu ali prenočitvi turista, leto ter vrednost prihodov ali prenočitev turistov.

Analiza podatkov pa je predstavljena v datoteki [analiza_turizma.ipynb](analiza_turizma.ipynb).
