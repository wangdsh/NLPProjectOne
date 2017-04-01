

def getLDAList(lda_result_file_path):
    lda_list = []
    fp = open(lda_result_file_path, "r")
    for line in fp:
        lda_list.append(line.strip())
    fp.close()
    return lda_list
