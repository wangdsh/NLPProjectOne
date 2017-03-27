# NLPProjectOne
CQA-QL-train.xml: 训练数据<br>
CQA-QL-devel.xml: 开发数据<br>
test_task3_English.xml: 测试数据<br>

预处理<br>
ParseXML.py: 解析CQA-QL-train.xml中的General问题<br>
ParseXML_for_yes_no.py: 解析CQA-QL-train.xml中的yes-no问题<br>

README.md: this file<br>
test: 测试<br>

##feature/url<br>
ParseXML_has_url.py: 判断CSubject、CBody是否包括链接<br>
result_train_has_url.txt: 训练数据，1表示有，0表示无<br>
result_devel_has_url.txt<br>
result_test_has_url.txt<br>