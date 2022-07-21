import pandas as pd
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

data = pd.read_csv('C://Users//KHURRAM//PycharmProjects//fyp-dashboard//static//datasets//dataset_logistic_regression.csv')
def data_head():
    rows = []
    count=0
    with open('C://Users//KHURRAM//PycharmProjects//fyp-dashboard//static//datasets//dataset_logistic_regression.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if count <= 10:
                rows.append(row)
                count+=1
    return rows

def header():
    with open('C://Users//KHURRAM//PycharmProjects//fyp-dashboard//static//datasets//dataset_logistic_regression.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
    return header

def feature_selection():
    x = data.drop(['Class'], axis=1)  # Drop The Target Variable
    y = data['Class']
    return x,y

def data_dimension():
    return data.shape

def data_nullable():
    return data.isna().any()  # data.isna()

def train_test_data():
    x = data.drop(['Class'], axis=1)  # Drop The Target Variable
    y = data['Class']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)
    # SHAPES
    return xTrain.shape, yTrain.shape, xTest.shape, yTest.shape

def predict():
    x = data.drop(['Class'], axis=1)  # Drop The Target Variable
    y = data['Class']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)
    x_matrix = x.values.reshape(-1, 1)
    logisreg = LogisticRegression()
    logisreg.fit(xTrain, yTrain)
    y_pred = logisreg.predict(xTest)
    return y_pred

def confusion_matrix():
    x = data.drop(['Class'], axis=1)  # Drop The Target Variable
    y = data['Class']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)
    logisreg = LogisticRegression()
    logisreg.fit(xTrain, yTrain)
    y_pred = logisreg.predict(xTest)
    cm = metrics.confusion_matrix(yTest, y_pred)
    return cm

def accuracy():
    x = data.drop(['Class'], axis=1)  # Drop The Target Variable
    y = data['Class']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)
    logisreg = LogisticRegression()
    logisreg.fit(xTrain, yTrain)
    y_pred = logisreg.predict(xTest)
    accuracy = logisreg.score(xTest, yTest)
    # print("Accuracy Of Model Is ", round(accuracy * 100, 2), "%")
    temp = str(round(accuracy * 100, 2))+"%"
    return temp
