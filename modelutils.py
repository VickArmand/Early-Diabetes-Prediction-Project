import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score,f1_score,mean_absolute_error
from sklearn.metrics import accuracy_score,f1_score,mean_squared_error,confusion_matrix,classification_report
import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
import os
modelspath='./static/ML Model'
modelfile= "diabetespredmodelusingxgboost.json"
modelpathfile=os.path.join(modelspath,modelfile)
def datapreprocessing(diabetesdataurl):
    diabetesdata= pd.read_csv(diabetesdataurl)
    diabetesdata[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = diabetesdata[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)
    diabetesdata.dropna(inplace=True)
    X=diabetesdata.drop(['Outcome'],axis=1)
    Y=diabetesdata['Outcome']
    scaler = StandardScaler()
    # X = scaler.fit_transform(X)
    return X,Y
def train(X,Y):  
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)
    xgb_cls=xgb.XGBClassifier(learning_rate =0.0001,n_estimators=1000, max_depth=5,min_child_weight=1,gamma=0,subsample=0.8, colsample_bytree=0.8,objective= 'binary:logistic',nthread=4,scale_pos_weight=1,seed=27)
    classifier=xgb_cls.fit(X_train,Y_train)
    trainpreds=classifier.predict(X_train)
    testpreds=classifier.predict(X_test)
    testaccuracy=accuracy_score(Y_test,testpreds)
    trainaccuracy=accuracy_score(Y_train,trainpreds)
    f1score= f1_score(Y_train,trainpreds, average=None)
    modelgeneration(classifier)
    return testaccuracy,trainaccuracy,f1score
def modelgeneration(classifier):
    modelspath='./static/ML Model'
    modelfile= "diabetespredmodelusingxgboost.json"
    # path_to_train="C:\\Users\\VICKFURY\\Documents\\projects\\Python Scripts\\ml\\ml codes\\supervised\\INTRODUCTION TO TENSORFLOW FOR COMPUTER VISION\\traffic signs\\Datasets\\Model Training Data\\Train"
    if not os.path.isdir(modelspath):
        os.makedirs(modelspath)
    modelfile=os.path.join(modelspath,modelfile)
    if not os.path.exists(modelfile):
        classifier.save_model(modelfile)
    else:
        os.remove(modelfile)
        classifier.save_model(modelfile)

    return True
def predict():
    # filename="diabetespredmodelusingxgboost.json"
    xgb_cls=xgb.XGBClassifier(learning_rate =0.0001,
    n_estimators=1000,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    objective= 'binary:logistic',
    nthread=4,
    scale_pos_weight=1,
    seed=27)
    xgb_cls.load_model(modelpathfile)
        # pregnanciesno=request.form["pregnanciesno"]
        # glucose=request.form["glucose"]
        # bmi=request.form["bmi"]
        # insulin=request.form["insulin"]
        # Age=request.form["Age"]
        # bloodpressure=request.form["bloodpressure"]
        # outcome=request.form["outcome"]
        # DiabetesPedigreeFunction=request.form["DiabetesPedigreeFunction"]
        # SkinThickness=request.form["SkinThickness"]
    features=[float(x) for x in request.form.values()]
    finalfeatures=[np.array(features)]
    sample1=[6,148,72,35,0,33.6,0.627,50]
    #sample1=[5,116,74,0,0,25.6,0.201,30]
    sample1=np.array(sample1)
    sample1=sample1.reshape(1,-1)
    prediction=xgb_cls.predict(sample1)
    return prediction
def computemetrics(X,Y):
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)

    modelpipe1=Pipeline([
        ('model', LogisticRegression()),
    ])
    modelpipe2=Pipeline([
        
        ('model',xgb.XGBClassifier(learning_rate =0.0001, n_estimators=1000,max_depth=5,min_child_weight=1,gamma=0,subsample=0.8,colsample_bytree=0.8,objective= 'binary:logistic', nthread=4,scale_pos_weight=1,seed=27))

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
    modelpipe2.fit(X_train, Y_train)
    modelpipe3.fit(X_train, Y_train)
    modelpipe4.fit(X_train, Y_train)
    modelpipe5.fit(X_train, Y_train)

    trainpred1=modelpipe1.predict(X_train)
    trainpred2=modelpipe2.predict(X_train)
    trainpred3=modelpipe3.predict(X_train)
    trainpred4=modelpipe4.predict(X_train)
    trainpred5=modelpipe5.predict(X_train)

    testpred1=modelpipe1.predict(X_test)
    testpred2=modelpipe2.predict(X_test)
    testpred3=modelpipe3.predict(X_test)
    testpred4=modelpipe4.predict(X_test)
    testpred5=modelpipe5.predict(X_test)
    
    # trainaccuracy=[accuracy_score(Y_train,trainpred1),accuracy_score(Y_train,trainpred2),accuracy_score(Y_train,trainpred3),accuracy_score(Y_train,trainpred4),accuracy_score(Y_train,trainpred5)]
    # testaccuracy=[accuracy_score(Y_test,testpred1),accuracy_score(Y_test,testpred2),accuracy_score(Y_test,testpred3),accuracy_score(Y_test,testpred4),accuracy_score(Y_test,testpred5)]
    # print (display_classificationreport(Y_test, testpred1))
    # print (display_classificationreport(Y_test, testpred2))
    # print (display_classificationreport(Y_test, testpred3))
    # print (display_classificationreport(Y_test, testpred4))
    # print (display_classificationreport(Y_test, testpred5))

    # print(f"Logistic Regression Mean Squared Error : {calculate_meansquarederror(modelpipe1, Y_train, trainpred1):.4f}")
    # print(f"XGBoost  Mean Squared Error : {calculate_meansquarederror(modelpipe2, Y_train, trainpred2):.4f}")
    # print(f"SVM  Mean Squared Error: {calculate_meansquarederror(modelpipe3, Y_train, trainpred3):.4f}")
    # print(f"Random Forest  Mean Squared Error: {calculate_meansquarederror(modelpipe4, Y_train, trainpred4):.4f}")
    # print(f"KNN Train Mean Squared Error: {calculate_meansquarederror(modelpipe5, Y_train, trainpred5):.4f}")

    # print(f"Logistic Regression Mean Squared Error : {calculate_meansquarederror(modelpipe1, Y_test, testpred1):.4f}")
    # print(f"XGBoost  Mean Squared Error : {calculate_meansquarederror(modelpipe2, Y_test, testpred2):.4f}")
    # print(f"SVM  Mean Squared Error: {calculate_meansquarederror(modelpipe3, Y_test, testpred3):.4f}")
    # print(f"Random Forest  Mean Squared Error: {calculate_meansquarederror(modelpipe4, Y_test, testpred4):.4f}")
    # print(f"KNN Train Mean Squared Error: {calculate_meansquarederror(modelpipe5, Y_test, testpred5):.4f}")
    return  calculate_model_metrics(modelpipe2,Y_test, testpred1),calculate_model_metrics(modelpipe2,Y_test, testpred2),calculate_model_metrics(modelpipe3,Y_test, testpred3),calculate_model_metrics(modelpipe4,Y_test, testpred4),calculate_model_metrics(modelpipe5,Y_test, testpred5)
def calculate_model_metrics(algorithm,true, pred):
    algorithm_details={f'{algorithm}': 
    {
    f'accuracy of {algorithm}':accuracy_score(true,pred),        f'mean squared error of{algorithm}': mean_squared_error(true,pred),
    f'confusion matrix of {algorithm}':confusion_matrix(true,pred),
    f'f1 score of {algorithm}':f1_score(true, pred),
    f'classification report of {algorithm}':classification_report(true,pred)
    }
    }
    return algorithm_details

    