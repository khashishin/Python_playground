import sys
import math
import numpy
from urllib.request import urlopen
# kolumny to dokumenty, bdzie mniej wierszy bo sa skorelowane
# V to już V' , wypisać sobie po przemnożeniu rezultat

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

    row_list = [delete_unallowed_signs(str(word.lower())) for word in open_file(file_name)]
    documents_int = int(row_list[0][0])
    words_to_search = row_list[-2].split()
    documents = row_list[1:-2]
    k=r=int(row_list[:-1][0])
    print (documents)

    C = [[0 for word in words_to_search ] for document in documents]
    for i, document in enumerate(documents):
        for index_of_word, word in enumerate(words_to_search):
            C[i][index_of_word] = 1 if word in document.split() else 0

    C = numpy.matrix(C)
    U,s,V = numpy.linalg.svd(C) # SVD decomposition

    S = [[0 for sigma in range(len(s))] for i in range(len(s))]
    for i, row in enumerate(S):
        S[i][i] = s[i]

    for d_index, document in enumerate(S):
        if d_index > k:
            S[d_index]=[0 for i in S[d_index]]

read_words("SVD_matrix_decomposition_input.txt")