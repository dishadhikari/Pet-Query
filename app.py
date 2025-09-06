from flask import Flask, request, redirect, render_template,url_for
import mysql.connector

app=Flask(__name__)

db=mysql.connector.connect(
    host="localhost",
    database="disha",
    user="root",
    password="standard20"
)
cursor=db.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/petquery')
def petquery():
    cursor.execute("select qid,title from questions order by time desc")
    questions=cursor.fetchall()
    return render_template('petquery.html',questions=questions)

@app.route('/question/<int:qid>')
def viewq(qid):
    cursor.execute("select*from questions where qid=%s",(qid,))
    question=cursor.fetchone()
    cursor.execute("select*from answers where qid=%s order by atime desc",(qid,))
    answers=cursor.fetchall()
    return render_template('answer.html',question=question,answers=answers)

@app.route('/add',methods=['POST'])
def add():
    q=request.form['question']
    cursor.execute(
        "insert into questions (title,time) values(%s,now())",(q,)
    )
    db.commit()
    cursor.execute("select qid,title from questions order by time desc")
    questions=cursor.fetchall()
    return render_template('petquery.html',message="Query submitted successfully",questions=questions)

@app.route('/addans',methods=['POST'])
def addans():
    a=request.form['answer']
    qid=request.form['qid']
    cursor.execute("insert into answers(answer,atime,qid)values (%s,now(),%s)",(a,qid))
    db.commit()
    cursor.execute("select*from questions where qid=%s",(qid,))
    question=cursor.fetchone()
    cursor.execute("select*from answers where qid=%s order by atime desc",(qid,))
    answers=cursor.fetchall()
    return render_template('answer.html',message="Answer submitted successfully",question=question,answers=answers)

if __name__=="__main__":
    app.run(debug=True)