# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 16:09:27 2021

@author: hongyong Han

To: Do or do not. There is no try.

"""

################################  合金筛选总程序二 ###############################
"""
Workflow:
4. 生成符合蠕变寿命预测的excle表、matlab预测、导入预测结果    
5. 筛选出蠕变寿命大于等于400h的合金（与TMS-138 对比）
6. 计算从5剩下的成分的 γ'体积分数、厚度、长宽比、JMatPro——TCP + 2.11*成分多项式 - 36.89
"""
## 准备工作，导入各种用到的包
import numpy as np
import pandas as pd
import openpyxl
import thermal
import microstructure
#
# 4 b) 导入寿命预测结果
end = "C:/Users/Uaena_HY/Desktop/李老师三代单晶/结果汇总1.xlsx"  #按需更改
life_predicted = pd.read_excel(end,sheet_name="life_dataset")

## 5.筛选寿命大于400h的合金
jj=0
judged=np.zeros((len(life_predicted), np.size(life_predicted,axis=1)),dtype=float)
for ii in range (len(life_predicted)):
    judge_output= life_predicted.iloc[ii]
    if judge_output['life']>=100:
        #print('life is ok')
        judged[ii,:]=judge_output
        jj=jj+1

j = len(life_predicted)
print("\n")
print('there are', j ,'alloys in search space')  
print('there are', jj, 'alloys predicted life more than 400h')    

selected2=np.zeros((jj, np.size(judged,axis=1)),dtype=float)
ll=0
for kk in range (len(judged)): 
    if  judged[kk,:].any()!=0: 
        selected2[ll,:]=judged[kk,:]    
        ll+=1                

# 经过1100℃/137MPa蠕变寿命筛选后,满足条件的合金        
selected_2 = pd.DataFrame(selected2, columns=['num','Ni','Al','Co','Cr','Mo','Re','Ru','Ta',
                      'W','Ti','Nb','temperature','stress','life'])


wb = openpyxl.load_workbook(end)
writer = pd.ExcelWriter(r'结果汇总1.xlsx',engine='openpyxl')
writer.book = wb
writer.sheets = {ws.title:ws for ws in wb.wooksheets}
selected_2.to_excel(writer,sheet_name="after_life",index=False)    

   
## 6.计算selected_2成分的 γ'体积分数、厚度、长宽比、JMatPro——TCP + 2.11*成分多项式 - 36.89
# a)计算FeretRatio 
set1 = selected2[:,1:10]
set2 = selected2[:,2:10]
Feret_Ratio = microstructure.get_FeretRatio(set1)
Feret_Ratio = Feret_Ratio.reshape(len(set1),1)
# b)计算thickness
gammaprime_thickness = microstructure.get_thickness(set1)
gammaprime_thickness = gammaprime_thickness.reshape(len(set1),1)
# c)计算volumefraction
gammaprime_volume = microstructure.get_volumefraction(set2)
gammaprime_volume = gammaprime_volume.reshape(len(set2),1)
# d1)计算成分多项式
Ni = selected_2['Ni']/58.69
Al = selected_2['Al']/26.98
Co = selected_2['Co']/58.93
Cr = selected_2['Cr']/52
Mo = selected_2['Mo']/95.94
Re = selected_2['Re']/186.2
Ru = selected_2['Ru']/101.1
Ta = selected_2['Ta']/180.9
W  = selected_2['W']/183.8
Ti = selected_2['Ti']/47.9
Nb = selected_2['Nb']/92.9
total = Ni+Al+Co+Cr+Mo+Re+Ru+Ta+W+Ti+Nb
Atom_Ni = (Ni/total)*100
Atom_Al = (Al/total)*100
Atom_Co = (Co/total)*100
Atom_Cr = (Cr/total)*100  
Atom_Mo = (Mo/total)*100
Atom_Re = (Re/total)*100
Atom_Ru = (Ru/total)*100  
Atom_Ta = (Ta/total)*100
Atom_W  = (W/total)*100


composition_polynomial = (Atom_Ta+1.5*Atom_Re+0.75*(Atom_Cr+Atom_Mo)+
                         0.5*(Atom_Al+Atom_W)- 0.4*Atom_Ru)
# d2)计算1100℃TCP含量
TCPcontent = thermal.get_TCPcontent(set1)                         
# d3)计算TCP判式
TCP_judgement = microstructure.TCP_judge(TCPcontent, composition_polynomial)
TCP_judgement = np.array(TCP_judgement).reshape(len(set1),1)
# e)汇总
micro_parameters = np.concatenate((selected2,Feret_Ratio,gammaprime_thickness,
                                   gammaprime_volume,TCP_judgement),axis=1)

finall = pd.DataFrame(micro_parameters,columns=['num','Ni','Al','Co','Cr','Mo','Re','Ru','Ta',
                      'W','Ti','Nb','temperature','stress','life',
                      'FeretRatio','thickness','Vf','TCP_judgement'])


finall.to_excel(writer,sheet_name="finall results",index=False)    
writer.save()
writer.close()