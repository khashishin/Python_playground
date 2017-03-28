import sys
import re

query = re.compile(r"(?:[^\.\s])[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+@\w+\.\w{1,6}|"
                   r"(?:[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]\\ {1}[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+)+@\w+\.\w{1,6}|"
                   r"(?:[\"\”])(?:\b(?<!\.))(?:[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@\\\ ]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@\\\ ]+)+(?:[\"\”])@\w+\.\w{1,6}")


test=sys.argv[1]
# test= 'My new e-mail address is $A12345@example.com and not ”Fred B”@example.com name..surname@example.com Fred\ Bl\ oggs@example.com"'
print (sorted(re.findall(query, test),reverse=True))


#2 sposob, omija niestety specjalne znaki na poczatku maila, ze wzgledu na \b
# ?: <- powoduje ze grupa nie jest brana pod uwage jako wynik, pomaga poradzic sobie z metodami biblioteki re ktore domyslnie zwracaja grupy
# (?:\b(?<!\.) <- poczatek slowa nie poprzedzony kropka = wyraz nie zaczyna sie od .
# ([\w]+[\.]?[\w]+) <- grupa znakow ktora jest oddzielona kropkami, nie bierze pod uwage 2 kropek po sobie
# (  ([\w]+[\.]?[\w]+)\\ {1}([\w]+[\.]?[\w]+)  )+ <- wyrazy ktore dodatkowo moga byc oddzielone "\ "

# Podstawowe słowa -
# (?:(?:\b(?<!\.)[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+)+@\w+\.\w{1,6})
#
# Słowa z wyescapowana spacja (musi to byc ciag znakow ktory moze, ale nie musi miec pomiedzy spacje
# (?:(?:\b(?<!\.))[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]\\ {1}[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+)+@\w+\.\w{1,6}
#
# 1 + 2
# (?:(?:\b(?<!\.))[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@](?:\\ )?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@]+)+@\w+\.\w{1,6}
#
# Cudzyslowia
# (?:[\"\”])(?:\b(?<!\.))(?:[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@\\\ ]+[\.]?[\w\_\+\-\\\=\/\$\!\%\#\&\*\?\^\{\}\~\|\@\\\ ]+)+(?:[\"\”])@\w+\.\w{1,6}