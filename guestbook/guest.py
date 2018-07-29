from flask import Flask, render_template, request, g, url_for, redirect   #render template
from sqlite3 import dbapi2 as sqlite3

# 먼저 파이썬 쉘에서 아래 명령어를 실행하여 데이터베이스를 준비한다   
#python 엔터
#>>> from guest import init_db; init_db()

DATABASE = "guest.db"       #상수 정의시 대문자로 쓴다. DB 선언

app = Flask(__name__)               #이름을 가지고 생성한다
app.config.from_object(__name__)     #configraton 환경설정  

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])      #"guest.db"  연결하는 코드

def init_db():                                      #DB 초기화
    with connect_db() as db:                        #연결하면 자동으로 해제해라
        with app.open_resource('schema.sql', mode="r") as f:    #스카마 실행한다    #create table - insert, update, delete, select
            db.cursor().executescript(f.read())     #sql 실행
        db.commit()
@app.before_request         #매 요청 들어오기 전에 
def before_request():           # DB에 연결해 놓아야함
    g.db = connect_db()

@app.teardown_request        # 매 요청 끝나면 할일
def teardown_request(ecxeption):                #before and teardown request!!
    if hasattr(g, 'db'):
        g.db.close()                #자원을 해제해라

# http://localhost:5000/
@app.route("/")                     #데코레이터 패턴
def index() :
    return render_template("index.html")        #template 폴더에 있는 index.html 실행

# http://localhost:5000/write
@app.route("/write", methods=['GET','POST'])     #URL: write 일 때 get과 post 메쏘드를 사용한다.
def write():
    if request.method == 'POST':                 #action은 write, methond는 post  : 입력
        name = request.form['name']      
        subject = request.form['subject']
        content = request.form['content']
        print('이름=', name, '제목=', subject, "내용=", content)
        sql = "insert into guest(name,subject,content) values(?,?,?)"   #??는 더하기 안하게 해준다.                               # 저장 코드 시작
        data = [ name, subject, content ]
        #db2 = connect_db() #1단계    g.db로 생략가능
        g.db.execute(sql, data)  #2           #insert 데이터 완성, 메모리까지 생성
        # print(rv.lastrowid) #0이 아니면 성공!
        # s = "저장 성공!!!"
        # if rv.lastrowid == 0:
        #     s = "저장에러 발생!"
        g.db.commit() #3
        #db2.close()   #4     g.db로 생략가능    #DB에 적용한다
        #print("성공은1, 실패는0, ok=", ok)
        return redirect(url_for("list"))
    
    else: return render_template("writeform.html")      # 처음 들어왔을 때 글쓰기 폼으로 가는 Get 메쏘드

#http://localhost:5000/list
@app.route("/list")
def list():
    sql = "select * from guest order by no desc"        #글번호의 역순으로 정렬
    cur = g.db.execute(sql)         #cursor 객체
    #print( cur.fetchall() )  전체가 메모리에 올라오는데
    guests = [ dict(no=row[0], name=row[1], subject=row[2], content=row[3], regdate=row[4]) for row in cur.fetchall()] 
    #한줄 씩땡김
    print(guests)
    return render_template("list.html", guests=guests)


#http://127.0.0.1:5000/layout
@app.route("/layout")
def layout():
    return render_template("layout.html")

#http://127.0.0.1:5000/test1
@app.route("/test1")
def test1():
    user1 = { "email":"hong@abc.com", "username":"홍길동" }
    user2 = { "email":"jangg@abc.com", "username":"장길산" }
    user3 = { "email":"im@abc.com", "username":"임꺽정" }
    users = [ user1, user2, user3 ]             #키 값구조로
    return render_template("test1.html", users=users)

if __name__ == "__main__":
    app.debug = True
    app.run() 
    