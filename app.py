import requests
from bs4 import BeautifulSoup
import re 
import datetime

from database import database
from database import country_numbers

def textToInt(textString):
    #quitamos los caracteres especiales
    textString =  re.sub('[^0-9]', '', textString)

    try:
        output = int(textString)
    except ValueError:
        output=0

    return output

def main():

    db_conn = database.create_connection('coronavirus.db')

    now = datetime.datetime.now()
    processTime = now.strftime("%m-%d-%Y %H:%M:%S")

    URL = 'https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic#covid19-container'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    last_modification_string = ''

    # Obtenemos la descripción de la última modificacion
    try:
        last_modification = soup.find('li', id='footer-info-lastmod').getText()
        last_modification_string = last_modification.replace(' This page was last edited on ', '')
        last_modification_string = last_modification_string.replace(u'\xa0', u'')
        last_modification_string = last_modification_string.replace('.', '')
    except:
        print('can\'t get last time exception')

    # Obtenemos los datos de los paises
    country_table = soup.find('table', class_=['wikitable', 'plainrowheaders',  'sortable', 'jquery-tablesorter'])
    tbody = country_table.find('tbody')
    trs = tbody.find_all('tr')

    for tr in trs:
        isACountry = False
        countryData = {}

        ths = tr.find_all('th')
        for th in ths:
            country_link = th.find('a')
            if country_link:
                if len(country_link.text) > 3:
                    isACountry = True
                    countryData['get_datetime'] =  processTime
                    countryData['country_name']=country_link.text 
            #print(country_link['href'])
    
        if isACountry == True:
            tds = tr.find_all('td')
            if len(tds) >= 3:
                if tds:
                    countryData['cases'] = textToInt(tds[0].text)
                    countryData['deaths'] = textToInt(tds[1].text)
                    countryData['deaths_rate'] = (countryData['deaths']*100)/countryData['cases']
                    countryData['recovery'] = textToInt(tds[2].text)
                    countryData['recovery_rate'] = (countryData['recovery']*100)/countryData['cases']
                    countryData['original_last_modification'] = last_modification_string
                    
                    new_country_id = country_numbers.insertOne(db_conn, countryData)
            
            #print(countryData)

    database.close_connection(db_conn)

if __name__ == '__main__':
    main()
