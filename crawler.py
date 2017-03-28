from urllib import request
from bs4 import BeautifulSoup
import numpy as np
start_ip = "http://150.254.36.78"
start_url="/SW-10/01-00.html"
unique_pages_set= set()
page_linking = set()
d = 0.85

def traverse_link(start_ip,start_url):
    start_website = start_ip+start_url
    site = BeautifulSoup(request.urlopen(start_website).read(), "html.parser")
    links=site.findAll('a')

    for element in links:
        link_url = element["href"]
        link = start_ip+link_url
        page_linking.add(tuple([start_website,link]))

        if link  not in unique_pages_set:
            unique_pages_set.add(link)
            if link_url[:3]=="htt":
                traverse_link(link_url,"")
            else:
                traverse_link(start_ip,link_url)


traverse_link(start_ip,start_url)
N=len(unique_pages_set)
pages_mapping=dict()
index=0
for page in unique_pages_set:
    pages_mapping[index]=page
    index+=1

def get_key(value):
    for k,v in pages_mapping.items():
        if v == value:
            return k


A = [[0 for i in range(N)] for y in range(N)]

for vote in page_linking:
    A[get_key(vote[0])][get_key(vote[1])] = 1

new_A = A
for i, row in enumerate(A):
    if sum(row) == 0:
        new_A[i] = [ ((1.0/N)*d)+((1-d)/N)  for x in range(N)]
    else:
        sum_in_row = float(sum(A[i]))
        new_A[i] = [((elem/sum_in_row)*d+((1-d)/N)) for elem in A[i]]

A = new_A

vectorw  = prev_vectorw= [1, 0, 0, 0]
changed_after_6 = True
while changed_after_6:
    vectorw = np.dot(np.array(vectorw), np.array(A))
    delta =  [abs(x - y) for x, y in zip(vectorw, prev_vectorw)]
    changed_after_6 = any([elem > 0.000001 for elem in delta])
    prev_vectorw = vectorw

print(sorted([round(float(elem), 4) for elem in vectorw], reverse=True))


# NOTATKI
# wiersze strony startowe
# kolumy docelowe
#
# Dla wszystkich wierszy sprawdzamy dzie mozna przejsc (macierz incydencji)
#
# Suma elementow wierszu (do ilu ide) i podzielenie pageranku, pomnoz je przez d
#
#
# dodac 1-d/n do kazdego
#
#
# 1-d/N - szansa znalezienia sie na stronie z nikad
# d(...) szansa z innych
#
#
# z macierzy potem liczymy PR dla strony
#
#
# mnozymy wektor razy macierz dopoki sie nie zmienia
# tak jak z wartosciami wlasnymi lambda*x = x