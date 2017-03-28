class Biblioteka:
    def __init__(self, limit):
        self.limit_wypozyczen= limit
        self.liczba_wypozyczen = 0
        self.dostepne_ksiazki = {}
        # [tytul, autor] = lista_egz

    def dostepne_egz(self):
            posortowane_ksiazki = sorted(self.dostepne_ksiazki.items(), key=lambda t: t[0])
            for x in posortowane_ksiazki:
                print ((x[0][0], x[0][1], len(x[1])))

    def wypozycz(self, autor, tytul, osoba):
        try:
            lista_egz = self.dostepne_ksiazki[(tytul,autor)]
            for x in lista_egz:
                if not x.wypozyczony and x.tytul == tytul:
                    if self.liczba_wypozyczen < self.limit_wypozyczen:
                        x.wypozyczony=True
                        osoba.lista_wypozyczonych.append(x)
                        return True
                    else:
                        return False
                else:
                    return False
        except:
            return False

    def oddaj(self, osoba, egzamplarz):
        try:
            lista_egz = self.dostepne_ksiazki[(egzamplarz.tytul,egzamplarz.autor)]
            for x in lista_egz:
                if egzamplarz==x:
                    x.wypozyczony=False
                    return True
        except:
            return False



    def dodaj_egzemplarz_ksiazki(self, tytul, autor, rok_wydania):
        try:
            self.dostepne_ksiazki[(tytul,autor)].append(Egzemplarz(tytul,autor,rok_wydania))
        except KeyError:
            self.dostepne_ksiazki[(tytul,autor)]=[Egzemplarz(tytul,autor,rok_wydania)]
        return True


class Czytelnik:
    def __init__(self, osoba):
        self.osoba = osoba
        self.lista_wypozyczonych=[]

    def wypozycz(self, tytul):
        Biblioteka.wypozycz(self.osoba, tytul)

    def oddaj(self, tytul, autor):
        for ksiazka in self.lista_wypozyczonych:
            if (ksiazka.tytul==tytul and ksiazka.autor==autor):
                variable = Biblioteka.oddaj(self.osoba, ksiazka)
                if variable==True:
                    self.lista_wypozyczonych.remove(ksiazka)
                return variable

class Ksiazka:
    def __init__(self, tytul, autor):
        self.tytul=tytul
        self.autor=autor

class Egzemplarz(Ksiazka):
    def __init__(self, tytul, autor, rok):
        self.wypozyczony=False
        self.rok_wydania=rok
        Ksiazka.__init__(self, tytul, autor)


biblio = Biblioteka(65)

liczba_ksiazek = int(input())
for x in range(liczba_ksiazek):
    ksiazka = eval(input())
    biblio.dodaj_egzemplarz_ksiazki( ksiazka[0], ksiazka[1], ksiazka[2])
biblio.dostepne_egz()
# biblio.wypozycz("jacek placek", "Chatka Puchatka")
# biblio.wypozycz("jacek placek", "Chatka Puchatka")
# ("Chatka Puchatka" , "Alan Alexander Milne" , 2014)
# ("Zhatka Puchatka" , "Alan Alexander Milne" , 2014)
# ("Ahatka Puchatka" , "Alan Alexander Milne" , 2014)
