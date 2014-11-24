import urllib.request
import time
import csv
import operator

from bs4 import BeautifulSoup


#Performs a HTTP-'POST' request, passes it to BeautifulSoup and returns the result
def doRequest(request):
    requestResult = urllib.request.urlopen(request)
    soup = BeautifulSoup(requestResult)
    return soup


#Returns all the result links from the given search parameters
def getLinksFromSearch(plz_von, plz_bis):
    database = []
    links = []

    #The search parameters
    params = {
    'name_ff': '',
    'strasse_ff': '',
    'plz_ff': plz_von,
    'plz_ff2': plz_bis,
    'ort_ff': '',
    'bundesland_ff': '',
    'land_ff': 'DE',
    'traeger_ff': '',
    'Dachverband_ff': '',
    'submit2' : 'Suchen'
    }

    DATA = urllib.parse.urlencode(params)
    DATA = DATA.encode('utf-8')
    
    request = urllib.request.Request(
    "http://www.altenheim-adressen.de/schnellsuche/suche1.cfm",
    DATA)

    # adding charset parameter to the Content-Type header.
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0")

    #The search request 
    soup = doRequest(request)

    for link in soup.find_all('a'):
        database.append(link.get('href'))

    #Remove the first Element ('None') to avoid Attribute Errors
    database.pop(0)

    for item in database:
        if item.startswith("suche"):
            links.append(item)

    return links



#Performs a search on the link results
def searchOnLinks(links):
    adresses = []
    i = 1
    j = len(links)
    print("Found", j, "results, collecting data.")
    for item in links:
        adresses.append(getContactInfoFromPage(item, i, j))
        i = i + 1
        time.sleep(0.1)
    print("All done.")
    return adresses

#A method to scrape the contact info from the search result
def getContactInfoFromPage(page, i, j):
    name = ''
    straße = ''
    plz = ''
    stadt = ''
    telefon = ''
    mail = ''
    url = ''

    data = [
           #'Name',
           #'Straße',
           #'PLZ',
           #'Stadt',
           #'Telefon',
           #'E-Mail',
           #'Homepage'
            ]
    
    request = urllib.request.Request("http://www.altenheim-adressen.de/schnellsuche/" + page)
    #request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    request.add_header("Content-Type", "text/html;charset=UTF-8")
    request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0")
    
    
    print("(" , i , "/" , j , ") Making request...") 
    soup = doRequest(request)
    print("Done.")

    findeName = soup.findAll('b')
    name = findeName[2]
    name = name.string.split('>')

    data.append(name[0])

    straße = getFieldValue(soup, "Straße")
    data.append(straße)

    ort = getFieldValue(soup, "Ort")
    (plz, stadt) = ort.split(' ', 1)
    data.append(plz)
    data.append(stadt)

    telefon = getFieldValue(soup, "Telefon")
    data.append(telefon)

    mail = getFieldValue(soup, "EMail")
    data.append(mail)

    url = getFieldValue(soup, "Internetadresse")
    data.append(url)

    return data
    
#Strips the text from the given field's sibling
def getFieldValue(soup, field):
    field_label = soup.find('td', text=field + ':')
    return field_label.find_next_sibling('td').get_text(strip=True)

#The main input/output function
def inputOutput():
    #PLZ is German for zip-code and consists of a five-digit number
    #The program passes the numbers to the servers, and the server
    #returns all search results between the two numbers
    plz_von = input("Please enter first PLZ: ")
    plz_bis = input("Please enter second PLZ: ")

    links = getLinksFromSearch(plz_von, plz_bis)

    #Checks if the search yielded any results
    if len(links) > 0:
        data = searchOnLinks(links)
        file_name = input("Save as: ")
        print("Writing to file...")
        with open(file_name + '.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(data)

    else:
        print("The search yielded no results.")


inputOutput()
