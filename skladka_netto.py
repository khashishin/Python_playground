liczba_pracownikow = int(input())

import math

class Pracownik:
    def __init__(self, imie, wynagrodzenie):
        self.imie=imie
        self.wynagrodzenie=int(wynagrodzenie)

    def policz_dane(self):
        emerytalna=round(self.wynagrodzenie*0.0976,2)
        rentowa=round(self.wynagrodzenie*0.0150,2)
        chorobowa=round(self.wynagrodzenie*0.0245,2)

        wynagrodzenie_pomn=self.wynagrodzenie - (emerytalna+rentowa+chorobowa)
        print (wynagrodzenie_pomn)
        brutto=self.wynagrodzenie-all
        zdrowotne = brutto *0.09
        koszty_przych = 111.25
        podst_zal_pod_doch=(brutto-koszty_przych)*0.82-46.33
        skl_zdrow=brutto*0.0775
        zal_doch=math.ceil(podst_zal_pod_doch - skl_zdrow)
        pelna_brutto=brutto - zdrowotne - zal_doch

laczny_koszt=0.00
for i in range(liczba_pracownikow):
    dane_pracownika = input().split(" ")
    pracownik = Pracownik(dane_pracownika[0],dane_pracownika[1])
    pracownik.policz_dane()
    laczny_koszt+= 0




