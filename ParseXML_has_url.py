# -*- coding: UTF-8 -*-

import xml.sax

global global_qsubject
global_qsubject = ""
global_qbody = ""
fp = open('result_has_url.txt', 'wb')
global_qtype = ""
has_url = 0


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
        if tag == 'CBody':
            self.cbody = True
        if tag == 'Question':
            if 'QTYPE' in attributes:
                global global_qtype
                global_qtype = attributes['QTYPE']

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'Question':
            global global_qtype
            global_qtype = ""
        if tag == 'CSubject':
            if self.CSubject.find("http") != -1:
                global has_url
                has_url += 1
        if tag == 'CBody' and self.cbody:
            if self.CBody.find("http") != -1:
                has_url += 1
            self.cbody = False
            self.CBody = ""
        if tag == 'Comment':
            if has_url > 0:
                self.comment_line += "\t1"
            else:
                self.comment_line += "\t0"
            print self.comment_line
            # global_qtype
            # if global_qtype == "GENERAL":
            #     fp.write(self.comment_line + '\n')
            fp.write(self.comment_line + '\n')
            self.comment_line = ""
            has_url = 0

    # 内容事件处理
    def characters(self, content):
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
    fp.close()
