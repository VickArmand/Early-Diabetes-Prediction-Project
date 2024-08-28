import africastalking as at
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
api_key = os.environ.get('AT_API_KEY')
username = os.environ.get('AT_USERNAME')
os.environ.get('EMAIL_PASS')
# Initialize the Africas Talking client with the required credentials
at.initialize(username, api_key)
def sendcustomizedsms(recipient,message,issent):
    # assign the sms functionality to a variable
    sms = at.SMS
    response=" "
    try:
        response = sms.send(message, [recipient])
        issent = True
    except:
        print("Message sending failed")
        issent = False
        
    return response,issent
    # Method for performing data preprocessings
def datapreprocessing(diabetesdataurl):
    diabetesdata= pd.read_csv(diabetesdataurl)
    diabetesdata[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = diabetesdata[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)
    diabetesdata.dropna(inplace=True)
    # diabetesdata['SkinThickness']=diabetesdata['SkinThickness'].replace(0,np.median(diabetesdata['SkinThickness']))
    # diabetesdata['Insulin']=diabetesdata['Insulin'].replace(0,np.median(diabetesdata['Insulin']))
    # diabetesdata['BMI']=diabetesdata['BMI'].replace(0,np.median(diabetesdata['BMI']))        
    # X=diabetesdata.drop(['Outcome','BloodPressure','SkinThickness'],axis=1)
    X=diabetesdata.drop(['Outcome','SkinThickness','BloodPressure'],axis=1)
    Y=diabetesdata['Outcome']
    # scaler = StandardScaler()
    # X = scaler.fit_transform(X)
    return X,Y
# Method for model training which returns accuracy and saves model in a file
def train(X,Y):  
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)
    classifier=svm.SVC(probability=True,kernel='linear')
    classifier.fit(X_train.values,Y_train)
    testpreds=classifier.predict(X_test.values)
    testaccuracy=round(accuracy_score(Y_test,testpreds)*100,2)
    # f1score= f1_score(Y_test,testpreds, average=None)
    mse=round(mean_squared_error(Y_test.values,testpreds),2)       
    modelspath='./app/static/ML Model'
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
    return testaccuracy,mse

def computemodelmetrics(X,Y):
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)
    modelpipe1=Pipeline([('model', LogisticRegression(max_iter=10000)),])
    modelpipe3=Pipeline([ ('model', svm.SVC(kernel='linear')),])
    modelpipe4=Pipeline([('model', RandomForestClassifier(n_estimators=200,criterion="entropy")),])
    modelpipe5=Pipeline([('model', KNeighborsClassifier(n_neighbors=2,metric="minkowski",p=2)),])
    modelpipe1.fit(X_train, Y_train)
    # modelpipe2.fit(X_train, Y_train)
    modelpipe3.fit(X_train.values, Y_train)
    modelpipe4.fit(X_train, Y_train)
    modelpipe5.fit(X_train, Y_train)
    testpred1=modelpipe1.predict(X_test)
    # testpred2=modelpipe2.predict(X_test)
    testpred3=modelpipe3.predict(X_test.values)
    testpred4=modelpipe4.predict(X_test)
    testpred5=modelpipe5.predict(X_test)
    accuracy={
            'Logistic Regression':round(accuracy_score(Y_test,testpred1)*100,2),
            'SVM':round(accuracy_score(Y_test,testpred3)*100,2),
            'Random Forest':round(accuracy_score(Y_test,testpred4)*100,2),        
            'K-Nearest Neighbours':round(accuracy_score(Y_test,testpred5)*100,2)
            # 'confusion matrix ':confusion_matrix(Y_test,testpred1),
            # 'classification report':classification_report(Y_test,testpred1)
        },
    # accuracy=[accuracy_score(Y_test,testpred1)*100,accuracy_score(Y_test,testpred3)*100,accuracy_score(Y_test,testpred4)*100,accuracy_score(Y_test,testpred5)*100]
    mse={
            'Logistic Regression': round(mean_squared_error(Y_test,testpred1),2),
            'SVM': round(mean_squared_error(Y_test,testpred3),2),
            'Random Forest': round(mean_squared_error(Y_test,testpred4),2),
            'K-Nearest Neighbours': round(mean_squared_error(Y_test,testpred5),2),
        },
    fs={
            'Logistic Regression': f1_score(Y_test, testpred1),
            'SVM': f1_score(Y_test, testpred3),
            'Random Forest': f1_score(Y_test, testpred4),
            'K-Nearest Neighbours':f1_score(Y_test, testpred5),
        }
        
    return accuracy,mse,fs