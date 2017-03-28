import pymysql
import datetime

host = input()
port= int(input())
uzytk = input()
haslo = input()
baza = input()
nadawcy = eval(input())
odbiorcy = eval(input())

connection = pymysql.connect(host=host,
    port = port, user=uzytk, passwd=haslo,
    database=baza)
cursor = connection.cursor()

tupla_nadawcy = []
tupla_odbiorcy = []
for nadawca in nadawcy:
    cursor.execute('select sum(duration) from polaczenia where from_subscriber = {}'.format(nadawca))
    tupla_nadawcy.append(int(cursor.fetchone()[0]))
for odbiorca in odbiorcy:
    cursor.execute('select max(datetime) from polaczenia where to_subscriber ={}'.format(odbiorca))
    tupla_odbiorcy.append(cursor.fetchone()[0].isoformat())

print (tuple(tupla_nadawcy))
print (tuple(tupla_odbiorcy))

# tabela polaczenia
# ('from_subscriber', 'int(11)', 'NO', 'MUL', None, '')
# ('to_subscriber', 'int(11)', 'NO', 'MUL', None, '')
# ('datetime', 'datetime', 'NO', '', None, '')
# ('duration', 'int(11)', 'NO', '', None, '')
# ('celltower', 'int(11)', 'NO', 'MUL', None, '')
