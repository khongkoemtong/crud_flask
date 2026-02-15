from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import os
import uuid
from functools import wraps



app = Flask(__name__)

app.secret_key = "123"

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


def login_require(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if 'user_id' not in session:
            
            return redirect(url_for('login'))
        return f(*args, **kwargs)
        
    return decorated_function

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/')
@login_require
def home():
    conect = connect_db()
    cursor = conect.cursor()

    cursor.execute("SELECT * FROM user")
    user = cursor.fetchall()

    return render_template('index.html',myuser =user)

@app.route('/insert',methods=["POST"])
@login_require
def insert():
    conect = connect_db()
    cursor = conect.cursor()

    name = request.form['hello']
    age=request.form['age']
    gender = request.form['gender']
    salary = request.form['salary']

    file = request.files['image']

    if file:
        pus_file = os.path.splitext(file.filename)[1]
        file_name = str(uuid.uuid4()) + pus_file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))

    sql = "INSERT INTO user (name,age,gender,salary,image) value (%s,%s,%s,%s,%s)"
    cursor.execute(sql,(name,age,gender,salary,file_name))
    conect.commit()
    return redirect(url_for('home'))

@app.route('/update',methods=["POST"])
@login_require
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

@app.route('/delete',methods=["POST"])
@login_require
def delete ():
    connection = connect_db()
    cursor = connection.cursor()
    id= request.form['id']

    sql = "DELETE FROM USER WHERE id =%s"
    cursor.execute(sql,(id))
    connection.commit()

    return redirect(url_for('home'))



@app.route('/userpage')
def userpage ():
    conection = connect_db()
    cursor = conection.cursor()

    cursor.execute( "SELECT * FROM user")
    alluser = cursor.fetchall()
    return render_template("userpage.html",user=alluser)


@app.route('/register',methods=['POST','GET'])
def register():
    error=""
    if request.method=="POST" :
        contion = connect_db()
        cursor = contion.cursor()

        username = request.form['username']
        email = request.form['email']
        pasword = request.form['password']

       
        try:
            sql = "INSERT INTO accounts (username,email,password) values(%s,%s,%s)"
            cursor.execute(sql,(username,email,pasword))
            contion.commit()
            error = "insert success"
        except Exception as e :
            error = ("can not insert data",e)
            
 


    return render_template("register.html",error =error)


@app.route('/login',methods=['POST','GET'])
def login():
    error = ""
    if request.method=='POST':

        contion= connect_db()
        cursor = contion.cursor()
        email = request.form['email']
        password = request.form['password']

        try:
            sql =("SELECT * FROM  accounts WHERE  email=%s AND password =%s")
            cursor.execute(sql,(email,password))
            acount =cursor.fetchone()
            error="Login success"

            if acount:
                acount['user_id']=acount[0]
                acount['user_name']=acount[1]
                return redirect(url_for('home'))
            
        except Exception as e :
            error="Can not find email and password ",e
            return redirect(url_for('login'))
    return render_template('login.html',error=error)


        





if __name__ =="__main__":
    print('server is running 🎉')
    app.run(debug=True)