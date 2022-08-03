import pandas as pd
import cx_Oracle as ora
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
# 한글 폰트 지정
plt.rc('font', family = "Malgun Gothic")

# ----------------------------------------------------------------------------------
# 오라클 연결 및 접속하기
def getConnection() :
    dsn = ora.makedsn('192.168.0.113', 1521, service_name='orcl')
    conn = ora.connect(user='mini_project', password='dbdbdb', dsn=dsn)
    return conn

# 커서 받기
def getCursor(conn):
    cursor = conn.cursor()
    return cursor

# 접속 정보 및 커서 반납하기
def dbClose(cursor, conn):
    cursor.close()
    conn.close()

# ----------------------------------------------------------------------------------
# 열이름 받아오기
def getColList(col, row):
    col_dict = {}
    
    for i in range(len(row)):
        col_dict[col[i].lower()] = row[i]
    
    return col_dict

# 여러건에 대한 리스트 + 딕셔너리 만드는 함수
def getDictType_FetchAll(col_name, row):
    list_row = []

    for tup in row:
        col_dict = {}
        
        for i in range(len(tup)):
            col_dict[col_name[i].lower()] = tup[i]
        
        list_row.append(col_dict)
    
    return list_row

# ----------------------------------------------------------------------------------
# survey 테이블 생성하기
def createTableSurvey():
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = '''CREATE TABLE user_data(
                idx 	  NUMBER(7)    NOT NULL,
                mbti 	  CHAR(4) 	   NOT NULL,
                test_type VARCHAR2(10) NOT NULL,
                sc_goal   NUMBER(7)    NOT NULL,
                sc_curr   NUMBER(7)    NOT NULL,
                st_method VARCHAR2(40) NOT NULL,
                major 	  VARCHAR2(10) NOT NULL,
                CONSTRAINT pk_idx PRIMARY KEY (idx)
)'''
    
    cursor.execute(sql)
    
    dbClose(cursor, conn)
    
# survey 정보 입력
def setSurveyInsert(pgender, pmbti, psc_goal, ptoeic, pteps, ptoeic_sp, popic, pst_method, pmajor, psucss):
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = '''SELECT NVL(MAX(idx)+1 ,1) as max_no
                FROM survey'''
    
    cursor.execute(sql)
    rs_max_no = cursor.fetchone()
    no = rs_max_no[0]
        
    sql = '''INSERT INTO survey(
                idx, gender, mbti, sc_goal, toeic, teps, toeic_sp, opic, st_method, major, sucss
                ) values (
                :idx, :gender, :mbti, :sc_goal, :toeic, :teps, :toeic_sp, :opic, :st_method, :major, :sucss
                )'''
                
    # sql = '''INSERT INTO survey(
    #             idx, gender, mbti, sc_goal, toeic, teps, toeic_sp, opic, st_method, major, sucss
    #             ) values (
    #             1, '남', 'INFP', 600, 400, 800, '800', '500', '독학', '공학계열', 1
    #             )'''
    
    # cursor.execute(sql,
    #                idx = 2, 
    #                gender = '남', 
    #                mbti = 'INFP', 
    #                sc_goal = 600, 
    #                toeic = 400, 
    #                teps = 800, 
    #                toeic_sp = '800', 
    #                opic = '500', 
    #                st_method = '독학', 
    #                major = '공학계열', 
    #                sucss = 1
    #                )
    
    cursor.execute(sql,
                   idx = no, 
                   gender = pgender, 
                   mbti = pmbti, 
                   sc_goal = psc_goal, 
                   toeic = ptoeic, 
                   teps = pteps, 
                   toeic_sp = ptoeic_sp, 
                   opic = popic, 
                   st_method = pst_method, 
                   major = pmajor, 
                   sucss = psucss
                   )
    
    conn.commit()
    
    dbClose(cursor, conn)
    return 'OK'

# 설문 전체리스트 조회
def getSurveyList():
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = ''' SELECT *
    FROM survey '''
    
    cursor.execute(sql)
    
    row = cursor.fetchall()
    
    col_name = cursor.description
    col = []
    for i in col_name:
        col.append(i[0].lower())
    
    dbClose(cursor, conn)
    
    # 데이터 프레임에 조회 결과 넣기
    df = pd.DataFrame(row, columns = col)
    
    df = df.sort_values(by='idx')
    
    return df
