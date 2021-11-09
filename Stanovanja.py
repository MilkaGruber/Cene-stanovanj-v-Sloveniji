import csv
import os
import requests
import re

lj_center_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'
lj_okolica_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/stanovanje/'
gorenjska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/gorenjska/stanovanje/'
juzna_primorska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/juzna-primorska/stanovanje/'
severna_primorska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/severna-primorska/stanovanje/'
notranjska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/notranjska/stanovanje/'
savinjska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/savinjska/stanovanje/'
podravska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/podravska/stanovanje/'
koroska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/koroska/stanovanje/'
dolenjska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/dolenjska/stanovanje/'
posavska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/posavska/stanovanje/'
zasavska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/zasavska/stanovanje/'
pomurska_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/pomurska/stanovanje/'

st_lj_center = 31
st_lj_okolica = 6
st_gorenjska = 6
st_juzna_primorska = 8
st_severna_primorska = 2
st_notranjska = 1
st_savinjska = 6
st_podravska = 10
st_koroska = 1
st_dolenjska = 3
st_posavska = 1
st_zasavska = 1
st_pomurska = 2

seznam = [
[lj_center_frontpage_url, st_lj_center, 'stanovanja_lj_center.html', 'stanovanja_lj_center.csv'],
[lj_okolica_frontpage_url, st_lj_okolica, 'stanovanja_lj_okolica.html', 'stanovanja_lj_okolica.csv'],
[gorenjska_frontpage_url, st_gorenjska, 'stanovanja_gorenjska.html', 'stanovanja_gorenjska.csv'],
[juzna_primorska_frontpage_url, st_juzna_primorska, 'stanovanja_juzna_primorska.html', 'stanovanja_juzna_primorska.csv'],
[severna_primorska_frontpage_url, st_severna_primorska, 'stanovanja_severna_primorska.html', 'stanovanja_severna_primorska.csv'],
[notranjska_frontpage_url, st_notranjska, 'stanovanja_notranjska.html', 'stanovanja_notranjska.csv'],
[savinjska_frontpage_url, st_savinjska, 'stanovanja_savinjska.html', 'stanovanja_savinjska.csv'],
[podravska_frontpage_url, st_podravska,'stanovanja_podravska.html', 'stanovanja_podravska.csv'],
[koroska_frontpage_url, st_koroska, 'stanovanja_koroška.html', 'stanovanja_koroška.csv'],
[dolenjska_frontpage_url, st_dolenjska, 'stanovanja_dolenjska.html', 'stanovanja_dolenjska.csv'],
[posavska_frontpage_url, st_posavska, 'stanovanja_posavska.html', 'stanovanja_posavska.csv'],
[zasavska_frontpage_url, st_zasavska, 'stanovanja_zasavska.html', 'stanovanja_zasavska.csv'],
[pomurska_frontpage_url, st_pomurska, 'stanovanja_pomurska.html', 'stanovanja_pomurska.csv']
]

imena_polj = ['lokacija', 'sobno', 'nadstropje', 'leto', 'velikost', 'cena']

stanovanja_directory = 'podatki_stanovanja'
csv_filename = 'stanovanja'

def download_url_to_string(url):
    try:
        page_content = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Verjetno imaš težave z internetom.')
        return None
    return page_content.text

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'a', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def read_file_to_string(directory, filename):
    with open(os.path.join(directory, filename), encoding='UTF-8') as input_file:
        return input_file.read()

def poberi_iz_vseh(seznam_url): 
    l = len(seznam_url)
    for i in range(l):
        datoteka = seznam_url[i][2]
        text = ''
        for st in range(seznam_url[i][1]):
            url = seznam_url[i][0] + f'{st}/'
            text += f'{seznam_url[i][0]}' + download_url_to_string(url)
            save_string_to_file(text, stanovanja_directory, datoteka)

def page_to_ads(page_content):
    pattern = r'<div class="oglas_container(.*?)<div class="clearer"></div>' 
    regexp = re.compile(pattern, re.DOTALL)
    return re.findall(regexp, page_content)

def vzorec_podatkov_iz_oglasa(block):
    pattern = (r'.*?<span class="title">(?P<lokacija>.*?)</span></a>.*?' 
    r'<span class="vrsta">Stanovanje</span><span class="tipi">(?P<sobno>.*?)</span></span>.*?' 
    r'<span class="atribut">Nadstropje: <strong>(?P<nadstropje>.*?)</strong>.*?' 
    r'class="atribut leto">Leto: <strong>(?P<leto>.*?)</strong>.*?' 
    r'<span class="velikost" lang="sl">(?P<velikost>.*?)m2</span>.*?'
    r'<span class="cena">(?P<cena>.*?) &euro;</span>'
    )
    regexp = re.compile(pattern, flags=re.DOTALL)
    najdeno = re.search(regexp, block)
    if najdeno:
        return najdeno.groupdict()
    else:
        return None

def seznam_slovarjev(regija_bloki):
    sez = []
    for blok in regija_bloki:
        sez.append(vzorec_podatkov_iz_oglasa(blok))
    return sez

def pripravi_imenik(ime_datoteke):
    pripravi_imenik(ime_datoteke)
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            if slovar:
                writer.writerow(slovar)

def izbrisi(sez):
    while None in sez:
        sez.remove(None)
    return sez

def main(seznam):
    for regija in seznam:
        vsebina_regije = read_file_to_string(stanovanja_directory, regija[2])
        seznam_sl = (seznam_slovarjev(page_to_ads(vsebina_regije)))
        zapisi_csv(izbrisi(seznam_sl), imena_polj, regija[3])

main(seznam)



