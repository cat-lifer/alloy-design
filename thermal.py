# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 14:22:53 2021

@author: hongyong Han

To: Do or do not. There is no try.

"""

import numpy as np
from sklearn.linear_model import Ridge



def get_thermalparameters(testset):
    ##读取数据
    data = np.loadtxt(r'C:\Users\Uaena_HY\Desktop\代码集\数据库\composition-parameters143951.txt',delimiter='\t') 

    x = data[:,:9]
    y_solves = data[:,-1]
    y_solidus = data[:,-2]
    y_liquidus = data[:,-3]
    
    #建模
    solves = Ridge().fit(x,y_solves)
    solidus = Ridge().fit(x,y_solidus)
    liquidus = Ridge().fit(x,y_liquidus)
    
    #预测
    solves_pred = solves.predict(testset)
    solidus_pred = solidus.predict(testset)
    liquidus_pred = liquidus.predict(testset)
    
    return solves_pred,solidus_pred,liquidus_pred

def get_TCPcontent(testset):
    ##读取数据
    TCP_set = np.loadtxt(r'C:\Users\Uaena_HY\Desktop\代码集\数据库\composition-TCP121032.txt',delimiter='\t')   
   
    xx =  TCP_set[:,:9]  
    yy =  TCP_set[:,-1]     
    
    #建模
    TCP = Ridge().fit(xx,yy)
    
    #预测
    TCP_pred = (TCP.predict(testset))*100
    
    return TCP_pred