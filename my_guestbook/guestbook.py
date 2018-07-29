# pip install flask-mysql  기억해라
from flask import Flask, render_template, request, url_for, redirect
from flaskext.mysql import MySQL

mysql = MySQL() #생성!

app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'test'            #상수형 변수

mysql.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/write", methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        # 고객 입력한 내용들을 받는다.    client to server
        name = request.form['name']
        subject = request.form['subject']
        content = request.form['content']
        print("이름=", name, "제목=", subject, "내용=", content)
        #테이블에 저장한다.
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "insert into guestbook(name,subject,content) values(%s,%s,%s)" #?: SQL lite , %s maria
        data = (name,subject,content)  #list : sql lite, tuple : maria
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        return redirect(url_for("list"))
    else:
        return render_template("writeform.html")

@app.route("/list")
def list():
    # DB에서 정보를 가져와서 HTML 형태로 출력한다.
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from guestbook order by no desc")
    guests = [ dict(no=row[0], name=row[1], subject=row[2], content=row[3], regdate=row[4]) for row in cursor.fetchall()]
    conn.close()
    return render_template("list.html", guests=guests)

    

if __name__ == "__main__":
    app.run(debug=True)




# Create table query
# create table guestbook(
#     no int primary key auto_increment,
#     name varchar(10) not null,
#     subject varchar(50) not null,
#     content varchar(500) not null,
#     regdate datetime default current_timestamp
# )