#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import multiprocessing
import numpy as np

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from scipy import linalg, mat, dot
# get

vector_len = 400

class Word2Vec:

    def __init__(self, step):   # 0 train, 1 devel, 2 test
        file = ""
        if step == 0:
            file = " ./train_w2v.vector"
        elif step == 1:
            file = "./devel_w2v.vector"
        elif step == 2:
            file = "./test_w2v.vector"
        self.model = Word2Vec.load(file)

    def cosine(self, list1, list2):
        a = mat(list1)
        b = mat(list2)
        c = dot(a,b.T)/linalg.norm(a)/linalg.norm(b)
        return c[0,0]

    def getSentenseSim(self, s1, s2):

        v1 = np.zeros(vector_len)
        v2 = np.zeros(vector_len)
        for word in s1.split():
            v1 += self.model.wv[word]
        for word in s2.split():
            v2 += self.model.wv[word]
        return self.cosine(v1, v2)

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print globals()['__doc__'] % locals()
        sys.exit(1)
    inp, out = sys.argv[1:4]

    model = Word2Vec(LineSentence(inp), size=400, window=5, min_count=5,
            workers=multiprocessing.cpu_count())

    # trim unneeded model memory = use(much) less RAM
    #model.init_sims(replace=True)
    # model.wv.save(outp1)
    model.save(out)



# train
# python word2vec.py ../../Pretreatment/Total/pretreatment_one_result_train_total_2.txt ./train_w2v.vector

# dev and test ignore
# dev
# python word2vec.py ../../Pretreatment/Total/pretreatment_one_result_devel_total_2.txt ./devel_w2v.vector

# test
# python word2vec.py ../../Pretreatment/Total/pretreatment_one_result_test_total_2.txt ./test_w2v.vector