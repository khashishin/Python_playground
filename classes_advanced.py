class Drzewo:
    def __init__(self, lista_krotek):
        self.lista = list(lista_krotek)
        self.prosta = MiaraProsta()
        self.potegowa = MiaraPotegowa()
        self.wierzcholki = self.zmapuj_wierzcholki()
        self.korzen = self.pobierz_korzen()

    def zmapuj_wierzcholki(self):
        lista_wierzcholkow = []
        for node in self.lista:
            if node[0] not in lista_wierzcholkow:
                lista_wierzcholkow.append(node[0])
            if node[1] not in lista_wierzcholkow:
                lista_wierzcholkow.append(node[1])

        return lista_wierzcholkow

    def pobierz_korzen(self):
        lista_wierzcholkow = self.wierzcholki
        for node in self.lista:
            lista_wierzcholkow.remove(node[1])
        return lista_wierzcholkow[0]

    def pobierz_nadkoncepty(self, wierzcholek ,nadkoncepty_poprzednie = 0):
        if nadkoncepty_poprzednie == 0:
            nadkoncepty = [wierzcholek]
        else:
            nadkoncepty = nadkoncepty_poprzednie

        if wierzcholek == self.korzen:
            return nadkoncepty

        for node in self.lista:
            if node[1] == wierzcholek:
                nadkoncepty.append(node[0])
                return self.pobierz_nadkoncepty(node[0], nadkoncepty)

    def oblicz_odleglosc(self, wierzcholek1, wierzcholek2, miara):
        nadwezly1 = self.pobierz_nadkoncepty(wierzcholek1)
        nadwezly2 = self.pobierz_nadkoncepty(wierzcholek2)
        odleglosc = 0
        if miara== "prosta":
            miara_odleglosci = self.prosta
        if miara=="potegowa":
            miara_odleglosci = self.potegowa

        return miara_odleglosci.licz_odleglosc(nadwezly1, nadwezly2)


class MiaraProsta:
    def licz_odleglosc(self, nadwezly1, nadwezly2):
        najblizszy_sasiad = None
        for wezel in nadwezly1:
            if wezel in nadwezly2:
                najblizszy_sasiad = wezel
                break
        odleglosc = nadwezly1.index(najblizszy_sasiad) + nadwezly2.index(najblizszy_sasiad)
        return odleglosc

class MiaraPotegowa:
    def licz_odleglosc(self, nadwezly1, nadwezly2):
        najblizszy_sasiad = None
        for wezel in nadwezly1:
            if wezel in nadwezly2:
                najblizszy_sasiad = wezel
                break
        wezel_1=nadwezly1.index(najblizszy_sasiad)
        wezel_2=nadwezly2.index(najblizszy_sasiad)
        odleglosc = sum([2**x for x in range(wezel_1)]) + sum([2**x for x in range(wezel_2)])
        return odleglosc

if __name__ == "__main__":
    drzewo = eval(input())
    input_wierzcholki = eval(input())
    lista_odleglosci = []
    d = Drzewo(drzewo)
    for input in input_wierzcholki:
        lista_odleglosci.append(d.oblicz_odleglosc(input[1], input[2], input[0]))
    print(lista_odleglosci)
