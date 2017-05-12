from urllib import request
from bs4 import BeautifulSoup
import json
import csv
import re
import datetime
import time
from random import choice

app_id = "1050560361741404"
app_secret = "2c573ede1a1d80cb5f2752aac94d787e" # DO NOT SHARE WITH ANYONE!
access_token = app_id + "|" + app_secret

pages_list = ["lincolnreport", "RHobbusJD", "theEagleisRising", "FreedomDailyNews"]
number_of_api_tries = 2
do_print= True

searched_words = ["clinton", "trump"]


def save_json_to_csv(json_data):
    with open('result.json', 'w') as outfile:
        json.dump(json_data, outfile)

def request_until_succeed(url):
    '''
    Metoda ktora probuje wykonac zapytanie na danej stronie, dopoki nie otrzyma odpowiedzi z sukcesem
    '''
    req = request.Request(url)
    success = False
    tries_unsuccesfull = 0
    while success is False:
        try: 
            response = request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception:
            tries_unsuccesfull +=1
            time.sleep(1)
            #print ("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print ("Error accessing url query")
            if tries_unsuccesfull > number_of_api_tries:
                return False
    return response.read()

def browse_API(query):
    '''
    Wyszukaj API facebooka z zadanym zapytaniem 
    '''
    base = "https://graph.facebook.com/v2.9"
    token = "&access_token={}".format(access_token)
    url = base + query + token
    if do_print:print("Querying url:" , url)
    try:
        data = json.loads(request_until_succeed(url))    
        return data
    except TypeError:
        #Null
        return False

def get_posts_and_statistics_json(page_id, access_token, posts_limit):
    '''
    Wykorzystujac zapytanie, korzystamy z metody browse_API z zadanym naszym query, zeby zwrocic wszystkie posty ze strony
    Zbieramy tez statystyki dot. komentarzy i lajków 
    '''
    fields_searched = "id,message,link,shares,since=1464739200,until=1477872000,comments.limit(0).summary(true),likes.limit(0).summary(true)"
    node = "/" + page_id
    query = "/posts/?fields={}&limit={}".format(fields_searched,posts_limit)
    url = node + query
    #save_json_to_csv(data)
    return browse_API(url)

site_content_mapping= {"dailysign.al/" : ("div", "class", "tds-content"),
						"dailysignal.com/" : ("div", "class", "tds-content")
                        } # strona : miejsce gdzie ma tresc artykulu

def get_base_from_link(link):
    '''
    Wybiera główną stronę na podstawie długiego linku np http://www.wyborcza.pl/moj-kot-zjadl-mi-sniadanie i wskazuje na wyborcza.pl, abstrachuje od protokołu
    '''
    link_parts = link.split('/')
    protocol = link_parts[0]
    host = link_parts[2]
    url = host +"/"
    #Nie zwraca http/https zeby uniknac podwojnego mapowania w site_content_mapping -> trzeba by bylo uwzglednic obie wersje
    return url

def read_webpage(adres_html):
    '''
    Metoda odczytuje strone za pomoca urllib i zwraca jej kod HTML, wykorzystuje User-Agent zeby sie podszyc pod przegladarke
    '''
    header_list = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},
                      {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'},
                      {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"},
                      {"User-Agent": 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
                      {"User-Agent": 'Opera/9.25 (Windows NT 5.1; U; en)'},
                      {"User-Agent": 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'}]
    header = choice(header_list) #wylosuj header tak zeby strona sie nie burzyla ze przeszukuje ja crawler
    try:
        req = request.Request(adres_html, None,headers=header)
        read_webpage = BeautifulSoup(request.urlopen(req).read(), "html.parser")
    except urllib.error.HTTPError:
        return
    return read_webpage

def delete_unallowed_signs(line):
    '''
    Czyta wybrana linie tekstu, usuwa znaki niedozwolone
    '''
    list_of_deleted_character = set([',', '.', '\r', '\n', '-', '"', "'", "/", "/", ":", "”", "„", "(", ")", "@", "_", "–", "*", "?", "…", "+", "“" , "#", "’", "&"])
    for ch in list_of_deleted_character:
        if ch in line:
            line = line.replace(ch, "")
    return line

def prepare_line(line):
    """
    Zamienia linie na slowa, usuwa znaki
    wejscie: Pan Jan lubi jezdzic samochodem, ale lubi tez pomarancze, wczoraj zjadl obiad!
    wyjscie: [pan, jan, lubi,...]
    """
    line = delete_unallowed_signs(line)
    line= line.lower()
    line = line.split()
    return line

def get_link_content(link):
    '''
    Zczytywanie tresci strony z linka.
    Najpierw szukamy strony bazowej (base_webpage)
    Potem wczytujemy ja, szukamy tekstu za pomoca naszego mapowania w slowniku site_content_mapping
    Wczytujemy tresc (article_text)
    Dzielimy na linie i slowa, i przygotowujemy kazda linie, 
    gotowa tresc (lista slow w liniach) jest dostepna w prepared_article_lines
    '''

    base_webpage = get_base_from_link(link)
    #print (link, base_webpage)
    if base_webpage in site_content_mapping.keys():
        page = read_webpage(link)
        searched_element = site_content_mapping[base_webpage][0]
        searched_parameter = site_content_mapping[base_webpage][1]
        searched_value = site_content_mapping[base_webpage][2]
        try:
            # Przyklad, szukamy DIV'a (element) z klasa (parametr) ktora ma wartosc "node-content"
            article_text = page.findAll(searched_element, {searched_parameter : searched_value}) # wyszukana tresc artykulu

            prepared_article_lines = []
            for element in article_text: # Dla kazdej linii w przetworzonym tekscie artykulu
                word_list = prepare_line(element.text)
                prepared_article_lines.add(word_list) # !!!!!!!TU SIE NA RAZIE KONCZY DZIALANIE PROGRAMU!!!!!!
        except AttributeError:
            # Nie znaleziono tekstu artyulu na stronie albo cos sie wywalilo
            pass

        return prepared_article_lines
    else:
        if do_print:print ("webpage " + base_webpage, " not in mapping")
        return ["Null"]
        
 

for page_id in pages_list:
    posts_limit = 100
    posts = get_posts_and_statistics_json(page_id, access_token, posts_limit)
    #print (json.dumps(posts, indent=2, sort_keys=True))

    for post in posts["data"]:
        #print(post["message"]) #wiadomosc
        #print(post["comments"]["summary"]["total_count"]) #liczba komentarzy
        #print(post["likes"]["summary"]["total_count"]) #liczba likeow
        #print(post["shares"]["count"]) #liczba shareow
        # print (post)
        # (message, link, num_of_comments, num_of_likes, num_of_shares)
        # (post["message"], post["link"] post["comments"]["summary"]["total_count"], post["likes"]["summary"]["total_count"], post["shares"]["count"])

        try:
            content = post["message"]    
            #print (prepare_line(content)) # LISTA SLOW W NEWSIE
            title_words = [word for word in prepare_line(content)]
            

            for word in title_words:
                if word in searched_words: # TUTAJ sprawdzamy czy post zawiera slowa ktorych szukamy -> hilary/trump

                    if word =="trump":
                        print ("O trumpie")
                    if word =="clinton":
                        print ("O clinton")

                    print ("TAK ZNALAZLEM SUPER LINK O TRUMPIE/CLINTON")
                    #link = []
                    #link = re.findall('(?:http|https)(?:\:\/\/)(?:(?:[\w+-.\/]+))', str(content))  #link w tresci posta
                    link = (post["link"]) # link w poscie (chyba to lepsze)
                    article_content = get_link_content(link)
                    # (post["message"], post["link"] post["comments"]["summary"]["total_count"], post["likes"]["summary"]["total_count"], post["shares"]["count"], article_content)
                    break
        except KeyError:
            if do_print:print ("Found post that couldnt process", str(post))

