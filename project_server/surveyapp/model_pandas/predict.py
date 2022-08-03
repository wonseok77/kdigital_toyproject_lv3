# 라이브러리(패키지) 불러오기
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

def setDataFrame(df):
    for i in range(len(df)):
        df.loc[i,'취득점수'] = max(df.loc[i,'toeic'],df.loc[i,'teps'],df.loc[i,'toeic_sp'],df.loc[i,'opic'])
    for i in range(len(df)):
        if df.loc[i,'toeic'] == df.loc[i,'취득점수']:
            df.loc[i,'적합시험'] = 'gtoeic'
        if df.loc[i,'teps'] == df.loc[i,'취득점수']:
            df.loc[i,'적합시험'] = 'gteps'
        if df.loc[i,'toeic_sp'] == df.loc[i,'취득점수']:
            df.loc[i,'적합시험'] = 'gtoeic_sp'
        if df.loc[i,'opic'] == df.loc[i,'취득점수']:
            df.loc[i,'적합시험'] = 'gopic'
    get_mbti = pd.get_dummies(df['mbti'])
    get_male = pd.get_dummies(df['gender'])
    get_st_method = pd.get_dummies(df['st_method'])
    get_major = pd.get_dummies(df['major'])
    get_test = pd.get_dummies(df['적합시험'])
    df = pd.concat([df,get_mbti,get_male,get_st_method,get_major,get_test],axis=1)
    df = df.drop(['idx','sucss','mbti','gender','st_method','major','적합시험','toeic','teps','toeic_sp','opic'],axis=1)
    return df

# 데이터 정제
def getPredRegDataFrame(df):
    x_df = df.iloc[:,:-4]
    x_df = x_df.drop(['취득점수'],axis=1)
    y_df = df['취득점수']
    return x_df, y_df

def setScaled(x_df,df_val):
    scaler = MinMaxScaler()
    scaler.fit(x_df)
    x_train_scaled = scaler.transform(x_df)
    x_test_scaled = scaler.transform(df_val)
    return x_train_scaled, x_test_scaled

def setPredRegressor(x_train_scaled,y_df):
    model = RandomForestRegressor()
    model.fit(x_train_scaled,y_df)
    return model

def getPredRegressor(model,x_test_scaled):
    pred = model.predict(x_test_scaled)
    pred = list(pred)
    pred_df = pd.DataFrame({'예측점수' : pred})
    pred_dict = pred_df.to_dict('records')
    pred_dict = pred_dict[0]['예측점수']
    return pred_dict



def getPredClaDataFrame(df):
    c_x_df = df.iloc[:,:-4]
    c_x_df = c_x_df.drop(['취득점수'],axis=1)
    c1_y_df = df['gtoeic']
    c2_y_df = df['gteps']
    c3_y_df = df['gtoeic_sp']
    c4_y_df = df['gopic']
    return c_x_df, c1_y_df, c2_y_df, c3_y_df, c4_y_df

def setPredClassifier(x_train_scaled, c1_y_df, c2_y_df, c3_y_df, c4_y_df):
    c1model = RandomForestClassifier()
    c1model.fit(x_train_scaled,c1_y_df)

    c2model = RandomForestClassifier()
    c2model.fit(x_train_scaled,c2_y_df)

    c3model = RandomForestClassifier()
    c3model.fit(x_train_scaled,c3_y_df)

    c4model = RandomForestClassifier()
    c4model.fit(x_train_scaled,c4_y_df)
    return c1model, c2model, c3model, c4model

def getPredClassifier(x_test_scaled, c1model, c2model, c3model, c4model):
    pred1 = c1model.predict(x_test_scaled)
    pred2 = c2model.predict(x_test_scaled)
    pred3 = c3model.predict(x_test_scaled)
    pred4 = c4model.predict(x_test_scaled)
    return pred1, pred2, pred3, pred4

def setClaDataFrame(pred1, pred2, pred3, pred4):
    pred1 = pd.DataFrame({'토익예측값':pred1}).reset_index(drop=True)
    pred2 = pd.DataFrame({'텝스예측값':pred2}).reset_index(drop=True)
    pred3 = pd.DataFrame({'토스예측값':pred3}).reset_index(drop=True)
    pred4 = pd.DataFrame({'오픽예측값':pred4}).reset_index(drop=True)
    cl_pred = pd.concat([pred1,pred2,pred3,pred4],axis=1)
    for i in range(len(cl_pred)):
        if cl_pred.loc[i,'토익예측값'] == 1 :
            cl_pred.loc[i,'예측적합시험'] = 'TOEIC'
        if cl_pred.loc[i,'텝스예측값'] == 1 :
            cl_pred.loc[i,'예측적합시험'] = 'TEPS'
        if cl_pred.loc[i,'토스예측값'] == 1 :
            cl_pred.loc[i,'예측적합시험'] = 'TOEIC_SP'
        if cl_pred.loc[i,'오픽예측값'] == 1 :
            cl_pred.loc[i,'예측적합시험'] = 'OPIC'
    
    try:
        cl_pred['예측적합시험']=cl_pred['예측적합시험'].fillna('ANYTHING')
    except Exception:
        return 'ANYTHING'
    
    result = cl_pred['예측적합시험']
    result = list(result)
    results = {'적합시험' : result}
    results = results['적합시험'][0]
    return results