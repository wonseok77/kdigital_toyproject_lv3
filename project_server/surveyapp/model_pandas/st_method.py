from django.http import HttpResponse
from django.shortcuts import render
from . import survey
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from django.core.paginator import Paginator

# ----------------------------------------------------------------------------------


# 전공별 어학시험별 크로스탭, 시각화, 분석결과 받아오기
def get_df_st_method():
    # DB에서 전체조회해서 데이터프레임에 담기
    df = survey.getSurveyList()
    
    # 어학시험별로 점수가 있을 경우 1, 없을 경우 0으로 치환
    for e in range(4, 8):
        for i in range(len(df)):
            if int(df.iloc[i, e]) > 0 :
                df.iloc[i, e] = 1
            else :
                df.iloc[i, e] = 0
    
    return df
    
def get_CrossTb_st_method(df):
    # 크로스탭 만들기
    gdf = df.groupby('st_method')[['toeic','teps','toeic_sp','opic']].sum()
    gdf = gdf.T
    
    return gdf

def df_st_method(df, gdf):
    co=df['st_method'].unique()
    
    # 시각화를 위해서 데이터 조작
    co = list(co)
    bb = [[co[e] for i in range(4)] for e in range(len(co))]
    bb = sum(bb,[])
    aa = pd.DataFrame()
    for e in co:
        aa = pd.concat([aa, gdf[e]],axis=0)
    aa.columns = ['선호도']
    aa['st_method'] = bb
    aa = aa.reset_index()
    aa.columns = ['시험종류','선호도','공부방법']
    
    return aa

def visualization_st_method(aa):
    # 한글 폰트 지정
    plt.rc('font', family = "Malgun Gothic")
    # 그래프 그리기
    fig = plt.figure(figsize=(8,7))
    sns.set_palette("pastel")
    sns.barplot(x='시험종류', y='선호도',hue='공부방법',data=aa)
    plt.legend(loc='upper right')
    fig.savefig('surveyapp/static/surveyapp/img/pref_st_method.png')
    
def get_ttest_st_method():
    tdf = survey.getSurveyList()
    
    co=tdf['st_method'].unique()
    co = list(co)

    # t검정을 활용해서 순위매기기(토익)
    df_test = tdf['toeic'] # 토익에 대해서만 체크
    df_total_toeic = pd.DataFrame() # 빈 데이터프레임 작성
    from itertools import combinations
    a = list(combinations(co, 2))
    q = []
    w = []
    for i in range(len(a)):
        q.append(a[i][0])
        w.append(a[i][1])
    for i in range(len(q)):
        e = df_test[tdf['st_method'] == q[i]]
        r = df_test[tdf['st_method'] == w[i]]
        statis, pv = stats.ttest_ind(e, r)
        df_temp = pd.DataFrame({'비교대상' : [q[i]+' vs '+w[i]], '검정통계량' : abs(statis), 'p-value' : pv})
        df_total_toeic = pd.concat([df_total_toeic, df_temp])
    df_total_toeic['검정통계량'] = round(df_total_toeic['검정통계량'], 3)
    df_total_toeic['p-value'] = round(df_total_toeic['p-value'], 3)
    
    # t검정을 활용해서 순위매기기(텝스)
    df_test = tdf['teps'] # 토익에 대해서만 체크
    df_total_teps = pd.DataFrame() # 빈 데이터프레임 작성
    from itertools import combinations
    a = list(combinations(co, 2))
    q = []
    w = []
    for i in range(len(a)):
        q.append(a[i][0])
        w.append(a[i][1])
    for i in range(len(q)):
        e = df_test[tdf['st_method'] == q[i]]
        r = df_test[tdf['st_method'] == w[i]]
        statis, pv = stats.ttest_ind(e, r)
        df_temp = pd.DataFrame({'비교대상' : [q[i]+' vs '+w[i]], '검정통계량' : abs(statis), 'p-value' : pv})
        df_total_teps = pd.concat([df_total_teps, df_temp])
    df_total_teps['검정통계량'] = round(df_total_teps['검정통계량'], 3)
    df_total_teps['p-value'] = round(df_total_teps['p-value'], 3)
    
    # t검정을 활용해서 순위매기기(토익스피킹)
    df_test = tdf['toeic_sp'] # 토익에 대해서만 체크
    df_total_toeic_sp = pd.DataFrame() # 빈 데이터프레임 작성
    from itertools import combinations
    a = list(combinations(co, 2))
    q = []
    w = []
    for i in range(len(a)):
        q.append(a[i][0])
        w.append(a[i][1])
    for i in range(len(q)):
        e = df_test[tdf['st_method'] == q[i]]
        r = df_test[tdf['st_method'] == w[i]]
        statis, pv = stats.ttest_ind(e, r)
        df_temp = pd.DataFrame({'비교대상' : [q[i]+' vs '+w[i]], '검정통계량' : abs(statis), 'p-value' : pv})
        df_total_toeic_sp = pd.concat([df_total_toeic_sp, df_temp])
    df_total_toeic_sp['검정통계량'] = round(df_total_toeic_sp['검정통계량'], 3)
    df_total_toeic_sp['p-value'] = round(df_total_toeic_sp['p-value'], 3)
    
    # t검정을 활용해서 순위매기기(오픽)
    df_test = tdf['opic'] # 토익에 대해서만 체크
    df_total_opic = pd.DataFrame() # 빈 데이터프레임 작성
    from itertools import combinations
    a = list(combinations(co, 2))
    q = []
    w = []
    for i in range(len(a)):
        q.append(a[i][0])
        w.append(a[i][1])
    for i in range(len(q)):
        e = df_test[tdf['st_method'] == q[i]]
        r = df_test[tdf['st_method'] == w[i]]
        statis, pv = stats.ttest_ind(e, r)
        df_temp = pd.DataFrame({'비교대상' : [q[i]+' vs '+w[i]], '검정통계량' : abs(statis), 'p-value' : pv})
        df_total_opic = pd.concat([df_total_opic, df_temp])
    df_total_opic['검정통계량'] = round(df_total_opic['검정통계량'], 3)
    df_total_opic['p-value'] = round(df_total_opic['p-value'], 3)
        
    df_total_toeic.sort_values('검정통계량', ascending=False, inplace=True)
    df_total_teps.sort_values('검정통계량', ascending=False, inplace=True)
    df_total_toeic_sp.sort_values('검정통계량', ascending=False, inplace=True)
    df_total_opic.sort_values('검정통계량', ascending=False, inplace=True)
    
    df_total_toeic = df_total_toeic.head(10)
    df_total_teps = df_total_teps.head(10)
    df_total_toeic_sp = df_total_toeic_sp.head(10)
    df_total_opic = df_total_opic.head(10)
    
    df_total_toeic = df_total_toeic.reset_index(drop = True)
    df_total_teps = df_total_teps.reset_index(drop = True)
    df_total_toeic_sp = df_total_toeic_sp.reset_index(drop = True)
    df_total_opic = df_total_opic.reset_index(drop = True)
    
    return df_total_toeic, df_total_teps, df_total_toeic_sp, df_total_opic

# 최종결론에 띄울 함수(평균 단순 비교)
def st_method_mean():
    df = survey.getSurveyList()
    
    test_type = ['toeic', 'teps', 'toeic_sp', 'opic']
    mean_ = {}
    
    for e in test_type:
        df_temp = df[df[e]>0][['st_method',e]]
        df_temp = df_temp.groupby('st_method')[e].mean()
        E = '학원의 평균점수는 ' + str(round(df_temp['학원'], 2))
        I = '인강의 평균점수는 ' + str(round(df_temp['인강'], 2))
        N = '스터디의 평균점수는 ' + str(round(df_temp['스터디'], 2))
        S = '독학의 평균점수는 ' + str(round(df_temp['독학'], 2))
        T = '기타의 평균점수는 ' + str(round(df_temp['기타'], 2))

        mean_[e] = {'score' : [E, I, N, S, T]}

    return mean_


# 기타    
# 독학    
# 스터디   
# 인강 
# 학원 