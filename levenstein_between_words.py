import sys

# import numpy as np
# dim = 2
# matrix = np.zeros((len(words[0]), len(words[1])), dtype=np.int)


def calculate_levenstein(word1,word2):
    kolumny = len(word2) +1
    wiersze = len(word1) +1

    levenstein_matrix = [[0 for x in range(kolumny)] for y in range(wiersze)]

    if wiersze-1 == 0:
        return len(word2)
    if kolumny-1 == 0:
        return len(word1)

    for kol in range(1, wiersze):
        levenstein_matrix[kol][0] = kol

    for wie in range(1, kolumny):
        levenstein_matrix[0][wie] = wie

    for j in range(1,kolumny):
        for i in range(1,wiersze):
            substitution_cost = 0 if word1[i-1] == word2[j-1] else 1
            levenstein_matrix[i][j] = min(levenstein_matrix[i-1][j] +1,
                                          levenstein_matrix[i][j-1] +1,
                                          levenstein_matrix[i-1][j-1] + substitution_cost )

    return levenstein_matrix[wiersze-1][kolumny-1]

# Wersja obrócona, dla treningu zrozumienia ;)
# def calculate_levenstein(word1,word2):
#     kolumny = len(word1) +1
#     wiersze = len(word2) +1

#     levenstein_matrix = [[0 for x in range(kolumny)] for y in range(wiersze)]

#     if wiersze-1 == 0:
#         return len(word2)
#     if kolumny-1 == 0:
#         return len(word1)

#     for kol in range(1, kolumny):
#         levenstein_matrix[0][kol] = kol

#     for wie in range(1, wiersze):
#         levenstein_matrix[wie][0] = wie


#     for j in range(1,wiersze):
#         for i in range(1,kolumny):
#             substitution_cost = 0 if word1[i-1] == word2[j-1] else 1
#             levenstein_matrix[j][i] = min(levenstein_matrix[j-1][i] +1,
#                                           levenstein_matrix[j][i-1] +1,
#                                           levenstein_matrix[j-1][i-1] + substitution_cost )
#     return levenstein_matrix[wiersze-1][kolumny-1]

print (calculate_levenstein(sys.argv[1], sys.argv[2]))