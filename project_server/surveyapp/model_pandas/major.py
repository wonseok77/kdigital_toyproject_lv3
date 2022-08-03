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
def get_df_major():
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
    
def get_CrossTb_major(df):
    # 크로스탭 만들기
    gdf = df.groupby('major')[['toeic','teps','toeic_sp','opic']].sum()
    gdf = gdf.T
    
    return gdf

def df_major(df, gdf):
    co=df['major'].unique()
    
    # 시각화를 위해서 데이터 조작
    co = list(co)
    bb = [[co[e] for i in range(4)] for e in range(len(co))]
    bb = sum(bb,[])
    aa = pd.DataFrame()
    for e in co:
        aa = pd.concat([aa, gdf[e]],axis=0)
    aa.columns = ['선호도']
    aa['단과대학'] = bb
    aa = aa.reset_index()
    aa.columns = ['시험종류','선호도','단과대학']
    
    return aa

def visualization_major(aa):
    # 한글 폰트 지정
    plt.rc('font', family = "Malgun Gothic")
    # 그래프 그리기
    fig = plt.figure(figsize=(8,7))
    sns.set_palette("pastel")
    sns.barplot(x='단과대학', y='선호도',hue='시험종류',data=aa)
    plt.legend(loc='upper right')
    fig.savefig('surveyapp/static/surveyapp/img/pref_major.png')
    
def get_ttest_major():
    tdf = survey.getSurveyList()
    
    co=tdf['major'].unique()
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
        e = df_test[tdf['major'] == q[i]]
        r = df_test[tdf['major'] == w[i]]
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
        e = df_test[tdf['major'] == q[i]]
        r = df_test[tdf['major'] == w[i]]
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
        e = df_test[tdf['major'] == q[i]]
        r = df_test[tdf['major'] == w[i]]
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
        e = df_test[tdf['major'] == q[i]]
        r = df_test[tdf['major'] == w[i]]
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
def major_mean():
    df = survey.getSurveyList()
    
    test_type = ['toeic', 'teps', 'toeic_sp', 'opic']
    mean_ = {}
    
    for e in test_type:
        df_temp = df[df[e]>0][['major',e]]
        df_temp = df_temp.groupby('major')[e].mean()
        E = '공과계열의 평균점수는 ' + str(round(df_temp['공과계열'], 2))
        I = '교육계열의 평균점수는 ' + str(round(df_temp['교육계열'], 2))
        N = '사회계열의 평균점수는 ' + str(round(df_temp['사회계열'], 2))
        S = '상경계열의 평균점수는 ' + str(round(df_temp['상경계열'], 2))
        T = '예/체능계열의 평균점수는 ' + str(round(df_temp['예/체능계열'], 2))
        F = '의약계열의 평균점수는 ' + str(round(df_temp['의약계열'], 2))
        P = '인문계열의 평균점수는 ' + str(round(df_temp['인문계열'], 2))
        J = '자연계열의 평균점수는 ' + str(round(df_temp['자연계열'], 2))
        
        mean_[e] = {'score' : [E, I, N, S, T, F, P, J]}

    return mean_

# 공과계열    
# 교육계열    
# 사회계열    
# 상경계열    
# 예/체능계열   
# 의약계열    
# 인문계열    
# 자연계열