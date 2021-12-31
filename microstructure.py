# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 19:17:43 2021

@author: hongyong Han

To: Do or do not. There is no try.

"""
import numpy as np
from sklearn.model_selection import  train_test_split
from sklearn.neighbors import KNeighborsRegressor  #k-NN
from sklearn.neural_network import MLPRegressor    #神经网络
from sklearn.preprocessing import StandardScaler   #预处理 均值为0 方差为1

def get_FeretRatio(testset):
    f_pred=np.zeros(shape=(len(testset),200))  #预留矩阵
    # 读取数据
    f=np.loadtxt(r'C:\Users\Uaena_HY\Desktop\代码集\数据库\f-453.txt',delimiter='\t')
    data1=np.random.permutation(f)
    x1=data1[:,:9]
    y1=data1[:,-1]
    
    for k in range(200):
            
        x_train1,x_test1,y_train1,y_test1 = train_test_split(x1,y1,test_size=0.2,random_state=1)

        scaler = StandardScaler()
        scaler.fit(x_train1)
        X_scaled = scaler.transform(x_train1)    
        X_predicted = scaler.transform(testset)
    
        #建模
        FeretRatio = MLPRegressor(random_state=38,max_iter=10000,activation ='tanh',
                       alpha=1,hidden_layer_sizes=(9,),solver='lbfgs').fit(X_scaled,y_train1)
        #预测
        f_pred[:,k] = FeretRatio.predict(X_predicted)
    ff = np.mean(abs(f_pred),axis=1)    
    return ff

def get_thickness(testset):
    th_pred=np.zeros(shape=(len(testset),200))  #预留矩阵
    #读取数据
    th=np.loadtxt(r'C:\Users\Uaena_HY\Desktop\代码集\数据库\th-453.txt',delimiter='\t')
    data2 = np.random.permutation(th)
    x2 = data2[:,:9]
    y2 = data2[:,-1]
    
    for k in range(200):
            
        x_train2,x_test2,y_train2,y_test2 = train_test_split(x2,y2,test_size=0.2,random_state=1)
        #建模
        thickness = KNeighborsRegressor(n_neighbors=6).fit(x_train2,y_train2)
    
        #预测
        th_pred[:,k] = thickness.predict(testset)
    thick = np.mean(abs(th_pred),axis=1) 
    return thick

def get_volumefraction(testset_No_Ni):
    V_pred=np.zeros(shape=(len(testset_No_Ni),200))  #预留矩阵    
    #读取数据
    V=np.loadtxt(r'C:\Users\Uaena_HY\Desktop\代码集\数据库\V-403.txt',delimiter='\t')
    data3 = np.random.permutation(V)
    x3 = data3[:,:8]
    y3 = data3[:,-1]

    for k in range(200):    
        x_train3,x_test3,y_train3,y_test3 = train_test_split(x3,y3,test_size=0.2,random_state=1)
        #建模
        Volume = KNeighborsRegressor(n_neighbors=3).fit(x_train3,y_train3)
    
        #预测
        V_pred[:,k] = Volume.predict(testset_No_Ni)
    vol = np.mean(abs(V_pred),axis=1)
    return vol
    
def TCP_judge(TCPcontent,composition_polynomial): 
    label = TCPcontent + 2.11*composition_polynomial-36.89
    return label
    
     
    