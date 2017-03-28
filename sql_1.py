import pymysql
host = input()
port= int(input())
uzytk = input()
haslo = input()
baza = input()

connection = pymysql.connect(host=host, port = port , user=uzytk, passwd= haslo, database = baza )
cursor = connection.cursor()
cursor.execute('select sum(duration) from polaczenia;')
for i in cursor:
    print((i[0]))
