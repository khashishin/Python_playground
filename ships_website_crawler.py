from urllib import request
from bs4 import BeautifulSoup

request_ship = BeautifulSoup(request.urlopen(input()).read(), "html.parser")
data= request_ship.findAll('div', {'class': 'group-ib nospace-between short-line'})
ship_name = request_ship.find('h1', {'class': 'font-200 no-margin'}).contents[0]
print (('Vessel Name', ship_name))
for index, x in enumerate(data):
    if index<5: print (tuple(x.text.replace("\n", "").split(': ')))
