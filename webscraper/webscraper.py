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

#Find alle links på siden
links = []
linkContainers = mainPage_soup.findAll("a", {"class":"summarizedCategory"})
# Dictionary med NAVN,TLF
allCompanies = {}

for link in linkContainers:
    token = link.get("href") + "?loadedPages=500"
    token = urllib.parse.urlsplit(token)
    token = list(token)
    token[2] = urllib.parse.quote(token[2])
    token = urllib.parse.urlunsplit(token)
    links.append(token)
print("Done!")

#Find alle tags med telefon numre på alle siderne på alle links
print("Finder navne og tlf numre lol...", end = '')
for link in links:
    placeHolderURL = link
    newUClient = uReq(placeHolderURL)
    tokenPage_html = newUClient.read()
    tokenPage_soup = soup(tokenPage_html, "html.parser")
    allDetailContainers = tokenPage_soup.find_all("span", {"class": "details"})
    # Frasortér unødig HTML fra de nestede telefon nummrer tags
    for detail in allDetailContainers:
        phoneNum = detail.find("span", {"class":"phone"})
        phoneNum = phoneNum.text.strip()[5:]

        navn = detail.find("span", {"class": "name"})
        navn = navn.text.strip()
        navn = navn.upper()
        navn = navn.replace(',','')
        navn = navn.replace("'", "")
        navn = navn.replace('"','')
        # Tilføj nyt sæt i allCompanies med NAVN,TLF
        allCompanies[navn] = phoneNum

newUClient.close()
print("Done!")

print("Opretter csv fil lmao...", end = '')
fileName = "telefonNumre.csv"
f = open(fileName, "w")

f.write("navn,tlf\n")
print("Done!")
print("Indsætter tlf numre i CSV filen lol...", end = '')
# Iterér gennem allCompanies Dictionary'en og tilføj ny linje i CSV filen med X og Y værdien
# såfremt længden af navnet er større end 0. (Undgår blanke felter)
for x, y in allCompanies.items():
    if(len(y) > 0):
        f.write(x +","+ y +"\n")
        #inserter.importPhoneNumbers(x,y)
f.close()
print("Done!")