liczba_pracownikow = int(input())


class Pracownik:
    def __init__(self, imie, wynagrodzenie):
        self.imie=imie
        self.wynagrodzenie=int(wynagrodzenie)
        self.koszty_przych = 111.25

    def policz_dane(self):
        emerytalna=round(self.wynagrodzenie*0.0976,2)
        rentowa=round(self.wynagrodzenie*0.0150,2)
        chorobowa=round(self.wynagrodzenie*0.0245,2)
        wynagrodzenie_pomn=round(self.wynagrodzenie - (emerytalna+rentowa+chorobowa),2)
        skladka_zdrowotna = round(wynagrodzenie_pomn *0.09 , 2)
        podst_podatku_dochodowego=round(((wynagrodzenie_pomn-self.koszty_przych)*0.18 -46.33),2)
        skladka_zdrowotna_do_odliczenia=round(wynagrodzenie_pomn*0.0775,2)
        pod_dochod=round((podst_podatku_dochodowego-skladka_zdrowotna_do_odliczenia),0)
        
        netto=round(wynagrodzenie_pomn-skladka_zdrowotna-pod_dochod,2)
    
        koszty_prac= round(self.wynagrodzenie*0.0976,2) + \
                     round(self.wynagrodzenie*0.065,2) + round(self.wynagrodzenie*0.0193,2) + \
                     round(self.wynagrodzenie*0.0245,2) + round(self.wynagrodzenie*0.001,2) #Bez funduszu pomostowego
        self.laczny_koszt=round(float(self.wynagrodzenie)+koszty_prac,2)
        
        return(self.imie+ " {:.2f} {:.2f} {:.2f}").format(netto, koszty_prac, self.laczny_koszt)
    def get_laczny_koszt(self):
        return self.laczny_koszt
        

laczny_koszt=0.00
lista_wynikow=[]
for i in range(liczba_pracownikow):
    dane_pracownika = input().split(" ")
    pracownik = Pracownik(dane_pracownika[0],dane_pracownika[1])
    lista_wynikow.append(pracownik.policz_dane())
    laczny_koszt+= pracownik.get_laczny_koszt()

for wynik in lista_wynikow:
    print (wynik)
    
print(("{:.2f}").format(laczny_koszt))

