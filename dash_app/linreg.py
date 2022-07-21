import pandas as pd
import csv
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.linear_model import LinearRegression
# sns.set()

data = pd.read_csv('C://Users//KHURRAM//PycharmProjects//fyp-dashboard//static//datasets//dataset_linear_regression.csv')
def lin_reg_data_head():
    rows = []
    count=0
    with open('C://Users//KHURRAM//PycharmProjects//fyp-dashboard//static//datasets//dataset_linear_regression.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if count <= 5:
                rows.append(row)
                count+=1
    print(header)
    return rows

def lin_reg_header():
    with open('C://Users//KHURRAM//PycharmProjects//fyp-dashboard//static//datasets//dataset_linear_regression.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
    return header

def lin_reg_feature_selection():
    x = data['SAT']  # Feature Variable
    y = data['GPA']  # Target Variable
    return x,y

def lin_reg_dimensions():
    x = data['SAT']  # Feature Variable
    y = data['GPA']  # Target Variable
    x_matrix = x.values.reshape(-1, 1)
    return x_matrix.shape

def lin_reg_r_value():
    x = data['SAT']  # Feature Variable
    y = data['GPA']  # Target Variable
    x_matrix = x.values.reshape(-1, 1)
    reg = LinearRegression()
    reg.fit(x_matrix, y)
    return reg.score(x_matrix, y)  # R-Sq Value

def lin_reg_intercept():
    x = data['SAT']  # Feature Variable
    y = data['GPA']  # Target Variable
    x_matrix = x.values.reshape(-1, 1)
    reg = LinearRegression()
    reg.fit(x_matrix, y)
    return reg.intercept_  # R-Sq Value

def lin_reg_new_data():
    lst = [1740, 1760]
    return lst

def lin_reg_predict():
    x = data['SAT']  # Feature Variable
    y = data['GPA']  # Target Variable
    x_matrix = x.values.reshape(-1, 1)
    reg = LinearRegression()
    reg.fit(x_matrix, y)
    new_data = pd.DataFrame(data=[1740, 1760], columns=['SAT'])
    return reg.predict(new_data)