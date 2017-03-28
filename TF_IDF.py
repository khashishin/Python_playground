import sys
import math
from urllib.request import urlopen

def read_words(file_name):
    strip_signs_list = [',', '.', '\r', '\n', '-', '"', "'"]
    def delete_unallowed_signs(text):
        for ch in strip_signs_list:
            if ch in text:
                text = text.replace(ch, "")
        return text

    def open_file(filename):
        f = open(filename, 'r') # opens the csv file
        row_list = f.readlines()
        f.close()      # closing
        return row_list

    core_url = urlopen("http://150.254.36.78/diffs.txt")
    core_words_input = [l.decode("utf-8") for l in core_url.readlines()]
    core_words_dict = dict() # word : core

    line_word_occurence_dict = dict() # [ (document_number, count, is_title, no_terms),  ]
    relevancy_of_documents_dict = dict() # (document_number, query_number) : Relevant?(bool)
    documents_with_word = dict()
    searched_words_sets = dict()
    row_list = [delete_unallowed_signs(str(word.lower())) for word in open_file(file_name)]
    documents_int = int(row_list[0][0])
    lines_for_document = 2
    number_of_words = lines_for_document * documents_int
    document_lines_ending = 1 + number_of_words

    #Creating core words dict
    for item in core_words_input:
        new_item = item.split()
        core_words_dict[new_item[0]] = new_item[1]

    #Adding searched queries and mapping them to word sets {query : word_set}
    for i,line in enumerate(row_list[document_lines_ending+1:]):
        words_to_search_from_line = set(line.split())
        searched_words_sets[i+1] = words_to_search_from_line

    def count_words_from_line(line_nr, document_number, line_to_process, is_title):
            line_to_process = line_to_process.split()
            #check if either title or contents has all the required relevant worlds
            for query_number, word_set in searched_words_sets.items():
                if word_set.issubset(line_to_process):
                        relevancy_of_documents_dict[(document_number, query_number)] = True
                #check and change the word form
                for word in word_set:
                    if word in core_words_dict.keys():
                        word = core_words_dict[word]

                    count = line_to_process.count(word)
                    if count >0:
                       if is_title == False:
                           dict_key = 'content'
                       else:
                           dict_key = "title"
                       try:
                           #no_documtns (content/title) for given work, needed for idf
                           documents_with_word[(word,dict_key)].add(document_number)
                       except KeyError:
                           documents_with_word[(word, dict_key)] = set([document_number])

                    count_tuple = (line_nr, document_number, count, is_title, len(line_to_process))
                    try:
                        line_word_occurence_dict[word].append(count_tuple)
                    except KeyError:
                        line_word_occurence_dict[word] = [count_tuple]


    def calculate_tfidf(occured, length, word, is_title):
        if is_title == False:
            dict_key = 'content'
        else:
            dict_key = "title"
        tf = float(occured)/length
        idf = math.log( float(documents_int) / len(documents_with_word[(word,dict_key)]))
        # print (word, documents_int*lines_for_document)
        tfidf = float(tf * idf)
        if is_title==True:
            tfidf = 2*tfidf
        return tfidf

    document_id = 0
    #Creating occurencies tuples when iterating over content lines
    for i, line in enumerate(row_list[1:1+number_of_words]):
        if i % 2 == 0:
            count_words_from_line(i, document_id, line, True)
        else:
            count_words_from_line(i, document_id, line, False)
            document_id+=1

    for query_number, word_set in searched_words_sets.items():     # for each query
        result_list =[]
        for document in range(documents_int):         # for each document presented
            try:
                if relevancy_of_documents_dict[(document,query_number)] == True:  #if it is relevant
                    tf_idf_list = [] # create TF list, value for each word (from word_set) from query
                    for word in word_set:
                        for tuple in line_word_occurence_dict[word]: #check for occurrences of every word
                            if tuple[1]==document: # if we are on a right document
                                tfidf = calculate_tfidf(occured =tuple[2], length = tuple[4],word = word, is_title= tuple[3])
                                # print ("word", word,"in line", tuple[0], "in doc", tuple[1], "occured", tuple[2], "is title? -",tuple[3], "and line has", tuple[4], "words in it and tfidf=", tfidf)
                                tf_idf_list.append(tfidf)

                    result_list.append((query_number,document,float(sum(tf_idf_list))))
            except KeyError:
                #not relevant - doesnt exist
                continue

        # print("query", query_number)
        result_list = (sorted(result_list, key = lambda result_list: (result_list[2], result_list[1]), reverse=True))
        # Sortowane jest po tf-idf a potem po kolejności dokumentów a nie linii ale to to samo....
        # print (result_list)
        print ([result[1] for result in result_list])


if __name__ == "__main__":
    read_words(sys.argv[1])

