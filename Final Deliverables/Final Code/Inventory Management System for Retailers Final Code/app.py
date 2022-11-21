from __future__ import print_function
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3 as sql
import re
import os
import ibm_db 


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mfb71612;PWD=mFTq4HCfJpkesNCD",'','')




app=Flask(__name__)
app.secret_key ='asd'

@app.route('/main')
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard():
     sql = "SELECT COUNT(*) FROM shops"
     stmt = ibm_db.exec_immediate(conn, sql)
     shop = ibm_db.fetch_both(stmt)
     numshop=shop["1"]
     sql = "SELECT COUNT(*) FROM products"
     stmt = ibm_db.exec_immediate(conn, sql)
     prod = ibm_db.fetch_both(stmt)
     numprod=prod['1']
     sql = "SELECT COUNT(*) FROM location"
     stmt = ibm_db.exec_immediate(conn, sql)
     location = ibm_db.fetch_both(stmt)
     numlocation=location['1']
     
     
     if shop | prod | location:
      return render_template('dashboard.html', numshop = numshop,numprod = numprod ,numlocation = numlocation)    
 

@app.route('/products',methods = ['POST', 'GET'])
def products():
    if request.method == 'POST':
      name = request.form['name']
      quantity = request.form['quantity']
      cost = request.form['cost']

      insert_sql = "INSERT INTO PRODUCTS VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.bind_param(prep_stmt, 3, cost)
      ibm_db.execute(prep_stmt)

      products = []
      sql = "SELECT * FROM PRODUCTS"
      stmt = ibm_db.exec_immediate(conn, sql)
      dictionary = ibm_db.fetch_both(stmt)
      while dictionary != False:
        products.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
      if products:
        return render_template("products.html", products = products) 
    return render_template('products.html')
    
@app.route('/location',methods = ['POST', 'GET'])
def location():
    if request.method == 'POST':
      name = request.form['name']
      insert_sql = "INSERT INTO location VALUES (?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.execute(prep_stmt)

      location = []
      sql = "SELECT * FROM location"
      stmt = ibm_db.exec_immediate(conn, sql)
      dictionary = ibm_db.fetch_both(stmt)
      while dictionary != False:
        location.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
      if location:
        return render_template("location.html", location = location) 
    return render_template('location.html')

@app.route('/shops',methods = ['POST', 'GET'])
def shops():
    if request.method == 'POST':
      name = request.form['name']
      status = request.form['status']
    
      insert_sql = "INSERT INTO SHOPS VALUES (?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, status)
      ibm_db.execute(prep_stmt)

      shops = []
      sql = "SELECT * FROM SHOPS"
      stmt = ibm_db.exec_immediate(conn, sql)
      dictionary = ibm_db.fetch_both(stmt)
      while dictionary != False:
        shops.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
      if shops:
        return render_template("shops.html", shops = shops) 
    return render_template('shops.html')
    
@app.route('/delete/<name>')
def delete(name):
  sql = f"SELECT * FROM products WHERE name='{(name)}'"
  stmt = ibm_db.exec_immediate(conn, sql)
  products = ibm_db.fetch_row(stmt)
  if products:
    sql = f"DELETE FROM products WHERE name='{(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    products = []
    sql = "SELECT * FROM products"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt) 
    while dictionary != False:
      products.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if products:
      return render_template("products.html", products = products)
  return render_template("products.html")

@app.route('/dele/<name>')
def dele(name):
  sql = f"SELECT * FROM shops WHERE name='{(name)}'"
  stmt = ibm_db.exec_immediate(conn, sql)
  store = ibm_db.fetch_row(stmt)
  if store:
    sql = f"DELETE FROM shops WHERE name='{(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    shops = []
    sql = "SELECT * FROM shops"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt) 
    while dictionary != False:
      shops.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if shops:
      return render_template("shops.html", shops = shops)
  return render_template("shops.html")

@app.route('/dellocation/<name>')
def dellocation(name):
  sql = f"SELECT * FROM location WHERE name='{(name)}'"
  stmt = ibm_db.exec_immediate(conn, sql)
  location = ibm_db.fetch_row(stmt)
  if location:
    sql = f"DELETE FROM location WHERE name='{(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)
    location = []
    sql = "SELECT * FROM location"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt) 
    while dictionary != False:
      location.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if location:
      return render_template("location.html",  location =  location)
  return render_template("location.html")



@app.route('/index')
def index():
    return render_template('index.html')      

@app.route('/user/<id>')
def user_info(id):
    with sql.connect('inventorymanagement.db') as con:
        con.row_factory=sql.Row
        cur =con.cursor()
        cur.execute(f'SELECT * FROM register WHERE email="{id}"')
        user = cur.fetchall()
    return render_template("user_info.html", user=user[0]) 

@app.route('/signin',methods =['GET', 'POST'])
def signin():
    global userid
    msg = ''
    if request.method == 'POST' :
        un = request.form['username']
        pd = request.form['password']
        sql = "SELECT * FROM register WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,un)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg = msg)

        
@app.route('/signup', methods=['POST','GET'])
def signup():
    msg=''
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        pw=request.form['password'] 
        sql='SELECT * FROM register WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            msg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Please enter the avalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg='name must contain only character and number'
        else:
            insert_sql='INSERT INTO register VALUES (?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,username)
            ibm_db.bind_param(pstmt,2,email)
            ibm_db.bind_param(pstmt,3,pw)
            ibm_db.execute(pstmt)
            msg='You have successfully registered click signin!!'
            return render_template("signin.html")   
     
         
    elif request.method == 'POST':
        msg="fill out the form first!"
    return render_template("signup.html",msg=msg)


    """ import sendgrid
    from sendgrid.helpers.mail import *


    sg = sendgrid.SendGridAPIClient(api_key='SENDGRID_API_KEY')
    from_email = Email("81519104009@smartinternz.com")
    to_email = To("815119104025@smartinternz.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers) """


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')
