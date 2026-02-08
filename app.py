from flask import Flask,render_template,request,redirect,url_for
import pymysql


app = Flask(__name__)
def connect_db():
    conection = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        db='my_python',
    )
    if not conection:
        print("can not connect to database ")
    print("connect to database success !")    
    return conection
connect_db()
@app.route('/')
def home():
    conect = connect_db()
    cursor = conect.cursor()

    cursor.execute("SELECT * FROM user")
    user = cursor.fetchall()

    return render_template('index.html',myuser =user,edit_data=None)

@app.route('/insert',methods=["POST"])
def insert ():
    conect = connect_db()
    cursor = conect.cursor()

    name = request.form['hello']
    age=request.form['age']
    gender = request.form['gender']
    salary = request.form['salary']

    sql = "INSERT INTO user (name,age,gender,salary) value (%s,%s,%s,%s)"
    cursor.execute(sql,(name,age,gender,salary))
    conect.commit()
    return redirect(url_for('home'))



@app.route('/update',methods=["POST"])
def update():
    conetion = connect_db()
    cursor = conetion.cursor()

    id = request.form['id']
    name= request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    salary = request.form['salary']


    sql ="UPDATE user SET name=%s,age = %s,gender=%s,salary = %s WHERE id =%s"
    cursor.execute(sql,(name,age,gender,salary,(id,)))

    conetion.commit()
    return redirect(url_for('home'))







if __name__ =="__main__":
    print('server is running 🎉')
    app.run(debug=True)