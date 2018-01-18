#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import json
import csv
import re
import datetime
import time
from random import choice

#Obsluga aplikacji -> dostep do API FB
app_id = ""
app_secret = "" # DO NOT SHARE WITH ANYONE!
access_token = app_id + "|" + app_secret

#Podstawowe zmienne
pages_list = ["lincolnreport", "RHobbusJD", "theEagleisRising", "FreedomDailyNews"]
number_of_api_tries = 2
do_print= True

################################################################################################################
                        ############################ ROZNE FUNKCJE ############################
def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 }).encode('utf-8')

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

def save_json_to_csv(json_data):
    with open('result.json', 'w') as outfile:
        json.dump(json_data, outfile)

################################################################################################################
                        ############################ API FB i obsługa Webowa ############################
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
            print ("{}: Error for URL {}".format(datetime.datetime.now(), url))
            # if tries_unsuccesfull > number_of_api_tries:
            #     return False
    return response.read()

def browse_API(query):
    '''
    Wyszukaj API facebooka z zadanym zapytaniem 
    Returns: dane(json) z wynikiem zapytania do API, albo False (nie zadzialalo)
    '''
    base = "https://graph.facebook.com/v2.9"
    token = "&access_token={}".format(access_token)
    url = base + query + token
    if do_print:print("Querying url:" , url)
    try:
        data = json.loads(request_until_succeed(url))    
        return data
    except TypeError:
        #Null result - unsuccessfull request
        return False

def get_posts_and_statistics_json(page_id, access_token, posts_limit):
    '''
    DEFINICJA ZAPYTANIA DO API FB
    Wykorzystujac zapytanie, korzystamy z metody browse_API z zadanym naszym query, zeby zwrocic wszystkie posty ze strony
    Zbieramy tez statystyki dot. komentarzy i lajkow 
    '''
    #fields_searched = "id,message,link,permalink_url, created_time, type, name, shares, comments.limit(0).summary(true), likes.limit(0).summary(true),since=1464739200,until=1477872000"
    #fields_searched = "id,message,link,permalink_url,created_time,type,name,shares,comments.limit(1).summary(true), reactions.limit(1).summary(true)"
    fields_searched = "message,link,created_time,shares,comments.limit(0).summary(true),likes.limit(0).summary(true),since=1464739200,until=1477872000"
    node = "/" + page_id
    query = "/posts/?fields={}".format(fields_searched) #&limit={}
    url = node + query
    return browse_API(url)

################################################################################################################
                        ############################ Zczytywanie tresci stron ############################

#CZYTANIE TRESCI STRON
# def read_webpage(adres_html):
#     '''
#     Metoda odczytuje strone za pomoca urllib i zwraca jej kod HTML, wykorzystuje User-Agent zeby sie podszyc pod przegladarke
#     '''
#     header_list = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},
#                       {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'},
#                       {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"},
#                       {"User-Agent": 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
#                       {"User-Agent": 'Opera/9.25 (Windows NT 5.1; U; en)'},
#                       {"User-Agent": 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'}]
#     header = choice(header_list) #wylosuj header tak zeby strona sie nie burzyla ze przeszukuje ja crawler
#     try:
#         req = request.Request(adres_html, None,headers=header)
#         read_webpage = BeautifulSoup(request.urlopen(req).read(), "html.parser")
#     except urllib.error.HTTPError:
#         return
#     return read_webpage

# site_content_mapping= {"dailysign.al/" : ("div", "class", "tds-content"),
# 						"dailysignal.com/" : ("div", "class", "tds-content")
#                         } # strona : miejsce gdzie ma tresc artykulu
#
# def get_base_from_link(link):
#     '''
#     Wybiera glowną stronę na podstawie długiego linku np http://www.wyborcza.pl/moj-kot-zjadl-mi-sniadanie i wskazuje na wyborcza.pl, abstrachuje od protokołu
#     '''
#     link_parts = link.split('/')
#     protocol = link_parts[0]
#     host = link_parts[2]
#     url = host +"/"
#     #Nie zwraca http/https zeby uniknac podwojnego mapowania w site_content_mapping -> trzeba by bylo uwzglednic obie wersje
#     return url
#
# def get_link_content(link):
#     '''
#     Zczytywanie tresci strony z linka.
#     Najpierw szukamy strony bazowej (base_webpage)
#     Potem wczytujemy ja, szukamy tekstu za pomoca naszego mapowania w slowniku site_content_mapping
#     Wczytujemy tresc (article_text)
#     Dzielimy na linie i slowa, i przygotowujemy kazda linie, 
#     gotowa tresc (lista slow w liniach) jest dostepna w prepared_article_lines
#     '''
#     base_webpage = get_base_from_link(link)
#     #print (link, base_webpage)
#     if base_webpage in site_content_mapping.keys():
#         page = read_webpage(link)
#         searched_element = site_content_mapping[base_webpage][0]
#         searched_parameter = site_content_mapping[base_webpage][1]
#         searched_value = site_content_mapping[base_webpage][2]
#         try:
#             # Przyklad, szukamy DIV'a (element) z klasa (parametr) ktora ma wartosc "node-content"
#             article_text = page.findAll(searched_element, {searched_parameter : searched_value}) # wyszukana tresc artykulu

#             prepared_article_lines = []
#             for element in article_text: # Dla kazdej linii w przetworzonym tekscie artykulu
#                 word_list = prepare_line(element.text)
#                 prepared_article_lines.add(word_list) # !!!!!!!TU SIE NA RAZIE KONCZY DZIALANIE PROGRAMU!!!!!!
#         except AttributeError:
#             # Nie znaleziono tekstu artyulu na stronie albo cos sie wywalilo
#             pass

#         return prepared_article_lines
#     else:
#         if do_print:print ("webpage " + base_webpage, " not in mapping")
#         return ["Null"]
        
################################################################################################################
                        ############################ Obsługa wyników i szukanie relewantnych postów ############################
def check_if_relevant(content): 
        '''
        Sprawdza czy post jest relewantny, na podstawie wyszukiwania slow, zwraca fraze ktorej szukamy
        albo zwraca False jak jej nie znajdzie
        returns: "Trump" albo "Clinton" albo "Trump+Clinton" albo False
        '''
        trump = False
        clinton = False
        title_words = [word for word in prepare_line(str(content))]
        if "trump" in title_words or "donald" in title_words:
            trump = True
            print ("TRUMP")
        if "clinton" in title_words or "hilary" in title_words:
            clinton = True
            print ("CLINTON")
        if trump and clinton:
            return "Trump+Clinton"
        else:
            if trump:
                return "Trump"
            if clinton:
                return "Clinton"
            else:
                return False

def processFacebookPageFeedStatus(status, access_token):
    '''
    Sprawdza status ktory otrzymal z FB - ktory jest jsonem (de facto slownikiem tutaj)
    Szuka poszczegolnych informacji -> linka, liczby lajkow itd
    '''
    status_message = '' if 'message' not in status.keys() else unicode_normalize(status['message'])
    relevant = check_if_relevant(status_message)
    if relevant: #Sprawdza czy jest to relewantny link (o Trumpie albo Clinton)
        
        type_of_message = relevant #Typ newsa ("Trump", "Clinton", "Trump+Clinton")
        # link_name = '' if 'name' not in status.keys() else unicode_normalize(status['name'])
        status_link = '' if 'link' not in status.keys() else unicode_normalize(status['link'])
        
        #Doprowadzenie czasu do ludzkiej formy
        status_published = datetime.datetime.strptime(
                status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
        status_published = status_published + \
                datetime.timedelta(hours=-5) # EST
        status_published = status_published.strftime(
                '%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs

        num_likes = 0 if 'likes' not in status else \
                status['likes']['summary']['total_count']
        num_comments = 0 if 'comments' not in status else \
                status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status else status['shares']['count']

        # !!!!!!!!REAKCJE - nie działa, na wypadek potrzeby trzeba sprawdzić czemu!!!!!!!!

        # Counts of each reaction separately; good for sentiment
        # Only check for reactions if past date of implementation:
        # http://newsroom.fb.com/news/2016/02/reactions-now-available-globally/
        # reactions = getReactionsForStatus(status_id, access_token) if \
        #         status_published > '2016-02-24 00:00:00' else {}
        # num_likes = 0 if 'like' not in reactions else \
        #         reactions['like']['summary']['total_count']
        # Special case: Set number of Likes to Number of reactions for pre-reaction
        # statuses
        # num_likes = num_reactions if status_published < '2016-02-24 00:00:00' \
                # else num_likes

        # def get_num_total_reactions(reaction_type, reactions):
        #     if reaction_type not in reactions:
        #         return 0
        #     else:
        #         return reactions[reaction_type]['summary']['total_count']

        # num_loves = get_num_total_reactions('love', reactions)
        # num_wows = get_num_total_reactions('wow', reactions)
        # num_hahas = get_num_total_reactions('haha', reactions)
        # num_sads = get_num_total_reactions('sad', reactions)
        # num_angrys = get_num_total_reactions('angry', reactions)
        return (type_of_message, str(status_message.decode('utf-8')), str(status_link), status_published, num_shares, num_comments, num_likes)
    else:
        return False

# def getReactionsForStatus(status_id, access_token):
#     # See http://stackoverflow.com/a/37239851 for Reactions parameters
#         # Reactions are only accessable at a single-post endpoint

#     base = "https://graph.facebook.com/v2.6"
#     node = "/%s" % status_id
#     reactions = "/?fields=" \
#             "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
#             ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
#             ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
#             ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
#             ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
#             ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
#     parameters = "&access_token=%s" % access_token
#     url = base + node + reactions + parameters

#     # retrieve data
#     data = json.loads(request_until_succeed(url))
#     return data

def scrapeFacebookPageFeedStatus(page_id, access_token):
    with open('facebook_statuses_{}.csv'.format(page_id), 'w') as file:
        w = csv.writer(file)
        w.writerow(["content_type","message","link","created_time","shares","comments","likes"])
        
        if do_print:
            num_processed = 0
            scrape_starttime = datetime.datetime.now()
            print ("Scraping {} Facebook Page: {}".format(page_id, scrape_starttime))
        
        has_next_page = True # Wykorzystywane do przeszukiwania i sprawdzania czy jest nastepna strona
        posts = get_posts_and_statistics_json(page_id, access_token, 100) #Scrapuje posty i tez wszystkie kolejne strony
        while has_next_page:
            try:
                for status in posts['data']:
                    relevant_post = processFacebookPageFeedStatus(status,
                            access_token)
                    if relevant_post != False: #False oznacza ze jest to dla nas news nierelewantny
                        print("writing row")
                        w.writerow(relevant_post) # Zapisuje wszystkie statystyki
                        if do_print: num_processed += 1
                if 'paging' in posts.keys(): #Jezeli ma wiecej stron
                    print ("DOING NEXT PAGE")
                    posts = json.loads(request_until_succeed(posts['paging']['next']))
                else:
                    has_next_page = False
            except TypeError: 
                has_next_page = False

        if do_print: print ("Done! {} statuses processed in {}".format(num_processed, datetime.datetime.now() - scrape_starttime))

################################################################################################################
                        ############################ Runner ############################
for page_id in pages_list:
    scrapeFacebookPageFeedStatus(page_id, access_token)
