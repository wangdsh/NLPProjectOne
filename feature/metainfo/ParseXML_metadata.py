# -*- coding: UTF-8 -*-

import xml.sax
import sys


class MyXMLHandler(xml.sax.ContentHandler):
    def __init__(self, outDir, file_type):
        self.qtype = ''
        self.ftype = file_type
        self.fp_general = outDir + 'metadata_general.txt'
        self.fp_yes_no = outDir + 'metadata_yes_no.txt'
        self.fp_total = outDir + 'metadata_total.txt'

    # 元素开始事件处理
    def startElement(self, tag, attributes):

        fp_total = open(self.fp_total, 'a+')
        fp_general = open(self.fp_general, 'a+')
        fp_yes_no = open(self.fp_yes_no, 'a+')

        if tag == 'Question':

            qline = ''
            if self.ftype == 2:
                qline = attributes['QID'] + "\t" + attributes['QCATEGORY'] + "\t" + \
                         attributes['QUSERID'] +"\t" + attributes['QTYPE'] + "\n"
            else:
                qline = attributes['QID'] + "\t" + attributes['QCATEGORY'] + "\t" + \
                         attributes['QUSERID'] +"\t" + attributes['QTYPE'] + "\t" + \
                         attributes['QGOLD_YN'] + "\n"

            fp_total.write(qline)
            if attributes['QTYPE'] == 'GENERAL':
                self.qtype = 'GENERAL'
                fp_general.write(qline)
            else:
                self.qtype = 'YES_NO'
                fp_yes_no.write(qline)

        elif tag == 'Comment':

            cline = ''
            if self.ftype == 2:
                cline = attributes['CID'] + "\t" + attributes['CUSERID'] + "\n"
            else:
                cline = attributes['CID'] + "\t" + attributes['CUSERID'] + "\t" + \
                         attributes['CGOLD'] +"\t" + attributes['CGOLD_YN'] + "\n"


            fp_total.write(cline)
            if self.qtype == 'GENERAL':
                fp_general.write(cline)
            else:
                fp_yes_no.write(cline)

        fp_total.close()
        fp_yes_no.close()
        fp_general.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Parse File Path"
        print "sys.argv[2]: Data Type (train 0, dev 1, test 2)"
        exit()

    outDir = ''             # 文件夹
    file_type = ''          # 文件类型

    if sys.argv[2] == '0':
        outDir = "./train/"
        file_type = 0
    elif sys.argv[2] == '1':
        outDir = "./dev/"
        file_type = 1
    elif sys.argv[2] == '2':
        outDir = "./test/"
        file_type = 2
    else:
        print 'error'
        exit()

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MyXMLHandler(outDir, file_type)
    parser.setContentHandler(Handler)

    # 解析文件
    parser.parse(sys.argv[1])

    print "parse " + sys.argv[1] + " done!"


# train file
# python ParseXML_metadata.py CQA-QL-train.xml 0

# dev file
# python ParseXML_metadata.py CQA-QL-devel.xml 1

# test file
# python ParseXML_metadata.py test_task3_English.xml 2


