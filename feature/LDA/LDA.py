#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import jieba, os
import codecs
from gensim import corpora, models, similarities
from pprint import pprint
from collections import defaultdict
import logging
import os.path
import sys
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf-8')

# read the train dev document
def load_data(dirPath):
    walk = os.walk(dirPath)  # '../../Pretreatment/General/'   train dev
    documents = []
    for root, dirs, files in walk:
        for name in files:
            raw = codecs.open(os.path.join(root, name), 'r', 'utf-8','ignore').read()
            documents.append(raw)
    return documents

def preprocess(documents):

    # read stop words
    stoplist = codecs.open('tmp/stopword.txt','r',encoding='utf8').readlines()
    stoplist = set(w.strip() for w in stoplist)

    #分词，去停用词
    texts = [[word for word in list(jieba.cut(document.replace('\t','').replace('\n',''), cut_all = True)) if word not in stoplist]
        for document in documents]
    #去除低频词
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 2]
            for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('tmp/sogou.dict')
    print(dictionary)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('tmp/sogou.mm', corpus)
    return corpus,dictionary


def train_lda(corpus,dictionary):
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    # 模型训练
    lda = models.LdaModel(corpus_tfidf, id2word = dictionary, num_topics = 9)
    #模型的保存/ 加载
    lda.save('tmp/sogou_lda.model')


def load_lda():
    lda = models.ldamodel.LdaModel.load('tmp/sogou_lda.model')
    for i in range(4):
        print lda.print_topic(i)

def test_lda():
    lda_model = models.ldamodel.LdaModel.load('tmp/sogou_lda.model')
    dictionary = corpora.Dictionary.load('tmp/sogou.dict')
    corpus = corpora.MmCorpus('tmp/sogou.mm')
    stoplist = codecs.open('tmp/stopword.txt', 'r', encoding='utf8').readlines()
    unseen_document = """
    　　在本赛季的这三场比赛中，骑士三战皆胜。值得一提的是，全场比赛骑士三分线外46投25中，打破NBA常规赛单场比赛单支球队三分球命中数纪录。
        """
    d = "".join(unseen_document.split())
    print "The unseen document is composed by the following text:", unseen_document
    print
    text = [word for word in list(jieba.cut(d, cut_all=True)) if word not in stoplist]

    bow_vector = dictionary.doc2bow(text)
    for i in range(0, 9):
        print lda_model.print_topic(i)
    print lda_model[bow_vector]
    for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1 * tup[1]):
        print "Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 3))

def print_lda():
    lda_model = models.ldamodel.LdaModel.load('tmp/sogou_lda.model')
    for i in range(0, 9):
        print i,lda_model.print_topic(i,10)

    print 0, lda_model.print_topic(0, 10)

def train(dirPath):
    documents = load_data(dirPath)
    corpus,dictionary = preprocess(documents)
    train_lda(corpus,dictionary)

def test():
    #load_lda()
    #test_lda()
    dictionary = corpora.Dictionary.load('tmp/sogou.dict')
    print dictionary[10]
    print len(dictionary)
    print dictionary

def test1():
    lda = models.ldamodel.LdaModel.load('tmp/sogou_lda.model')
    test_doc = """
        　　中华网总经理陈晓薇表示，该公司将在今年首季推出生活频道及重建英语频道，并着手发展与其他国家及知名企业合作的资讯网页，此外在5月份，中华网推出针对内地专业人士的娱乐内容，作为将来3G手机内容的供应来源。（英宁）
            """
    test_doc = list(jieba.cut(test_doc)) # 新文档进行分词
    doc_bow = corpora.Dictionary.doc2bow(test_doc)  # 文档转换成bow
    doc_lda = lda[doc_bow]  # 得到新文档的主题分布
    # 输出新文档的主题分布
    print doc_lda
    for topic in doc_lda:
        print "%s\t%f\n" % (lda.print_topic(topic[0]), topic[1])

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit(1)

    inp, outp1 = sys.argv[1:3]

    train(inp)
    print_lda()



# train
# python LDA.py ../../Pretreatment/General/pretreatment_one_result_train_general.txt ./train.model

# dev and test ignore
# dev
# python category_probability.py ../metainfo/dev/metadata_total.txt 1

# test
# python category_probability.py ../metainfo/test/metadata_total.txt 2