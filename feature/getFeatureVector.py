#-*- coding:utf-8 -*-

import sys
import LDA.latent_dirichlet_allocation as LDA
import LSI.LSI as LSI
import bag_of_words.bag_of_words as BOW
import cuserEqualquser.cuserEqualquser as cEq
import metainfo.ParseXML_metadata as MetaData
import category_probability.category_probability as cate_pro
import word2vec.word2vecUtil as word2vecUtil
import url.ParseXML_has_url as URL
import numpy as np
import pickle as pickle

TRAIN_LINES = 19141
DEVEL_LINES = 1945
TEST_LINES = 2305

MIN_VALUE = 1e-8


def main(step):     # 0 train, 1 devel, 2 test

    # feature
    file = ""
    if step == 0:
        file = "../Pretreatment/Total/pretreatment_one_result_train_total_3_id.txt"
        pickle_general = "./train_general_data.pkl"
        pickle_yes_no = "./train_yes_no_data.pkl"
    elif step == 1:
        file = "../Pretreatment/Total/pretreatment_one_result_devel_total_3_id.txt"
        pickle_general = "./devel_general_data.pkl"
        pickle_yes_no = "./devel_yes_no_data.pkl"
    elif step == 2:
        file = "../Pretreatment/Total/pretreatment_one_result_test_total_3_id.txt"
        pickle_general = "./test_general_data.pkl"
        pickle_yes_no = "./test_yes_no_data.pkl"
    else:
        print 'error step!'
        return

    fp = open(file, "r")    # read file
    fp_pickle_general = open(pickle_general, "wb")
    fp_pickle_yes_no = open(pickle_yes_no, "wb")

    row_num = 0         # line number

    qindex = 0          # index
    qid = 0
    qcontent = ""       # content

    features_gen = list()   # [[], [], ...]
    feature_yes_no = list()

    # meta
    meta = MetaData.MetaData(step)

    # LDA
    lda = LDA.LDA_Util()

    # LSI
    lsi = LSI.LSI_Util()

    # category_probability
    cp = cate_pro.category_util()

    # cuserEqualquser
    ceq = cEq.cuserEqualquser_Util(step)

    # URL
    url = URL.get_url_utli(step)

    # word2vec
    w2v = word2vecUtil.Word2VecUtil()

    # add_step
    add_step = 0        # train
    if step == 1:
        add_step = TRAIN_LINES      # dev
    elif step == 2:
        add_step = TRAIN_LINES + DEVEL_LINES      # test


    for line in fp:

        lines = line.split('\t')
        rowid = lines[0].strip()
        content = lines[1].strip()

        print rowid, content

        if not "_" in rowid:     # question
            qindex = row_num
            qid = rowid
            qcontent = content          # comment
        else:

            feature = []

            # cid
            feature.append(rowid)

            # LDA
            feature.append(lda.getLDASim(qindex + add_step, row_num + add_step))

            # LSI
            feature.append(lsi.getLSISim(qindex + add_step, row_num + add_step))

            # BOW
            if qcontent and content:
                bow = BOW.BOW(qcontent, content)
                feature.append(bow.getVectorSim())
            else:
                feature.append(MIN_VALUE)

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

            print qid, meta.getQuestionType(qid)

            if meta.getQuestionType(qid) == "GENERAL":
                features_gen.append(feature)
            else:
                feature_yes_no.append(feature)

        row_num += 1

    print len(features_gen), len(feature_yes_no)
    # pickle features  labels
    pickle.dump(features_gen, fp_pickle_general)
    pickle.dump(feature_yes_no, fp_pickle_yes_no)

    # close
    fp.close()
    fp_pickle_general.close()
    fp_pickle_yes_no.close()

def showFeatures(file_path):
    fp = open(file_path, "r")
    features = pickle.load(fp)
    print "Show Features!"
    print features

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "sys.argv[1]: step! (0 train, 1 devel, 2 test)"
        exit()

    step = int(sys.argv[1])
    main(step)
    # showFeatures("./train_general_data.pkl")

# bow w2v LDA TF-IDF URL Category_pro cuserComQuser

# train
# python getFeatureVector.py 0

# devel
# python getFeatureVector.py 1

# test
# python getFeatureVector.py 2

    

    
    
    

