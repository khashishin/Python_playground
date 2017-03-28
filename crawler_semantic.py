from urllib import request
from bs4 import BeautifulSoup

start_website = "http://www.coigdzie.pl/"
site = BeautifulSoup(request.urlopen(start_website).read(), "html.parser")

# links=site.findAll('div', {'class':"cig_happening  recommended"})
# for link in links:
#     print (link.find("h2").text)
#     data = link.find("span", {'class':'address'}).text
#     print(data)

daty = site.findAll('span', {'class': 'venue'} )
daty = set(daty)

for data in daty:
    print (data.text)