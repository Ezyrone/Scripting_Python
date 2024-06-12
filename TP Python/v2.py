from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import sys

def score(recherche):

    xa=u'\xa0'
    req = Request(
        url="https://fr.search.yahoo.com/search?p={}".format(recherche), 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    for reponse in soup.find_all('h2'):

        result = re.search('Environ(.*)résultats', reponse.text)
        resultat = result.group(1).replace(xa, '').strip()
        return resultat


if len(sys.argv) < 3 :
    print(" nope, faut 2 paramétres ou plus")
    exit(1)
    
print("{} : {}".format(sys.argv[1], score(sys.argv[1])))
print("{} : {}".format(sys.argv[2], score(sys.argv[2])))