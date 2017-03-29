ludzie = input()
wyniki=input()

ludzie = list(set(ludzie.split(" ")))
wyniki = wyniki.split(" ")

lista_wynikow=[]

for uczestnik in ludzie:
	lista_wynikow.append((uczestnik, wyniki.count(uczestnik)))
lista_wynikow.sort(key=lambda item: item[1], reverse=True)

print(lista_wynikow)
