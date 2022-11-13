import os
import requests
from bs4 import BeautifulSoup

# Disclaimer
print("This application will store your location information in a local file called Info.txt, if you'd like to change the location, delete the contents of the file and run the script again.")

# Saves location so it doesn't have to be manually typed each time
infoFile = 'Info.txt'
if os.path.exists(infoFile) == False:
    with open(infoFile, 'w', encoding='utf-8') as writeFile:
        location = input('Where would you like to search? (City, 2 Letter State): ').lower()
        writeFile.write(location)
elif os.path.exists(infoFile):
    with open(infoFile, 'rt') as readFile:
        location = readFile.read()

# Turns location into URL format
locationList = location.split(', ', 1)
city = locationList[0].split(' ')
state = locationList[1]
cityCode = '+'.join(city)
locationCode = cityCode + '%2C+' + state

# Turns search term into URL format
searchTerm = input('What would you like to search for?: ')
searchTermList = searchTerm.split(" ")
if len(searchTermList) == 1:
    search = searchTermList[0]
elif len(searchTermList) >= 2:
    search = "+".join(searchTermList)

# Collects page number and puts the URL together
pageNumber = input('Which page number would you like to search on?: ')
if pageNumber == 1:
    URL = f'https://www.simplyhired.com/search?q={search}&l={locationCode}'
else:
    URL = f'https://www.simplyhired.com/search?q={search}&l={locationCode}&pn={pageNumber}'
pageCode = requests.get(URL)

# Parses HTML from URL
soup = BeautifulSoup(pageCode.content, 'html.parser')
results = soup.find(id='job-list')

# Gets all job elements from HTML
jobElements = results.find_all('article', class_='SerpJob')

# Searches for jobs with the search term in the title
searchedJobs = results.find_all('h3', string=lambda text: searchTerm in text.lower())
if not bool(searchedJobs):
    print('Search returned no results, please try another page or a different search term.')
    quit()
searchedJobElements = [h3_element.parent.parent.parent for h3_element in searchedJobs]

# Grabs all elements of jobs that passed the search and prints them
for jobElement in searchedJobElements:
    titleElement = jobElement.find('h3', class_='jobposting-title')
    subtitleElement = jobElement.find('div', class_='jobposting-subtitle')
    companyElement = subtitleElement.find('span', class_='jobposting-company')
    locationElement = subtitleElement.find('span', class_='jobposting-location')
    links = titleElement.find('a', class_='card-link', href=True)
    print(titleElement.text)
    print(companyElement.text)
    print(locationElement.text)
    print(f'Apply here: https://simplyhired.com{links["href"]}')
