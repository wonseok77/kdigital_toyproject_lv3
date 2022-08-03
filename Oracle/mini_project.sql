CREATE TABLE survey(
    idx 	  NUMBER(7)     NOT NULL,
    gender	  NVARCHAR2(4) 	    NOT NULL,
	mbti 	  CHAR(4) 	    NOT NULL,
    sc_goal   NUMBER(7)     NOT NULL,
    toeic	  NUMBER(7),
	teps	  NUMBER(7),
	toeic_sp  NUMBER(7),
	opic	  NUMBER(7),
    st_method NVARCHAR2(20) NOT NULL,
    major 	  NVARCHAR2(20) NOT NULL,
	sucss	  NUMBER(7)		NOT NULL,
    CONSTRAINT pk_survey PRIMARY KEY (idx)
)


idx : 인덱스(PK)
gender : 성별
mbti : 성격유형
sc_goal : 목표점수대
toeic : 토익취득점수
teps : 텝스취득점수
toeic_sp : 토스취득점수
opic : 오픽취득점수
st_method : 공부방법
major : 전공
sucss : 목표점수 달성여부