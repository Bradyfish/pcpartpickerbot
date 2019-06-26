import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from time import sleep

#launch url
url = "https://pcpartpicker.com/products/cpu/"

# create a new Firefox session
browser = webdriver.Firefox()

browser.get(url)
sleep(2)

innerHTML = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

soup=BeautifulSoup(innerHTML, 'html.parser')

all = soup.find_all("tr", {"class":"tr__product"})

oldnames = []
for item in all:
    oldnames.append(item.find("div", {"class":"td__nameWrapper"}).text)

names = []
for name in oldnames:
    spl = name.split()
    del spl[-1]
    names.append(' '.join(spl))

cores = []
for item in all:
    cores.append(item.find("td", {"class": "td__spec td__spec--1"}).text[10:])

basespeeds = []
for item in all:
    basespeeds.append(item.find("td", {"class": "td__spec td__spec--2"}).text[10:])

ocspeeds = []
for item in all:
    ocspeed = item.find("td", {"class": "td__spec td__spec--3"})
    try:  # I'm so sorry for this, i can't test if dtype == None lmao
        if len(ocspeed) != 0:
            ocspeeds.append(ocspeed.text[11:])
    except:
        ocspeeds.append("Cannot Overclock")

TDPs = []
for item in all:
    TDPs.append(item.find("td", {"class": "td__spec td__spec--4"}).text[3:])

IGs = []
for item in all:
    IGs.append(item.find("td", {"class": "td__spec td__spec--5"}).text[19:])

CPUPrices = []
for item in all:
    CPUPrices.append(item.find("td", {"class": "td__price"}).text[:-3])
for price in CPUPrices:
    try:
        len(price) == 3
    except:
        price = "No Price Listed"
        print("Ye")

SMTs = []
for item in all:
    yesno = item.find("td", {"class": "td__spec td__spec--6"}).text[3:]
    if yesno == "Yes":
        SMTs.append(True)
    else:
        SMTs.append(False)


threads = []
for core, SMT in zip(cores, SMTs):
    if SMT:
        threads.append(str(int(core) * 2))
    else:
        threads.append(str(core))


data = {'Name':names,
        'Price':CPUPrices,
        'Cores':cores,
        'Base Speed':basespeeds,
        'Overclock Speed':ocspeeds,
        'Thermal Design Power':TDPs,
        'Integrated Graphics':IGs,
        'Threads':threads}

CPUDF1 = pd.DataFrame(data)
CPUDF = CPUDF1.set_index("Name", drop = True)


