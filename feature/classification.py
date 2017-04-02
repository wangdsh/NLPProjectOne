# -*- coding: utf-8 -*-

import numpy as np
import os,sys
from sklearn import tree
from sklearn import svm
from sklearn import metrics
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import  accuracy_score  
from sklearn.metrics import confusion_matrix    
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB 
from sklearn.preprocessing import MinMaxScaler

import numpy as np

GENERAL_NUM_CLASS = 6
YES_NO_NUML_CLASS = 3


#notice, we only use gbdt, essemble, tree, knn and svm classifier
#you can add others if you need

def getOneHotVec(X, num_class):
    one_hot = np.zeros((X.shape[0], num_class))
    one_hot[np.arange(X.shape[0]), X] = 1
    return one_hot

class Classification():
    def __init__(self, classifier, trainFile, devFile):
        f = open(trainFile)
        data = np.loadtxt(f)
        
        # select columns 1 through end
        X_train = data[:, 1:]  
        y_train = data[:, 0]
        y_train = getOneHotVec(y_train, GENERAL_NUM_CLASS)
        f.close()
            
        f = open(devFile)
        pre = np.loadtxt(f)
        X_test = pre[:, 1:]
        
        # min_max_scaler = MinMaxScaler()
        # X_train = min_max_scaler.fit_transform(X_train)
        # X_test = min_max_scaler.fit_transform(X_test)

        #fit transform if there exit NAN or INFINITE
        #otherwise you'll get error when clf.predict()
        X_test = Imputer().fit_transform(X_test) 
        if np.isnan(X_test).any():
            print "nan in X_test!"
            exit()
            
        self.y_test = pre[:, 0] 
        f.close()
        
        if classifier == 'tree':
            #max_depth = 4 is best
            # max_depth = np.arange(1, 10)
            # clf = GridSearchCV(tree.DecisionTreeClassifier(), param_grid = {'max_depth': max_depth})
            clf = tree.DecisionTreeClassifier(max_depth = 4)
            
        elif classifier == 'knn':
            #n_neighbors = 9 is best
            #but default is 5, better than 9?
            # n_neighbors = np.arange(1, 10)  
            # clf = GridSearchCV(KNeighborsClassifier(), param_grid = {'n_neighbors': n_neighbors})
            clf = KNeighborsClassifier(n_neighbors = 9)
            
        elif classifier == 'svm':
            #{'kernel': 'rbf', 'C': 100, 'gamma': 0.001}
            # param_grid = [{'C': [1, 10, 100, 1000], 'kernel': ['linear']}, {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]
            # clf = GridSearchCV(svm.SVC(), param_grid)
            clf = svm.SVC(kernel='rbf', gamma = 0.001, C = 100)
            
        elif classifier == 'gbdt':
            # max_depth = np.arange(1, 10)
            # n_estimators = [10, 100, 1000]
            # learning_rate = [0.1, 0.2, 0.3, 0.4, 0.5]
            # clf = GridSearchCV(GradientBoostingClassifier(), param_grid = {'max_depth': max_depth, 'n_estimators': n_estimators, 'learning_rate': learning_rate})
            clf = GradientBoostingClassifier(n_estimators = 1000, max_depth = 10)
            
        elif classifier == 'essemble':
            #{'n_estimators': 10, 'max_depth': 6}
            # max_depth = np.arange(1, 10)
            # n_estimators = [10, 100, 1000]
            # clf = GridSearchCV(RandomForestClassifier(), param_grid = {'max_depth': max_depth, 'n_estimators': n_estimators})
            clf = RandomForestClassifier(n_estimators = 1000, random_state=15325)
            
        elif classifier == 'nb':
            clf = MultinomialNB()
            print clf
        else:
            print "Invalid classifier in Class Classification __init__()!"
            exit()
        
        clf.fit(X_train, y_train) 
        #print clf.best_params_
        
        self.y_pred = clf.predict(X_test)
        
        '''
        #test usage!
        self.calculate_result(self.y_test, self.y_pred)
        print( "ACC:  %f " %accuracy_score(y_test,y_pred))
        '''
        
    def getPreResult(self, outputFile):
        fout = open(outputFile,"w+")
        for each in self.y_pred:
            eachint = int(each)
            fout.write(str(eachint)+"\n")
        fout.close()        
   
    #this function is used for testing!
    def calculate_result(self):  
        m_precision = metrics.precision_score(self.y_test, self.y_pred)
        m_recall = metrics.recall_score(self.y_test, self.y_pred) 
        print 'precision:{0:.3f}'.format(m_precision)  
        print 'recall:{0:0.3f}'.format(m_recall) 
        print 'f1-score:{0:.3f}'.format(metrics.f1_score(self.y_test, self.y_pred))    
    
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "sys.argv[1]: classifier"
        print "sys.argv[2]: trainFile"
        print "sys.argv[3]: devFile"
        print "sys.argv[4]: outputFile"
        exit()

    cfInstance = Classification(sys.argv[1], sys.argv[2], sys.argv[3])
    cfInstance.getPreResult(sys.argv[4])
    




