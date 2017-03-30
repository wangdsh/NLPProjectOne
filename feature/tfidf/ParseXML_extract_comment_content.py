# -*- coding: UTF-8 -*-

import xml.sax
import logging
import os.path
import nltk
import string
from nltk.corpus import wordnet as wn
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
CID = ""


class MyXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.CSubject = ""
        self.CBody = ""
        self.cbody = False
        self.comment_line = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'Comment':
            if 'CID' in attributes:
                # self.comment_line += attributes['CID']
                global CID
                CID = attributes['CID']
        if tag == 'CBody':
            self.cbody = True

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "CSubject":
            self.CSubject = content.replace("\t", "").strip()
        if self.CurrentData == "CBody":
            self.CBody += content

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'CSubject':
            self.comment_line += self.CSubject
        if tag == 'CBody' and self.cbody:
            self.comment_line += " " + self.CBody.replace("\t", "").replace("\n", " ").strip()
            self.cbody = False
            self.CBody = ""
        if tag == 'Comment':
            # 文本预处理
            # 2.分割成句子
            sents = sent_tokenizer.tokenize(self.comment_line)

            # 3.去掉数字标点和非字母字符
            cleanLines = [self.CleanLines(line.encode("utf-8")) for line in sents]

            # 4.nltk.word_tokenize分词
            words = [self.WordTokener(cl) for cl in cleanLines]

            # 5.去停用词和小写去短词
            cleanWords = self.CleanWords(words)

            # 6.使用Wordnet进行词干化
            stemWords = self.StemWords(cleanWords)

            # 7.
            strLine = self.WordsToStr(stemWords)

            # # 句子分割成词
            # wordsInStr = nltk.word_tokenize(sents[0])
            #
            # # 去掉数字标点和非字母字符
            # delEStr = string.punctuation + string.digits  # ASCII 标点符号，数字
            # identify = string.maketrans('', '')
            # line = " ".join(wordsInStr)
            # line = line.encode("utf-8").translate(identify, delEStr)

            print CID
            print " ".join(strLine)

            self.comment_line = ""

    def CleanLines(self, line):
        identify = string.maketrans('', '')
        delEStr = string.punctuation + string.digits  # ASCII 标点符号，数字
        # cleanLine = line.translate(identify,delEStr) #去掉ASCII 标点符号和空格
        cleanLine = line.translate(identify, delEStr)  # 去掉ASCII 标点符号
        return cleanLine

    def WordTokener(self, sent):  # 将单句字符串分割成词
        wordsInStr = nltk.word_tokenize(sent)
        return wordsInStr

    def CleanWords(self,wordsInStr): # 去掉标点符号，长度小于3的词以及non-alpha词，小写化
        cleanWords = []
        stopwords = {}.fromkeys([line.rstrip() for line in open('stopwords_short.txt')])
        for words in wordsInStr:
            cleanWords += [[w.lower() for w in words if w.lower() not in stopwords]]
        return cleanWords

    def StemWords(self, cleanWordsList):
        stemWords = []
        for words in cleanWordsList:
            stemWords += [[wn.morphy(w) for w in words]]
        return stemWords

    def WordsToStr(self, stemWords):
        strLine = []
        for words in stemWords:
            strLine += [w for w in words if w is not None]
        return strLine

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error("Usage example: python ParseXML_extract_comment_content.py ../../CQA-QL-devel.xml result_devel_conment_content.txt")
        sys.exit(1)
    input_file, output_file = sys.argv[1:3]

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MyXMLHandler()
    parser.setContentHandler(Handler)

    parser.parse(input_file)
