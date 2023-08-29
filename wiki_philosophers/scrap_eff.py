import requests
from bs4 import BeautifulSoup
import numpy as np

page = requests.get('https://en.wikipedia.org/wiki/Immanuel_Kant')

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="bodyContent")

jobs = results.find_all("td", class_="infobox-full-data")



def check_philosopher_link(title, name, URL):
    
    # print('Name: ', name)
    
    try:
        response = requests.get(URL)
    except:
        return 'LinkFailed'
    
    url_text = BeautifulSoup(response.text, 'html.parser')

    pp = url_text.find("div", class_="shortdescription nomobile noexcerpt noprint searchaux")
    
    try:
        if 'philosopher' in pp.text:
            return name.lower()
        else:
            return 'NotPhilosopher'
    except:
        return 'SomethingElse'
    
AZ = np.load('all_philosophers/AZ.npy') 

def check_name(title, name, URL):
    # print('Name: ', name)
    for element in AZ:
        # if all(substring in element for substring in name.split()) or all(substring in element for substring in title.split()):
        #     return element
        match1 = set(element.split()).intersection(set(name.split()))
        match2 = set(element.split()).intersection(set(title.split()))

        if (len(match1) == len(name.split())) or (len(match2) == len(title.split())):
            return element
    else:
        return check_philosopher_link(title, name, URL)

influences = []
influenced = []


for job_element in jobs:    
    if job_element.find_all(text = "Influences"):
        for element in job_element.find_all("a"):
            if element.get('title'):
                if element.get('href'):
                    influences.append(check_name(element.text.lower(), element.get('title').lower(), 'https://en.wikipedia.org/' + element.get('href')))
    
    if job_element.find_all(text = "Influenced"):
        for element in job_element.find_all("a"):
            if element.get('title'):
                if element.get('href'):
                    influenced.append(check_name(element.text.lower(), element.get('title').lower(), 'https://en.wikipedia.org/' + element.get('href')))   

print(influences)  
print(influenced)   
