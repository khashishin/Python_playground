#feature selection slad 18
#wyliczenie n podstawie slajdu 9/10 (10 konkretny przyklad)

def calculate_classification(file_name):
    strip_signs_list = [',', '.', '\r', '\n', '-', '"', "'"]
    def delete_unallowed_signs(text):
        for ch in strip_signs_list:
            if ch in text:
                text = text.replace(ch, "")
        return text

    def open_file(filename):
        f = open(filename, 'r')
        row_list = f.readlines()
        f.close()      # closing
        return row_list

    def draw_terms(document):
        for word in document.split():
            term_set.add(word)


    row_list = [delete_unallowed_signs(str(word.lower())) for word in open_file(file_name)]
    training_docs = int(row_list[0][0])
    binary_row = training_docs+1
    term_set = set()
    #documents iteration
    documents = [line for line in row_list[1:binary_row]]
    for line in documents:
        draw_terms(line)

    print (term_set)

    #binary docs
    binary = [element for element in row_list[binary_row].split()]
    print(binary)

    #row to test
    test_row = row_list[-2]
    print (test_row)

    #last row - documents important
    feature_sel_num = int(row_list[-1][0])
    print (feature_sel_num)


    chi_2 = [{term: 0} for term in term_set]

    print(chi_2)

if __name__ == "__main__":
	#"KNN_input.txt"
	file_name = sys.argv[1]
	calculate_classification(file_name)