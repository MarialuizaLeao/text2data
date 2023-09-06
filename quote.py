import requests
import numpy as np
from bs4 import BeautifulSoup
import scrapy


alreadyFound = set()
seachedPhilosophers = set()

linksList = list()

AZ_names = np.load('wiki_philosophers/all_philosophers/AZ.npy')
AZ_url = np.load('wiki_philosophers/all_philosophers/AZ_url.npy')

AZ_names = AZ_names.tolist()
AZ_url = AZ_url.tolist()

def getPageTittle(soup):
    return soup.find("h1", class_="firstHeading mw-first-heading").text
    
def getNameOfRedirectedPage(URL):
    page = requests.get('https://en.wikipedia.org' + str(URL))
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find("h1", class_="firstHeading mw-first-heading").text

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
        
        currentPhilosopher = getPageTittle(soup)
        seachedPhilosophers.add(currentPhilosopher)
        

        for jobElement in jobs:
            if jobElement.find_all(string = "Influences"):
                for element in jobElement.find_all("a"):
                    if element.get('title'):
                        if element.get('href')[:6] == "/wiki/":
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
                                }
        if len(linksList) > 0:     
            next_page = "https://en.wikipedia.org" + str(linksList.pop(0))
        else:
            while(True and len(AZ_names) > 0):
                name = AZ_names.pop(0)
                link = AZ_url.pop(0)
                if name not in seachedPhilosophers:
                    next_page = "https://en.wikipedia.org" + str(link)
                    break
                
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page)
            )