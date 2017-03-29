liczba_figur = int(input())
import math

class Kolo:
    def __init__(self, promien):
        self.promien=float(promien)
        self.wylicz_pole()
    
    def wylicz_pole(self):
        self.pole=(self.promien**2) * math.pi
        
class Prostokat:
    def __init__(self, bok_a, bok_b):
        self.bok_a=float(bok_a)
        self.bok_b=float(bok_b)
        self.wylicz_pole()
    
    def wylicz_pole(self):
        self.pole=self.bok_a*self.bok_b 
        
class Trojkat:
    def __init__(self, bok_a, bok_b,bok_c):
        self.bok_a=float(bok_a)
        self.bok_b=float(bok_b)
        self.bok_c=float(bok_c)
        self.wylicz_pole()
    
    def wylicz_pole(self):
        p = 1/2 * (self.bok_a+self.bok_b+self.bok_c)
        self.pole=math.sqrt(p * (p - self.bok_a) * (p - self.bok_b) * (p - self.bok_c) )

lista_wynikow=[]
suma_pol=0
for i in range(liczba_figur):
    dane_figury = input().split(" ")
    if len(dane_figury)==3:
        trojkat = Trojkat(*dane_figury)
        suma_pol+=trojkat.pole
    elif len(dane_figury)==2:
        prostokat = Prostokat(*dane_figury)
        suma_pol+=prostokat.pole
    elif len(dane_figury)==1:
        kolo = Kolo(dane_figury[0])
        suma_pol+=kolo.pole
    else:
        continue
    

print (round(suma_pol,2))


