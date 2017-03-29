import unittest
from testowane_rozwiazanie import Biblioteka

class TestLibraryApp(unittest.TestCase):
    def test_dodaj_egzemplarz_ksiazki(self):
        biblioteka = Biblioteka()
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2014)
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2015)
        biblioteka.dodaj_egzemplarz_ksiazki("Wladca Piercieni", "J. R. R. Tolkien", 1982)
        self.assertTrue(len(biblioteka.dostepne_egz("Potop")) == 2)
        self.assertTrue(len(biblioteka.raport_ksiazek()) == 2)

    def test_dodaj_egzemplarz_i_wypozycz(self):
        biblioteka = Biblioteka()
        for i in range(5):
            biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2000 + i)
        biblioteka.wypozycz("Piotr Kaluzny", "Potop")
        self.assertTrue(len(biblioteka.dostepne_egz("Potop")) == 4)
        self.assertTrue(len(biblioteka.pobierz_czytelnika("Piotr Kaluzny").wypozyczone) == 1)

    def testuj_limit_wypozyczen(self):
        biblioteka = Biblioteka()
        for i in range(5):
            biblioteka.dodaj_egzemplarz_ksiazki("Harry Potter czesc %d" % (i + 1), "J. K. Rowling", 1994 + i)
        for i in range(5):
            biblioteka.wypozycz("Piotr Kaluzny", "Harry Potter czesc %d" % (i + 1))
        self.assertTrue(len(biblioteka.pobierz_czytelnika("Piotr Kaluzny").wypozyczone) == 3)
        self.assertTrue(len(biblioteka.dostepne_egz("Harry Potter czesc 4")) == 1),
        self.assertTrue(len(biblioteka.dostepne_egz("Harry Potter czesc 5")) == 1)

    def testuj_drugi_egzemplarz_tej_samej_ksiazki(self):
        biblioteka = Biblioteka()
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2014)
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2015)
        biblioteka.wypozycz("Piotr Kaluzny", "Potop")
        biblioteka.wypozycz("Piotr Kaluzny", "Potop")
        self.assertTrue(len(biblioteka.pobierz_czytelnika("Piotr Kaluzny").wypozyczone) == 1)
        self.assertTrue(not biblioteka.dostepne_egz("Potop")[0].wypozyczony)

    def testuj_ksiazka_juz_wypozyczona(self):
        biblioteka = Biblioteka()
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2014)
        biblioteka.wypozycz("Piotr Kaluzny", "Potop")
        self.assertFalse(biblioteka.wypozycz("Michael Jordan", "Potop"))

    def testuj_oddanie_ksiazki(self):
        biblioteka = Biblioteka()
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2014)
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2015)
        biblioteka.wypozycz("Piotr Kaluzny", "Potop")
        ilosc_dostepnych_w_bibliotece_egzemplarzy_po_wypozyczeniu = len(biblioteka.dostepne_egz("Potop"))
        liczba_posiadanych_ksiazek_przez_czytelnika_po_wypozyczeniu =\
            len(biblioteka.pobierz_czytelnika("Piotr Kaluzny").wypozyczone)
        biblioteka.oddaj("Piotr Kaluzny", "Potop")
        self.assertTrue(len(biblioteka.dostepne_egz("Potop"))
                        > ilosc_dostepnych_w_bibliotece_egzemplarzy_po_wypozyczeniu)
        self.assertTrue(liczba_posiadanych_ksiazek_przez_czytelnika_po_wypozyczeniu
                        > len(biblioteka.pobierz_czytelnika("Piotr Kaluzny").wypozyczone))

    def testuj_oddanie_ksiazki_niewlasciwy_czytelnik(self):
        biblioteka = Biblioteka()
        biblioteka.dodaj_egzemplarz_ksiazki("Potop", "Henryk Sienkiewicz", 2014)
        biblioteka.wypozycz("Piotr Kaluzny", "Potop")
        self.assertFalse(biblioteka.oddaj("Steve Jobs", "Potop"))
        self.assertTrue(len(biblioteka.dostepne_egz("Potop")) == 0)
        self.assertTrue(len(biblioteka.pobierz_czytelnika("Piotr Kaluzny").wypozyczone) == 1)
        self.assertTrue(len(biblioteka.pobierz_czytelnika("Steve Jobs").wypozyczone) == 0)


if __name__ == '__main__':
    unittest.main()
