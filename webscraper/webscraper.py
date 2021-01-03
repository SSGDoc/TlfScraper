from urllib.request import urlopen as uReq
import urllib.parse
from bs4 import BeautifulSoup as soup
import PayLoadInserter as inserter

mainPageUrl = 'https://novaindex.com/dk/aalborg'

# Åben forbindelse til siden
uClient = uReq(mainPageUrl)

#Hent siden
mainPage_html = uClient.read()

#Luk forbindelsen til siden
uClient.close()
mainPage_soup = soup(mainPage_html, "html.parser")
print("Finder links...", end = '')

#Find alle links
links = []
linkContainers = mainPage_soup.findAll("a", {"class":"summarizedCategory"})
allCompanies = {}

for link in linkContainers:
    token = link.get("href") + "?loadedPages=500"
    token = urllib.parse.urlsplit(token)
    token = list(token)
    token[2] = urllib.parse.quote(token[2])
    token = urllib.parse.urlunsplit(token)
    links.append(token)
print("Done!")
#Find alle phone containers på alle links

print("Finder navne og tlf numre...", end = '')
for link in links:
    placeHolderURL = link
    newUClient = uReq(placeHolderURL)
    tokenPage_html = newUClient.read()
    tokenPage_soup = soup(tokenPage_html, "html.parser")
    allDetailContainers = tokenPage_soup.find_all("span", {"class": "details"})

    for detail in allDetailContainers:
        phoneNum = detail.find("span", {"class":"phone"})
        phoneNum = phoneNum.text.strip()[5:]

        navn = detail.find("span", {"class": "name"})
        navn = navn.text.strip()
        navn = navn.upper()
        navn = navn.replace(',','')
        navn = navn.replace("'", "")
        navn = navn.replace('"','')

        allCompanies[navn] = phoneNum

newUClient.close()
print("Done!")

print("Opretter csv fil...", end = '')
fileName = "telefonNumre.csv"
f = open(fileName, "w")

f.write("navn,tlf\n")
print("Done!")
print("Indsætter tlf numre i databasen...", end = '')
for x, y in allCompanies.items():
    if(len(y) > 0):
        f.write(x +","+ y +"\n")
        inserter.importPhoneNumbers(x,y)
f.close()
print("Done!")