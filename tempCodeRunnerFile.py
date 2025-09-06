from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

app=Flask(__name__)

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="standard20",
    database="disha"
)
cursor=db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("select*from todo where complete=%s",(0,))
    incomplete=cursor.fetchall()
    cursor.execute("select*from todo where complete=%s",(1,))
    complete=cursor.fetchall()
    return render_template('index.html',incomplete=incomplete,complete=complete)

@app.route('/add',methods=['POST'])
def add():
    todo_text=request.form['todoitem']
    cursor.execute(
        "insert into todo (text,complete) values(%s,%s)",
        (todo_text,0)
    )
    db.commit()
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    cursor.execute(
        "update todo set complete=%s where id=%s",
        (1,id)
    )
    db.commit()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)    