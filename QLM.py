import sys
import operator

def open_file(filename):
    f = open(filename, 'r')
    row_list = f.readlines()
    f.close()      # closing
    return row_list

strip_signs_list = [',', '.', '\r', '\n', '-', '"', "'"]
def delete_unallowed_signs(text):
    for ch in strip_signs_list:
        if ch in text:
            text = text.replace(ch, "")
    return text

prepared_lines = [delete_unallowed_signs(str(word.lower())) for word in open_file(file_name)]
amount_of_documents = int(prepared_lines[0])
documents = prepared_lines[1:amount_of_documents+1]
query = prepared_lines[-1]
terms = query.split()
corpus = ' '.join(documents)
documents_rating = {i:i for i in range(len(documents))}


if __name__ == '__main__':
	file_name = str(sys.argv[1])
	#"KNN_input.txt"
    for i, document in enumerate(documents):
        document_score = 1
        for term in terms:
            TFtd = float(document.count(term))
            Ld = len(document.split())
            TFtc = float(corpus.count(term))
            Lc = len(corpus.split())
            Ptd = ((TFtd/Ld) + (TFtc/Lc)) /2
            document_score *= Ptd
        documents_rating[i] = document_score

print([element[0] for element in sorted(documents_rating.items(), key=operator.itemgetter(1), reverse=True)])
