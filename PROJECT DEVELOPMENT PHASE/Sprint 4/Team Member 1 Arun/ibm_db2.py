import ibm_db

conn = ibm_db.connect("DATABASE:bludb; HOSTNAME= ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=31505;SECURITY=SSL;SSLServerCertificate=DigitalCertGlobalRootCA.crt;UID=mfb71612;PWD=M5oQBPWACqVkV09t",'','')
print(conn)
print("connection sucessful......")
import ibm_db
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

conn = ibm_db.connect("DATABASE:bludb; HOSTNAME= ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=31505;SECURITY=SSL;SSLServerCertificate=DigitalCertGlobalRootCA.crt;UID=mfb71612;PWD=M5oQBPWACqVkV09t",'','')
print(conn)
print("connection sucessful......")

app = Flask(__name__)



@app.route('/')
def home():
  return render_template('login.html')

@app.route('/checking', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = ibm_db.connect.cursor(ibm_db.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (email, password, ))
        account = cursor.fetch_assoc()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))
 




@app.route('/register',methods = ['POST', 'GET'])
def reg():
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        password= request.form['password']
        confrim_password= request.form['confrim_password']

        sql = "SELECT * FROM students WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('login.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO students VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.bind_param(prep_stmt, 4, confrim_password)
            ibm_db.execute(prep_stmt)
    
        return render_template('index.html', msg="Student Data saved successfuly..")

@app.route('/Inventory')
def home():
  return render_template('Products.html')

@app.route('/chart')
def home():
  return render_template('chart.html')

@app.route('/setting')
def home():
  return render_template('login.html')