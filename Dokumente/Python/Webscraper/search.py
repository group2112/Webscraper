import urllib.request

from bs4 import BeautifulSoup



#Returns all the result links from the given search parameters
def getLinks(plz_von, plz_bis):
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
    'land_ff': '',
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
    searchResult = urllib.request.urlopen(request)

    soup = BeautifulSoup(searchResult)

    for link in soup.find_all('a'):
        database.append(link.get('href'))

    #Remove the first Element ('None') to avoid Attribute Errors
    database.pop(0)

    for item in database:
        if item.startswith("suche"):
            links.append(item)

    return links


links = getLinks(50000, 50126)



        
