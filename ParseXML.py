# -*- coding: UTF-8 -*-

import xml.sax

global global_qsubject
global_qsubject = ""
global_qbody = ""
fp = open('result_general.txt', 'wb')
global_qtype = ""


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
                self.comment_line += attributes['CID']
            if 'CGOLD' in attributes:
                self.comment_line += "\t" + attributes['CGOLD']
        if tag == 'CBody':
            self.cbody = True
        if tag == 'Question':
            if 'QTYPE' in attributes:
                global global_qtype
                global_qtype = attributes['QTYPE']

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'Question':
            global global_qsubject
            global_qsubject = ""
            global global_qbody
            global_qbody = ""
            global global_qtype
            global_qtype = ""
        if tag == 'CSubject':
            self.comment_line += "\t" + self.CSubject
        if tag == 'CBody' and self.cbody:
            self.comment_line += "\t" + self.CBody.replace("\t", "").replace("\n", " ").strip()
            self.cbody = False
            self.CBody = ""
        if tag == 'Comment':
            global_qsubject
            global_qbody
            self.comment_line += "\t" + global_qsubject + "\t" + global_qbody
            print self.comment_line
            global_qtype
            if global_qtype == "GENERAL":
                fp
                fp.write(self.comment_line + '\n')
            self.comment_line = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "QSubject":
            global global_qsubject
            global_qsubject += content.replace("\t", "").strip()
        if self.CurrentData == "QBody":
            global global_qbody
            global_qbody += content.replace("\t", "").strip()
        if self.CurrentData == "CSubject":
            self.CSubject = content.replace("\t", "").strip()
        if self.CurrentData == "CBody":
            self.CBody += content


if __name__ == '__main__':
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MyXMLHandler()
    parser.setContentHandler(Handler)

    parser.parse("CQA-QL-train.xml")
    fp
    fp.close()
