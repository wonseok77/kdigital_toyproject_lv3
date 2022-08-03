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


# mbti별 어학시험별 크로스탭, 시각화, 분석결과 받아오기
def get_df_mbti():
    # DB에서 전체조회해서 데이터프레임에 담기
    df = survey.getSurveyList()
    
    # mbti별로 점수가 있을 경우 1, 없을 경우 0으로 치환
    for e in range(4, 8):
        for i in range(len(df)):
            if int(df.iloc[i, e]) > 0 :
                df.iloc[i, e] = 1
            else :
                df.iloc[i, e] = 0
    
    return df
    
def get_CrossTb_mbti(df):
    # 크로스탭 만들기
    gdf = df.groupby('mbti')[['toeic','teps','toeic_sp','opic']].sum()
    gdf = gdf.T
    
    return gdf

def df_mbti(df, gdf):
    co=df['mbti'].unique()
    
    # 시각화를 위해서 데이터 조작
    co = list(co)
    bb = [[co[e] for i in range(4)] for e in range(len(co))]
    bb = sum(bb,[])
    aa = pd.DataFrame()
    for e in co:
        aa = pd.concat([aa, gdf[e]],axis=0)
    aa.columns = ['선호도']
    aa['mbti'] = bb
    aa = aa.reset_index()
    aa.columns = ['시험종류','선호도','mbti']
    
    return aa

def visualization_mbti(aa):
    # 한글 폰트 지정
    plt.rc('font', family = "Malgun Gothic")
    # 그래프 그리기
    fig = plt.figure(figsize=(8,7))
    sns.set_palette("pastel")
    sns.barplot(x='시험종류', y='선호도',hue='mbti',data=aa)
    plt.legend(loc='upper right')
    fig.savefig('surveyapp/static/surveyapp/img/pref_mbti.png')
    
def get_ttest_mbti():
    tdf = survey.getSurveyList()
    
    co=tdf['mbti'].unique()
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
        e = df_test[tdf['mbti'] == q[i]]
        r = df_test[tdf['mbti'] == w[i]]
        statis, pv = stats.ttest_ind(e, r)
        df_temp = pd.DataFrame({'비교대상' : [q[i]+' vs '+w[i]], '검정통계량' : abs(statis), 'p-value' : pv})
        df_total_toeic = pd.concat([df_total_toeic, df_temp])
    df_total_toeic['검정통계량'] = round(df_total_toeic['검정통계량'], 3)
    df_total_toeic['p-value'] = round(df_total_toeic['p-value'], 3)
    
    # t검정을 활용해서 순위매기기(텝스)
    df_test = tdf['teps'] # 텝스에 대해서만 체크
    df_total_teps = pd.DataFrame() # 빈 데이터프레임 작성
    from itertools import combinations
    a = list(combinations(co, 2))
    q = []
    w = []
    for i in range(len(a)):
        q.append(a[i][0])
        w.append(a[i][1])
    for i in range(len(q)):
        e = df_test[tdf['mbti'] == q[i]]
        r = df_test[tdf['mbti'] == w[i]]
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
        e = df_test[tdf['mbti'] == q[i]]
        r = df_test[tdf['mbti'] == w[i]]
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
        e = df_test[tdf['mbti'] == q[i]]
        r = df_test[tdf['mbti'] == w[i]]
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

def get_chi2_mbti(df):
    # 유형별로 MBTI 자르기
    df['EI'] = df['mbti'].str[0:1]
    df['NS'] = df['mbti'].str[1:2]
    df['TF'] = df['mbti'].str[2:3]
    df['PJ'] = df['mbti'].str[3:4]
    
    # 데이터프레임 복사
    kdf = df.copy()
    
    # 어학시험별로 나누기
    ttoeic = df[['idx','toeic']]
    tteps = df[['idx','teps']]
    ttos = df[['idx','toeic_sp']]
    topic = df[['idx','opic']]
    
    
    for i in range(len(ttoeic)):
        if ttoeic['toeic'][i] == 1:
            ttoeic.loc[i,'토익여부'] = 'toeic'
        else:
            ttoeic.loc[i,'토익여부'] = 0
    ttoeic = ttoeic[ttoeic['토익여부']!=0]
    ttoeic = ttoeic[['idx','토익여부']]
    
    for i in range(len(tteps)):
        if tteps['teps'][i] == 1:
            tteps.loc[i,'텝스여부'] = 'teps'
        else:
            tteps.loc[i,'텝스여부'] = 0
    tteps = tteps[tteps['텝스여부']!=0]
    tteps = tteps[['idx','텝스여부']]
    
    for i in range(len(ttos)):
        if ttos['toeic_sp'][i] == 1:
            ttos.loc[i,'토익스피킹여부'] = 'toeic_sp'
        else:
            ttos.loc[i,'토익스피킹여부'] = 0
    ttos = ttos[ttos['토익스피킹여부']!=0]
    ttos = ttos[['idx','토익스피킹여부']]
    
    for i in range(len(ttos)):
        if topic['opic'][i] == 1:
            topic.loc[i,'오픽여부'] = 'opic'
        else:
            topic.loc[i,'오픽여부'] = 0
    topic = topic[topic['오픽여부']== 'opic']
    topic = topic[['idx','오픽여부']]
    
    tteps.columns = ['idx','토익여부']
    ttos.columns = ['idx','토익여부']
    topic.columns = ['idx','토익여부']
    
    cdf = pd.concat([ttoeic,tteps,ttos,topic],axis = 0)
    cdf.columns = ['idx','시험기록']
    
    kdf = pd.merge(cdf,kdf,left_on='idx',right_on='idx',how='left')
    
    ctabEI = pd.crosstab(index = kdf['EI'], columns = kdf['시험기록'])
    ctabNS = pd.crosstab(index = kdf['NS'], columns = kdf['시험기록'])
    ctabTF = pd.crosstab(index = kdf['TF'], columns = kdf['시험기록'])
    ctabPJ = pd.crosstab(index = kdf['PJ'], columns = kdf['시험기록'])
    
    ### 검정 하기
    resultEI = stats.chi2_contingency(ctabEI)
    resultNS = stats.chi2_contingency(ctabNS)
    resultTF = stats.chi2_contingency(ctabTF)
    resultPJ = stats.chi2_contingency(ctabPJ)

    if resultEI[1] > 0.05:
        resultEI_ = 'p-value 값이 유의수준 <b>{:.3f} > 0.05</b> 이므로, ' \
                '<br> 성격유형 EI에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 없다.(귀무가설 채택)</b>'.format(resultEI[1])
    else:
        resultEI_ = 'p-value 값이 유의수준 <b>{:.3f} <= 0.05</b> 이므로, ' \
                '<br> 성격유형 EI에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 있다.(대립가설 채택)</b>'.format(resultEI[1])
    
    if resultNS[1] > 0.05:
        resultNS_ = 'p-value 값이 유의수준 <b>{:.3f} > 0.05</b> 이므로, ' \
                '<br> 성격유형 NS에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 없다.(귀무가설 채택)</b>'.format(resultNS[1])
    else:
        resultNS_ = 'p-value 값이 유의수준 <b>{:.3f} <= 0.05</b> 이므로, ' \
                '<br> 성격유형 NS에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 있다.(대립가설 채택)</b>'.format(resultNS[1])
    
    if resultTF[1] > 0.05:
        resultTF_ = 'p-value 값이 유의수준 <b>{:.3f} > 0.05</b> 이므로, ' \
                '<br> 성격유형 TF에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 없다.(귀무가설 채택)</b>'.format(resultTF[1])
    else:
        resultTF_ = 'p-value 값이 유의수준 <b>{:.3f} <= 0.05</b> 이므로, ' \
                '<br> 성격유형 TF에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 있다.(대립가설 채택)</b>'.format(resultTF[1])
                
    if resultPJ[1] > 0.05:
        resultPJ_ = 'p-value 값이 유의수준 <b>{:.3f} > 0.05</b> 이므로, ' \
                '<br> 성격유형 PJ에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 없다.(귀무가설 채택)</b>'.format(resultPJ[1])
    else:
        resultPJ_ = 'p-value 값이 유의수준 <b>{:.3f} <= 0.05</b> 이므로, ' \
                '<br> 성격유형 PJ에 따라 선호하는 어학시험에는 ' \
                '<b>차이가 있다.(대립가설 채택)</b>'.format(resultPJ[1])

    return resultEI_, resultNS_, resultTF_, resultPJ_

# 최종결론에 띄울 함수(평균 단순 비교)
def mbti_mean():
    df = survey.getSurveyList()
    
    test_type = ['toeic', 'teps', 'toeic_sp', 'opic']
    mean_ = {}
    
    for e in test_type:
        df_temp = df[df[e]>0][['mbti',e]]
        df_temp['EI'] = df_temp['mbti'].str[0:1]
        df_temp['NS'] = df_temp['mbti'].str[1:2]
        df_temp['TF'] = df_temp['mbti'].str[2:3]
        df_temp['PJ'] = df_temp['mbti'].str[3:4]

        EI = df_temp.groupby('EI')[e].mean()
        E = 'E의 평균점수는 ' + str(round(EI['E'], 2))
        I = 'I의 평균점수는 ' + str(round(EI['I'], 2))

        NS = df_temp.groupby('NS')[e].mean()
        N = 'N의 평균점수는 ' + str(round(NS['N'], 2))
        S = 'S의 평균점수는 ' + str(round(NS['S'], 2))

        TF = df_temp.groupby('TF')[e].mean()
        T = 'T의 평균점수는 ' + str(round(TF['T'], 2))
        F = 'F의 평균점수는 ' + str(round(TF['F'], 2))

        PJ = df_temp.groupby('PJ')[e].mean()
        P = 'P의 평균점수는 ' + str(round(PJ['P'], 2))
        J = 'J의 평균점수는 ' + str(round(PJ['J'], 2))
        
        mean_[e] = {'score' : [E, I, N, S, T, F, P, J]}

    return mean_