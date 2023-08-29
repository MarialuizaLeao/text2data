import requests
from bs4 import BeautifulSoup
import numpy as np

page = requests.get('https://en.wikipedia.org/wiki/Plato')

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="bodyContent")

jobs = results.find_all("td", class_="infobox-full-data")



def check_whether_philosophy(title, name, URL):
    try:
        response = requests.get(URL)
    except:
        return 'LinkFailed'
    
    url_text = BeautifulSoup(response.text, 'html.parser')

    pp = url_text.find("div", class_="shortdescription nomobile noexcerpt noprint searchaux")
    
    if 'philosopher' in pp.text:
        return name.lower()
    else:
        return check_name(title, name)
    
AZ = np.load('all_philosophers/AZ.npy')

def check_name(title, name):
    print('Name: ', name)
    for element in AZ:
        if all(substring in element for substring in name.split()) or all(substring in element for substring in title.split()):
            return element
    else:
        return 'NotPhilosopher'

influences = []
influenced = []


for job_element in jobs:    
    if job_element.find_all(text = "Influences"):
        for element in job_element.find_all("a"):
            if element.get('title'):
                if element.get('href'):
                    influences.append(check_whether_philosophy(element.text.lower(), element.get('title').lower(), 'https://en.wikipedia.org/' + element.get('href')))
    
    if job_element.find_all(text = "Influenced"):
        for element in job_element.find_all("a"):
            if element.get('title'):
                if element.get('href'):
                    influenced.append(check_whether_philosophy(element.text.lower(), element.get('title').lower(), 'https://en.wikipedia.org/' + element.get('href')))   ##element.get('title'), also a possible scenario  

print(influences)  
print(influenced)   
