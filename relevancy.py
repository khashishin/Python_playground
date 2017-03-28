import sys
def calculate_relevancy(file_name):
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

    row_list = [delete_unallowed_signs(str(word.lower())) for word in open_file(file_name)]
    search_engines_number = int(row_list[0][0])
    relevant_lists_dict={}
    truly_relevant = set()
    relevant_found = set()

    #True relevancy
    for i,line in enumerate(row_list[search_engines_number+1:]):
        binary_row = line.split()
        for x,element in enumerate(binary_row):
            if int(element)==1:
                truly_relevant.add(int(x))

    #Adding outputs of search engines
    for i,line in enumerate(row_list[1:1+search_engines_number]):
        search_engine_output = [int(i) for i in line.split()]
        relevant_lists_dict[i] = search_engine_output
        for document in search_engine_output:
            if document in truly_relevant:
                relevant_found.add(document)

    for search_engine, output_list in relevant_lists_dict.items():
        precision = len(set(output_list).intersection(truly_relevant))/len(output_list)
        recall = len(set(output_list).intersection(truly_relevant))/len(truly_relevant)
        relative_recall = len(set(output_list).intersection(relevant_found))/len(relevant_found)
        F2= float(3*precision*recall)/(2*precision+recall)

        precision_j_sum=0.0
        relevance_sum = 0.0
        for position, element in enumerate(output_list):
            position_relevance = 1 if element in truly_relevant else 0
            relevance_sum += float(position_relevance)
            precision_j = relevance_sum / (position+1)
            precision_j_sum += (precision_j * position_relevance)
        print(precision_j_sum)
        print(len(truly_relevant))
        avg_mean_prec = precision_j_sum / len(truly_relevant)

        print ([round(precision,2), round(relative_recall,2), round(F2,2), round(avg_mean_prec,2)])

if __name__ == '__main__':
	#"relevancy_input.txt"
	file_name = sys.argv[1]
	calculate_relevancy(file_name)