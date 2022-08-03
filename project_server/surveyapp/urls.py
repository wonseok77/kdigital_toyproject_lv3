from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('survey_form/', views.survey_form), # 설문페이지 열기
    
    # path('insertTest/', views.set_Survey_Insert_test), # DB 입력 테스트
    
    path('insert/', views.set_Survey_Insert), # 설문 DB 입력
    
    # path('survey_analysis/', views.survey_analysis), # 설문 분석페이지
    
    path('insertexcel/', views.excel_input), # 엑셀파일 DB 입력
    
    path('mbti/', views.mbti_), # MBTI 분석
    path('major/',views.major_), # 전공별 분석
    path('study/',views.study_), # 공부방법별 분석
    path('pred_result/',views.predict_test_sc), # 어학시험, 점수 페이지
    path('pred_user/',views.predict_user), # 예측 사용자 정보 입력 페이지
    path('background/',views.backg), # 분석배경 페이지
    path('',views.main_open),
]