import requests
import numpy as np
from bs4 import BeautifulSoup
import scrapy

i = 0

influences = []
influenced = []



class QuoteSpider(scrapy.Spider):
    name = 'quote-spider'
    start_urls = ['https://en.wikipedia.org/wiki/Socrates']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find(id="bodyContent")
        jobs = results.find_all("td", class_="infobox-full-data")

        for jobElement in jobs:
            if jobElement.find_all(text = "Influences"):
                for element in jobElement.find_all("a"):
                    if element.get('title'):
                        if element.get('href'):
                            yield{
                                'influences' : element.get('title')
                            }
                            #influences.append(check_whether_philosophy(element.text.lower(), element.get('title').lower(), 'https://en.wikipedia.org/' + element.get('href')))

        next_page = "https://en.wikipedia.org/wiki/Plato"
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page)
            )