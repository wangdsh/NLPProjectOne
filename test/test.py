# -*- coding: UTF-8 -*-

import xml
import xml.sax
import StringIO


class XMLContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.name = False
        self.content = ''
    def startElement(self, name, attrs):
        if name == 'name':
            self.name = True
    def characters(self,content):
        self.content += content
    def endElement(self,name):
        if self.name and name == 'name':
            self.name = False
            print self.content
            self.content = ''

# xmlText = r'<name>D &amp; C YELLOW NO. 10</name>'
# xmlFile = StringIO.StringIO(xmlText)
#
# XMLContentHandler=XMLContentHandler()
# xml.sax.parse(xmlFile,XMLContentHandler)

if __name__ == '__main__':
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = XMLContentHandler()
    parser.setContentHandler(Handler)

    parser.parse("test.xml")
