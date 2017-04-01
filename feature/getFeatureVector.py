#-*- coding:utf-8 -*-

import sys
import LDA.latent_dirichlet_allocation as LDA
import LSI.LSI as LSI
import bag_of_words.bag_of_words as BOW
import cuserEqualquser.cuserEqualquser as cEq
import category_probability.category_probability as CP
import word2vec.word2vec as word2vec
import numpy as np

def main(step):     # 0 train, 1 devel, 2 test

    # feature
    file = ""
    if step == 0:
        file = "../Pretreatment/Total/pretreatment_one_result_train_total_no_blank.txt"
    elif step == 1:
        file = "../Pretreatment/Total/pretreatment_one_result_devel_total_no_blank.txt"
    elif step == 2:
        file = "../Pretreatment/Total/pretreatment_one_result_test_total_no_blank.txt"
    else:
        return

    fp = open(file, "r")
    row_num = 0

    qindex = 0          # index
    qcontent = ""       # content

    features = list()   # [[], [], ...]

    # LDA
    lda = LDA.LDA_Util(step)

    # LSI
    lsi = LSI.LSI_Util(step)

    # word2vec
    w2v = word2vec.Word2Vec(step)

    for line in fp:
        lines = line.split('\t')
        rowid = lines[0].strip()
        content = lines[0].strip()
        if len(rowid.split()) == 1:     # question
            qindex = row_num
            qcontent = content          # comment
        else:

            feature = []

            # cid
            feature.append(rowid)

            # LDA

            feature.append(lda.getLDASim(qindex, row_num))

            # LSI

            feature.append(lsi.getLSISim(qindex, row_num))

            # BOW
            bow = BOW.BOW(qcontent, content)
            feature.append(bow.getVectorSim())

            # category_probability


            # cuserEqualquser
            ceq = cEq.cuserEqualquser_Util(step)
            feature.append(ceq.get_cuserEqualquser_value(rowid))

            # url

            # word2vec
            feature.append(w2v.getSentenseSim(qcontent, content))

            features.append(feature)

        row_num += 1

    # pickle features  labels

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "sys.argv[1]: step! (0 train, 1 devel, 2 test)"
        exit()

    step = int(sys.argv[1])
    main(step)

# bow w2v LDA TF-IDF URL Category_pro cuserComQuser
# bow w2v

    

    
    
    

