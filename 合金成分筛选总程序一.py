# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:57:53 2021

@author: hongyong Han

To: Do or do not. There is no try.

"""

################################  合金筛选总程序一 ###############################
"""
Workflow:
1. 生成成分空间
2. 采用热力学模型 计算出固相线温度、γ'相溶解温度、1100℃TCP相含量 wt.%
3. 筛选：固相线温度≥1330℃、γ'相溶解温度≥1250℃、热处理窗口≥30℃ 
4. 对3剩下的合金：采用 matlab 加速版寿命预测程序 预测1100℃/137MPa 合金蠕变寿命
"""
"""
Important parameters description:
1. Compositions:原始成分空间,不含Ti Nb
2. thermal_selected、selected_1: 经热力学筛选后剩余的合金，包括 成分（没Ti Nb)、固液相线、溶解温度、TCP  
3. selected2、selected_2：经蠕变寿命筛选后，满足条件的合金
4. micro_parameters、finall:最终结果
"""
## 准备工作，导入各种用到的包
import numpy as np
import pandas as pd
import thermal


## 1.生成成分空间
import itertools    
Al=np.arange(5.8,6.3,0.2)    #如果想固定一个元素含量不变，写成np.arange(n,n+1,1),即元素含量固定为n
Co=np.arange(8.5,9.7,0.2)   #[start,stop,step) 左闭右开  建立各元素筛选范围 
Cr=np.arange(3,3.6,0.2)  #运行过程如果出现MemoryError，内存溢出，原因是数据量太大，电脑处理不了
Mo=np.arange(1,1.7,0.2)
Re=np.arange(4.5,5.5,0.4)
Ru=np.arange(3,4,0.2)
Ta=np.arange(7,9,0.4)
W =np.arange(3,4,0.2)

p=0
total = len(Al)*len(Co)*len(Cr)*len(Mo)*len(Re)*len(Ru)*len(Ta)*len(W)
predict=np.zeros((total, 8),dtype=float)
for i in itertools.product(Al,Co,Cr,Mo,Re,Ru,Ta,W):
    predict[p,:] = i
    p+=1
Ni = 100-(predict.sum(axis=1))

Compositions =np.concatenate((Ni.reshape(total,1),predict),axis=1)
com = pd.DataFrame(Compositions,columns=['Ni','Al','Co','Cr','Mo','Re','Ru','Ta','W'])

end ="C:/Users/Uaena_HY/Desktop/李老师三代单晶/结果汇总1.xlsx"  #按需更改
writer = pd.ExcelWriter(end)                                         
com.to_excel(writer,sheet_name="composition space")

## 2.采用热力学模型 计算出固相线温度、γ'相溶解温度、1100℃TCP相含量 wt.% 、热处理窗口
# a)计算出固相线温度、γ'相溶解温度
solves_pred,solidus_pred,liquidus_pred = thermal.get_thermalparameters(Compositions)
# b) 1100℃TCP相含量 
TCP_pred = thermal.get_TCPcontent(Compositions)
# c) 热处理窗口
heatwindow = solidus_pred - solves_pred
# 转成dataframe
data_1 = np.concatenate((Compositions,solves_pred.reshape(total,1),solidus_pred.reshape(total,1),
                            liquidus_pred.reshape(total,1),heatwindow.reshape(total,1),TCP_pred.reshape(total,1)),axis=1)
thermal_filter = pd.DataFrame(data_1, columns=['Ni','Al','Co','Cr','Mo','Re','Ru','Ta',
                      'W','solves','solidus','liquidus','heatwindow',
                      'TCP'])
## 3.筛选热力学参数:固相线温度≥1330℃、γ'相溶解温度≥1250℃、热处理窗口≥40℃
j=0
judged=np.zeros((len(thermal_filter), np.size(thermal_filter,axis=1)),dtype=float)
for i in range (len(thermal_filter)):
    judge_output= thermal_filter.iloc[i]
    if judge_output['solidus']>=1300:
        print('solidus is ok')
        if judge_output['solves']>=1200:  #预测出的值大概比JmatPro计算的低15度
            print('solves is ok')
            if judge_output['heatwindow']>=20:
                print('heatwindow is ok')                
                judged[i,:]=judge_output
                j=j+1
print("\n")
print('there are', total ,'alloys in search space')  
print('there are', j, 'alloys satisfy thermal conditions')    
print("\n")

thermal_selected=np.zeros((j, np.size(judged,axis=1)),dtype=float)
l=0
for k in range (len(judged)): 
    if  judged[k,:].any()!=0: 
        thermal_selected[l,:]=judged[k,:]    
        l+=1                

# 经过热力学参数筛选后,满足条件的合金        
selected_1 = pd.DataFrame(thermal_selected, columns=['Ni','Al','Co','Cr','Mo','Re','Ru','Ta',
                      'W','solvus','solidus','liquidus','heatwindow',
                      'TCP'])

selected_1.to_excel(writer,sheet_name="after_thermal")


## 4. 生成符合蠕变寿命预测的excle表、matlab预测、导入预测结果
# a) 生成符合蠕变寿命预测的excle表
Ti = np.full(shape=[j,1],fill_value=0)
Nb = np.full(shape=[j,1],fill_value=0)
temperature = np.full(shape=[j,1],fill_value=1100)
stress = np.full(shape=[j,1],fill_value=137)
elements = thermal_selected[:,:9]
life_predict = np.concatenate((elements,Ti,Nb,temperature,stress),axis=1)

life_dataset = pd.DataFrame(life_predict, columns=['Ni','Al','Co','Cr','Mo','Re','Ru','Ta',
                      'W','Ti','Nb','temperature','stress'])

life_dataset.to_excel(writer,sheet_name="life_dataset")
writer.save()
writer.close()




