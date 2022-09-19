import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,f1_score,mean_squared_error,confusion_matrix,classification_report

import pickle as pk
import os
import sys
sys.setrecursionlimit(10000)

class ModelUtils:
    def datapreprocessing(diabetesdataurl):
        diabetesdata= pd.read_csv(diabetesdataurl)
        diabetesdata[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = diabetesdata[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)
        diabetesdata.dropna(inplace=True)
        X=diabetesdata.drop(['Outcome','BloodPressure'],axis=1)
        Y=diabetesdata['Outcome']
        # scaler = StandardScaler()
        # X = scaler.fit_transform(X)
        return X,Y
    def train(X,Y):  
        X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)
        classifier=svm.SVC(kernel='linear')
        classifier.fit(X_train,Y_train)
        trainpreds=classifier.predict(X_train)
        testpreds=classifier.predict(X_test)
        testaccuracy=accuracy_score(Y_test,testpreds)*100
        f1score= f1_score(Y_test,testpreds, average=None)        
        modelspath='./static/ML Model'
        modelfile= "diabetespredmodelusingxgboost.pkl"
        modelpathfile=os.path.join(modelspath,modelfile)
        if not os.path.isdir(modelspath):
            os.makedirs(modelspath)
        modelpathfile=os.path.join(modelspath,modelfile)
        if not os.path.exists(modelpathfile):
            pk.dump(classifier,open(modelpathfile,'wb'))
        else:
            os.remove(modelpathfile)
            pk.dump(classifier,open(modelpathfile,'wb'))

        return testaccuracy,f1score
 
    def computemetrics(X,Y):
        X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)

        modelpipe1=Pipeline([
            ('model', LogisticRegression()),
        ])
        modelpipe3=Pipeline([
            
            ('model', svm.SVC(kernel='linear')),
        ])
        modelpipe4=Pipeline([
            
            ('model', RandomForestClassifier(n_estimators=2,criterion="entropy")),
        ])
        modelpipe5=Pipeline([
            
            ('model', KNeighborsClassifier(n_neighbors=2,metric="minkowski",p=2)),
        ])


        modelpipe1.fit(X_train, Y_train)
        # modelpipe2.fit(X_train, Y_train)
        modelpipe3.fit(X_train, Y_train)
        modelpipe4.fit(X_train, Y_train)
        modelpipe5.fit(X_train, Y_train)
        testpred1=modelpipe1.predict(X_test)
        # testpred2=modelpipe2.predict(X_test)
        testpred3=modelpipe3.predict(X_test)
        testpred4=modelpipe4.predict(X_test)
        testpred5=modelpipe5.predict(X_test)
        accuracy={
                'Logistic Regression':accuracy_score(Y_test,testpred1)*100,
                'SVM':accuracy_score(Y_test,testpred1)*100,
                'Random Forest':accuracy_score(Y_test,testpred1)*100,        
                'K-Nearest Neighbours':accuracy_score(Y_test,testpred1)*100
                # 'confusion matrix ':confusion_matrix(Y_test,testpred1),
                # 'classification report':classification_report(Y_test,testpred1)
            },
        mse={
                'Logistic_Regression': mean_squared_error(Y_test,testpred1),
                'SVM': mean_squared_error(Y_test,testpred3),
                'Random Forest': mean_squared_error(Y_test,testpred4),
                'K-Nearest Neighbours': mean_squared_error(Y_test,testpred5),
            },
        fs={
                'Logistic Regression': f1_score(Y_test, testpred1),
                'SVM': f1_score(Y_test, testpred3),
                'Random Forest': f1_score(Y_test, testpred4),
                'K-Nearest Neighbours':f1_score(Y_test, testpred5),
            }
            
        return accuracy,mse,fs


    