import operator
import math
import sys

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

def most_common(lst):
    return max(set(lst), key=lst.count)

def get_cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def get_tf(term, document):
    try:
        return document.count(term) / len(document.split())
    except ZeroDivisionError:
        return 0

def get_idf(term, corpus_all_wordlist):
    try:
        return len(corpus_all_wordlist) / sum([term in document for document in corpus_all_wordlist])
    except ZeroDivisionError:
        return 0

def calculate_knn_classification(file_name):
	row_list = [delete_unallowed_signs(str(word.lower())) for word in open_file(file_name)]
    amount_of_documents = int(row_list[0])
    documents = row_list[1:amount_of_documents + 1]
    class_assignment_for_documents = [int(i) for i in row_list[amount_of_documents + 1].split()]
    query = row_list[amount_of_documents + 2]
    k_nearest_neigh = int(row_list[-1])
    corpus = ' '.join(documents).split()

    #Vectorisation of documents to tf-idf vectors
    documents_as_tfidf_vectors = []
    for document in documents:
        tf_idf_vector = []
        for term in document.split():
            tf_idf_for_term = get_tf(term, document) * get_idf(term, corpus)
            tf_idf_vector.append(tf_idf_for_term)
        documents_as_tfidf_vectors.append(tf_idf_vector)
    target_doc_tf_idf_vector = []
    for term in query.split():
        tf_idf_for_term = get_tf(term, query) * get_idf(term, corpus)
        target_doc_tf_idf_vector.append(tf_idf_for_term)

    #Calculating cos dist of tfids vectors of documents with query
    cos_distances = []
    for i, tfidf_vector in enumerate(documents_as_tfidf_vectors):
        cos_dist = get_cosine_similarity(target_doc_tf_idf_vector, tfidf_vector)
        cos_distances.append((i, cos_dist, class_assignment_for_documents[i]))

    sorted_cos_distances = sorted(cos_distances, key=operator.itemgetter(1))
    class_assignment_list = []

    #Classifying document to class of his N nearest neighbours
    for doc in range(k_nearest_neigh):
        class_assignment_list.append(sorted_cos_distances[doc][2])
    most_probable_class = most_common(class_assignment_list)
    probability_new_document_is_a_part_of_this_class = class_assignment_list.count(most_probable_class) / len(class_assignment_list)

    if probability_new_document_is_a_part_of_this_class >= 0.5:
        print(1)
    else:
        print(0)


if __name__ == '__main__':
	#"KNN_input.txt"
	file_name = sys.argv[1]
    calculate_knn_classification(file_name)