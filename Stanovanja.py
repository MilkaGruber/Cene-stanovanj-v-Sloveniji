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

seznam_url = [
[lj_center_frontpage_url, st_lj_center, 'stanovanja_lj_center.html'],
[lj_okolica_frontpage_url, st_lj_okolica, 'stanovanja_lj_okolica.html'],
[gorenjska_frontpage_url, st_gorenjska, 'stanovanja_gorenjska.html'],
[juzna_primorska_frontpage_url, st_juzna_primorska, 'stanovanja_juzna_primorska.html'],
[severna_primorska_frontpage_url, st_severna_primorska, 'stanovanja_severna_primorska.html'],
[notranjska_frontpage_url, st_notranjska, 'stanovanja_notranjska.html'],
[savinjska_frontpage_url, st_savinjska, 'stanovanja_savinjska.html'],
[podravska_frontpage_url, st_podravska,'stanovanja_podravska.html'],
[koroska_frontpage_url, st_koroska, 'stanovanja_koroška.html'],
[dolenjska_frontpage_url, st_dolenjska, 'stanovanja_dolenjska.html'],
[posavska_frontpage_url, st_posavska, 'stanovanja_posavska.html'],
[zasavska_frontpage_url, st_zasavska, 'stanovanja_zasavska.html'],
[pomurska_frontpage_url, st_pomurska, 'stanovanja_pomurksa.html']
]

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

#poberi_iz_vseh(seznam_url)


