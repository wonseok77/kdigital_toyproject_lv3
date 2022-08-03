from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from .model_pandas import survey
from .model_pandas import major
from .model_pandas import mbti
from .model_pandas import st_method
from .model_pandas import predict

# ----------------------------------------------------------------------------------
# # 테이블 생성
# def createTable(request):
#     survey.createTableSurvey()
    
#     return HttpResponse('Create OK....')

# # 설문 데이터 입력 테스트
# def set_Survey_Insert_test(request) :

#     pgender = '남' 
#     pmbti = 'INFP' 
#     psc_goal = 600 
#     ptoeic = 400
#     pteps = 800 
#     ptoeic_sp = '800'
#     popic = '500'
#     pst_method = '독학'
#     pmajor = '공학계열'
#     psucss = 1
    
#     sql = survey.setSurveyInsert(pgender, pmbti, psc_goal, ptoeic, pteps, ptoeic_sp, popic, pst_method, pmajor, psucss)
    
#     return HttpResponse(sql)

# 엑셀파일 전처리하는 함수
def excel_cut(df):
    df.columns = ['mbti', 'st_method', 'gender', 'major', 'sc_goal', 'toeic', 'teps', 'opic', 'toeic_sp']
    
    df['st_method'] = df['st_method'].apply(lambda c:'인강' if c == '인터넷강의' \
                                            else '독학' if c == '독학' \
                                            else '학원' if c == '학원수강' \
                                            else '스터디' if c == '스터디그룹' \
                                            else '기타')
    
    df['major'] = df['major'].apply(lambda c:'공과계열' if c == '공학계열' \
                                            else '상경계열' if c == '상경계열' \
                                            else '의약계열' if c == '의약계열' \
                                            else '사회계열' if c == '사회계열' \
                                            else '예/체능계열' if c == '예/체능계열' \
                                            else '인문계열' if c == '인문계열' \
                                            else '자연계열' if c == '자연계열' \
                                            else '교육계열')
    
    df['sc_goal'] = df['sc_goal'].apply(lambda c:160 if c == '320점 미만(NH)' \
                                            else 395 if c == '320점 이상 ~ 470점 미만(IL)' \
                                            else 595 if c == '470점 이상 ~ 720점 미만(IM1)' \
                                            else 767 if c == '720점 이상 ~ 815점 미만(IM2)' \
                                            else 865 if c == '815점 이상 ~ 915점 미만(IM3)' \
                                            else 935 if c == '915점 이상 ~ 955점 미만(IH)' \
                                            else 972)
    
    df['opic'] = df['opic'].apply(lambda c:160 if c == 'NH' \
                                            else 395 if c == 'IL' \
                                            else 595 if c == 'IM1' \
                                            else 767 if c == 'IM2' \
                                            else 865 if c == 'IM3' \
                                            else 935 if c == 'IH' \
                                            else 0 if c == '해당없음' \
                                            else 972)
    df['toeic_sp'] = df['toeic_sp'].apply(lambda c:160 if c == 'NH' \
                                            else 395 if c == 'IL' \
                                            else 595 if c == 'IM1' \
                                            else 767 if c == 'IM2' \
                                            else 865 if c == 'IM3' \
                                            else 935 if c == 'IH' \
                                            else 0 if c == '해당없음' \
                                            else 972)
    
    return df

# 엑셀파일 입력하는 함수
def excel_input(request):
    file_path = 'C:/DEV/STUDY/MiniProject02/data/어학시험에_대한_설문조사.xlsx' # 파일경로
    df = pd.read_excel(file_path)
    
    df = excel_cut(df)
    
    for i in range(len(df)):
        pgender = df['gender'][i]
        pmbti = df['mbti'][i]
        psc_goal = df['sc_goal'][i]
        ptoeic = df['toeic'][i]
        pteps = df['teps'][i]
        ptoeic_sp = df['toeic_sp'][i]
        popic = df['opic'][i]
        pst_method = df['st_method'][i]
        pmajor = df['major'][i]
        
        # psucss 판별해주는 조건문
        lst_temp = [ptoeic, pteps, ptoeic_sp, popic]

        if max(lst_temp) >= psc_goal:
            psucss = 1
        else:
            psucss = 0
        
        psc_goal = int(psc_goal)
        ptoeic = int(ptoeic)
        pteps = int(pteps)
        ptoeic_sp = int(ptoeic_sp)
        popic = int(popic)
        
        rs = survey.setSurveyInsert(pgender, pmbti, psc_goal, ptoeic, pteps, ptoeic_sp, popic, pst_method, pmajor, psucss)
        
    if rs == 'OK':
        msg = '''<script>
            alert('엑셀파일 입력완료')
            location.href = '/survey/'
            </script>'''
        
    return HttpResponse(msg)
    
# 설문 참여하기 페이지
def survey_form(request):
        
    return render(
        request,
        'surveyapp/survey.html',
        {}
    )

# 설문 데이터 입력
def set_Survey_Insert(request) :
    ptoeic = request.POST.get('toeic_sc')
    pteps = request.POST.get('teps_sc')
    ptoeic_sp = request.POST.get('toeic_sp')
    popic = request.POST.get('opic_sc')

    # 어학시험점수 받아와서 해당없음 선택했을 경우 0으로 반환
    if ptoeic == '':
        ptoeic = 0
    if pteps == '':
        pteps = 0
    if ptoeic_sp == '':
        ptoeic_sp = 0
    if popic == '':
        popic = 0
    
    # 점수에 문자입력될 경우 예외처리
    try:
        ptoeic = int(ptoeic)
        pteps = int(pteps)
        ptoeic_sp = int(ptoeic_sp)
        popic = int(popic)
    except Exception:
        msg = '''<script>
            alert('올바른 점수를 입력해주세요')
            location.href = '/survey/survey_form/'
            </script>'''
        return HttpResponse(msg)
        
    pgender = request.POST.get('gender')
    pmbti = request.POST.get('E_I') + request.POST.get('S_N') + request.POST.get('T_F') + request.POST.get('J_P')
    psc_goal = int(request.POST.get('sc_goal'))
    pst_method = request.POST.get('st_method')
    pmajor = request.POST.get('major')
    
    # psucss 판별해주는 조건문
    lst_temp = [ptoeic, pteps, ptoeic_sp, popic]
    
    if max(lst_temp) >= psc_goal:
        psucss = 1
    else:
        psucss = 0
        
    # 토익점수 예외처리
    if ptoeic < 0 or ptoeic > 990:
        msg = '''<script>
            alert('올바른 점수를 입력해주세요')
            location.href = '/survey/survey_form/'
            </script>'''
        return HttpResponse(msg)
    
    # 텝스점수 예외처리
    if pteps < 0 or pteps > 600:
        msg = '''<script>
            alert('올바른 점수를 입력해주세요')
            location.href = '/survey/survey_form/'
            </script>'''
        return HttpResponse(msg)
    
    rs = survey.setSurveyInsert(pgender, pmbti, psc_goal, ptoeic, pteps, ptoeic_sp, popic, pst_method, pmajor, psucss)
    if rs == 'OK':
        msg = '''<script>
            alert('설문에 참여해주셔서 감사합니다')
            location.href = '/survey/survey_form/'
            </script>'''
        
    return HttpResponse(msg)

# ----------------------------------------------------------------------------------
# MAIN 페이지 열기
def main_open(request):
    return render(
        request,
        'surveyapp/list.html',
        {}
    )

def mbti_(request):
        
    df = mbti.get_df_mbti()
    
    gdf = mbti.get_CrossTb_mbti(df)
    
    df_total_toeic, df_total_teps, df_total_toeic_sp, df_total_opic = mbti.get_ttest_mbti()
    
    aa = mbti.df_mbti(df, gdf)
    mbti.visualization_mbti(aa)
    
    resultEI_, resultNS_, resultTF_, resultPJ_ = mbti.get_chi2_mbti(df)
    
    mean_ = mbti.mbti_mean()
    mtoeic = mean_['toeic']
    mteps = mean_['teps']
    mopic = mean_['opic']
    mtoeic_sp = mean_['toeic_sp']
    
    context = {'gdf' : gdf.to_html,
               'df_total_toeic' : df_total_toeic.to_html, 
               'df_total_teps'  : df_total_teps.to_html, 
               'df_total_toeic_sp' : df_total_toeic_sp.to_html, 
               'df_total_opic' : df_total_opic.to_html,
               'resultEI_' : resultEI_,
               'resultNS_' : resultNS_,
               'resultTF_' : resultTF_,
               'resultPJ_' : resultPJ_,
               'mtoeic' : mtoeic,
               'mteps' : mteps,
               'mopic' : mopic,
               'mtoeic_sp' : mtoeic_sp}
    

    return render(
        request,
        'surveyapp/mbti.html',
        context
    )
   
def major_(request):
    
    df = major.get_df_major()
    
    gdf = major.get_CrossTb_major(df)
    
    df_total_toeic, df_total_teps, df_total_toeic_sp, df_total_opic = major.get_ttest_major()
    
    aa = major.df_major(df, gdf)
    major.visualization_major(aa)
    
    mean_ = major.major_mean()
    mtoeic = mean_['toeic']
    mteps = mean_['teps']
    mopic = mean_['opic']
    mtoeic_sp = mean_['toeic_sp']
    
    context = {'gdf' : gdf.to_html,
               'df_total_toeic' : df_total_toeic.to_html, 
               'df_total_teps'  : df_total_teps.to_html, 
               'df_total_toeic_sp' : df_total_toeic_sp.to_html, 
               'df_total_opic' : df_total_opic.to_html,
               'mtoeic' : mtoeic,
               'mteps' : mteps,
               'mopic' : mopic,
               'mtoeic_sp' : mtoeic_sp}
    
    return render(
        request,
        'surveyapp/major.html',
        context
    )
    
def study_(request):
    
    df = st_method.get_df_st_method()
    
    gdf = st_method.get_CrossTb_st_method(df)
    
    df_total_toeic, df_total_teps, df_total_toeic_sp, df_total_opic = st_method.get_ttest_st_method()
    
    aa = st_method.df_st_method(df, gdf)
    st_method.visualization_st_method(aa)
    
    mean_ = st_method.st_method_mean()
    mtoeic = mean_['toeic']
    mteps = mean_['teps']
    mopic = mean_['opic']
    mtoeic_sp = mean_['toeic_sp']
    
    context = {'gdf' : gdf.to_html,
               'df_total_toeic' : df_total_toeic.to_html, 
               'df_total_teps'  : df_total_teps.to_html, 
               'df_total_toeic_sp' : df_total_toeic_sp.to_html, 
               'df_total_opic' : df_total_opic.to_html,
               'mtoeic' : mtoeic,
               'mteps' : mteps,
               'mopic' : mopic,
               'mtoeic_sp' : mtoeic_sp}
    
    return render(
        request,
        'surveyapp/study.html',
        context
    )

# 배경분석 페이지열기
def backg(request):
    
    return render(
        request,
        'surveyapp/background.html',
        {}
    )

# ----------------------------------------------------------------------------------
# 점수 예측
def sc_predict(df, df_val):
    x_df, y_df = predict.getPredRegDataFrame(df)
    x_df_val = df_val
    x_train_scaled, x_test_scaled = predict.setScaled(x_df,x_df_val)
    model=predict.setPredRegressor(x_train_scaled,y_df)
    pred_dict = predict.getPredRegressor(model,x_test_scaled)
    return pred_dict

# 어학시험 종류 예측
def test_predict(df, df_val):
    c_x_df, c1_y_df, c2_y_df, c3_y_df, c4_y_df = predict.getPredClaDataFrame(df)
    x_df_val = df_val
    x_train_scaled, x_test_scaled = predict.setScaled(c_x_df,x_df_val)
    c1model, c2model, c3model, c4model=predict.setPredClassifier(x_train_scaled, c1_y_df, c2_y_df, c3_y_df, c4_y_df)
    pred1, pred2, pred3, pred4=predict.getPredClassifier(x_test_scaled, c1model, c2model, c3model, c4model)
    result = predict.setClaDataFrame(pred1, pred2, pred3, pred4)
    return result

# 오픽, 토스의 경우
def pr_result(result, pred_dict):
    if result == 'OPIC' or result == 'TOEIC_SP':
        if pred_dict < 320:
            pred_dict = 'NH'
        elif pred_dict < 470 and pred_dict >= 320:
            pred_dict = 'IL'
        elif pred_dict < 720 and pred_dict >= 470:
            pred_dict = 'IM1'
        elif pred_dict < 815 and pred_dict >= 720:
            pred_dict = 'IM2'
        elif pred_dict < 915 and pred_dict >= 815:
            pred_dict = 'IM3'
        elif pred_dict < 955 and pred_dict >= 915:
            pred_dict = 'IH'
        else:
            pred_dict = 'Advance'
    return pred_dict


# 320점 미만(NH)
# 320점 이상 ~ 470점 미만(IL)
# 470점 이상 ~ 720점 미만(IM1)
# 720점 이상 ~ 815점 미만(IM2)
# 815점 이상 ~ 915점 미만(IM3)
# 915점 이상 ~ 955점 미만(IH)
# 955점 이상(AL)
# ----------------------------------------------------------------------------------
# 어학시험, 점수 예측 함수
def predict_test_sc(request):
    psc_goal = int(request.POST.get('sc_goal'))
    pmbti = request.POST.get('E_I') + request.POST.get('S_N') + request.POST.get('T_F') + request.POST.get('J_P')
    pgender = request.POST.get('gender')
    pst_method = request.POST.get('st_method')
    pmajor = request.POST.get('major')
    
    df = survey.getSurveyList()
    df = predict.setDataFrame(df)
    df_val = pd.DataFrame({'sc_goal' : [0], '남' : [0], '여' : [0], \
                           'ENTJ' : [0], 'ENTP' : [0], 'ENFJ' : [0], 'ENFP' : [0], 'ESTJ' : [0], 'ESTP' : [0], 'ESFJ' : [0], 'ESFP' : [0], \
                           'INTJ' : [0], 'INTP' : [0], 'INFJ' : [0], 'INFP' : [0], 'ISTJ' : [0], 'ISTP' : [0], 'ISFJ' : [0], 'ISFP' : [0], \
                           '학원' : [0], '인강' : [0], '스터디' : [0], '독학' : [0], '기타' : [0], \
                           '공과계열' : [0], '교육계열' : [0], '사회계열' : [0], '상경계열' : [0], \
                           '예/체능계열' : [0], '의약계열' : [0], '인문계열' : [0], '자연계열' : [0]})
    
    df_val['sc_goal'] = psc_goal
    df_val[pmbti] = 1
    df_val[pgender] = 1
    df_val[pst_method] = 1
    df_val[pmajor] = 1
    
    sc_pred = sc_predict(df, df_val)
    test_pred = test_predict(df, df_val)
    
    sc_pred = pr_result(test_pred, sc_pred)
    
    context = {'sc_pred' : sc_pred, 'test_pred' : test_pred}
    
    return render(
        request,
        'surveyapp/predict.html',
        context
    )

# 예측 사용자의 정보받아오는 페이지
def predict_user(request):

    return render(
        request,
        'surveyapp/predict_user.html',
        {}
    )