#-*- coding:utf-8 -*-

import sys
import LDA.latent_dirichlet_allocation as LDA
import LSI.LSI as LSI
import bag_of_words.bag_of_words as BOW
import cuserEqualquser.cuserEqualquser as cEq
import metainfo.ParseXML_metadata as MetaData
import category_probability.category_probability as cate_pro
import word2vec.word2vec as word2vec
import url.ParseXML_has_url as URL
import numpy as np
import pickle as pickle

def main(step):     # 0 train, 1 devel, 2 test

    # feature
    file = ""
    if step == 0:
        file = "../Pretreatment/Total/pretreatment_one_result_train_total_no_blank.txt"
        pickle_general = "./train_general_data.pkl"
        pickle_yes_no = "./train_yes_no_data.pkl"
    elif step == 1:
        file = "../Pretreatment/Total/pretreatment_one_result_devel_total_no_blank.txt"
        pickle_general = "./devel_general_data.pkl"
        pickle_yes_no = "./devel_yes_no_data.pkl"
    elif step == 2:
        file = "../Pretreatment/Total/pretreatment_one_result_test_total_no_blank.txt"
        pickle_general = "./test_general_data.pkl"
        pickle_yes_no = "./test_yes_no_data.pkl"
    else:
        print 'error step!'
        return

    fp = open(file, "r")
    row_num = 0

    qindex = 0          # index
    qid = 0
    qcontent = ""       # content

    features_gen = list()   # [[], [], ...]
    feature_yes_no = list()

    # meta
    meta = MetaData.MetaData(step)

    # LDA
    lda = LDA.LDA_Util(step)

    # LSI
    lsi = LSI.LSI_Util(step)

    # category_probability
    cp = cate_pro.category_util()

    # cuserEqualquser
    ceq = cEq.cuserEqualquser_Util(step)

    # URL
    url = URL.get_url_utli(step)

    # word2vec
    w2v = word2vec.Word2Vec(step)

    for line in fp:
        lines = line.split('\t')
        rowid = lines[0].strip()
        content = lines[0].strip()
        if len(rowid.split()) == 1:     # question
            qindex = row_num
            qid = rowid
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
            feature.extend(cp.get_category_vec(meta.getQuestionCat(qid)))

            # cuserEqualquser
            feature.append(ceq.get_cuserEqualquser_value(rowid))

            # url
            feature.append(url.get_url_value(rowid))

            # word2vec
            feature.append(w2v.getSentenseSim(qcontent, content))

            # label
            feature.append(meta.getCommentType(rowid, qid))

            if meta.getQuestionType(qid) == "GENERAL":
                features_gen.append(feature)
            else:
                feature_yes_no.append(feature)

        row_num += 1

    # pickle features  labels
    pickle.dump(features_gen, pickle_general)
    pickle.dump(feature_yes_no, pickle_yes_no)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "sys.argv[1]: step! (0 train, 1 devel, 2 test)"
        exit()

    step = int(sys.argv[1])
    pickle_path = sys.argv[2]
    main(step)

# bow w2v LDA TF-IDF URL Category_pro cuserComQuser

# train
# python getFeatureVector 0

# devel
# python getFeatureVector 1

# test
# python getFeatureVector 2

    

    
    
    

