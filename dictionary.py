ludzie = input()
wyniki=input()

lista_uczestnikow = list(set( ludzie.lower().split(" ") ))
wyniki = wyniki.lower().split(" ")

lista_wynikow={}
for wynik in wyniki:
    if wynik in lista_uczestnikow:
        try:
            lista_wynikow[wynik]+=1
        except KeyError:
            lista_wynikow[wynik]=1
    else:
        continue
lista_wynikow = sorted(lista_wynikow.items(), key=lambda x: x[1], reverse=True)
print(lista_wynikow)