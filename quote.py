import requests
import numpy as np
from bs4 import BeautifulSoup
import scrapy


alreadyFound = set()
seachedPhilosophers = set()
notSearchedPhilosophers = set()

linksList = list()

AZ = np.load('wiki_philosophers/all_philosophers/AZ.npy')
AZ_url = np.load('wiki_philosophers/all_philosophers/AZ_url.npy')

notSearchedPhilosophers = set(AZ)
    
def getNameOfRedirectedPage(URL):
    page = requests.get('https://en.wikipedia.org' + str(URL))
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find("span", class_="mw-page-title-main").text

def checkIfLinkRedirect(element):
    return element.get('class') == ['mw-redirect']
    #retornar true se eh redirecionado

class QuoteSpider(scrapy.Spider):
    name = 'quote-spider'
    start_urls = ['https://en.wikipedia.org/wiki/Socrates']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find(id="bodyContent")
        jobs = results.find_all("td", class_="infobox-full-data")
        
        currentPhilosopher = soup.find("span", class_="mw-page-title-main").text
        seachedPhilosophers.add(currentPhilosopher)
        

        for jobElement in jobs:
            if jobElement.find_all(string = "Influences"):
                for element in jobElement.find_all("a"):
                    if element.get('title'):
                        if element.get('href'):
                            if checkIfLinkRedirect(element):
                                name = getNameOfRedirectedPage(element.get('href'))
                            else:
                                name = element.get('title')
                            if(name not in seachedPhilosophers and name not in alreadyFound):
                                linksList.append(element.get('href'))
                                alreadyFound.add(name)
                                yield{
                                    'nome' : currentPhilosopher,
                                    'influences' : name,
                                    'ja pesquisados' : seachedPhilosophers
                                }
        if len(linksList) > 0:      
            next_page = "https://en.wikipedia.org" + str(linksList.pop(0))
        else:
            for i in range(len(AZ)):
                if AZ[i] not in seachedPhilosophers:
                    next_page = "https://en.wikipedia.org" + str(AZ_url[i])
                    print(next_page)
                    np.delete(AZ, i)
                    np.delete(AZ_url, i)
                    break
                    
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page)
            )