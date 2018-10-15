import operator
from urllib.request import urlopen
import sys

prepared_lines = []
queries = []
filepath = sys.argv[1]

def prepare_lines():
    with open(filepath, 'r') as in_file:
        lines = in_file.readlines()
    for line in lines:
        prepared_line = line
        prepared_line = prepared_line.replace('.', '')
        prepared_line = prepared_line.replace(',', '')
        prepared_line = prepared_line.replace('\n', '')
        prepared_line = prepared_line.lower()
        prepared_lines.append(prepared_line)
    query_amount = int(prepared_lines[int(prepared_lines[0]) * 2 + 1])
    for q in range(query_amount):
        queries.append(prepared_lines[-query_amount + q])
    del prepared_lines[0]
    del prepared_lines[-query_amount - 1:]


def replace_lemma(lines):
    f = urlopen("http://150.254.36.78/diffs.txt")
    ls = [l.decode("utf-8") for l in f.readlines()]
    lemmas = dict()
    for line in ls:
        x = line.split(" ")
        y = [v.replace("\n", "") for v in x if v != ""]
        lemmas[y[0]] = y[1]

    replaced_lemmas_lines = []
    for line in lines:
        replaced_line = []
        for word in line.split():
            try:
                replaced_line.append(lemmas[word])
            except KeyError:
                replaced_line.append(word)
        replaced_lemmas_lines.append(replaced_line)
    return replaced_lemmas_lines


def get_tf(term, document):
    return document.count(term) / len(document.split())


def get_idf(term, documents):
    try:
        return len(documents) / sum([term in document for document in documents])
    except ZeroDivisionError:
        return 0

prepare_lines()
prepared_lines = replace_lemma(prepared_lines)

documents = dict()
amount_of_documents = int(len(prepared_lines) / 2)
topics = prepared_lines[0::2]
contents = prepared_lines[1::2]
for i in range(amount_of_documents):
    documents[(i, ' '.join(topics[i]), ' '.join(contents[i]))] = {}

for query in queries:
    query_result = {}
    results_indexes = []
    for document in documents:
        measure = 0
        for word_of_query in query.split():
            measure_for_word = 2 * (get_tf(word_of_query, document[1]) * get_idf(word_of_query, topics)) \
                      + get_tf(word_of_query, document[2]) * get_idf(word_of_query, contents)
            measure += measure_for_word
        query_result[document[0]] = measure
    sorted_result = sorted(query_result.items(), key=operator.itemgetter(1), reverse=True)
    for index, relevancy in sorted_result:
        if relevancy > 0:
            results_indexes.append(index)
    print(results_indexes)

