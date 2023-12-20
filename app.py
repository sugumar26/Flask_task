import os
import psycopg2
from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
actual_amt=5000
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sqlconnect", methods=["POST", "GET"])
def sqlconnect():
    conn = psycopg2.connect(
        host="localhost",
        database="sugumar",
        user='postgres',
        password='Sugu@2002',
        port=5433)

    cur = conn.cursor()

    cur.execute('''select * from students''')
    values = cur.fetchall()
    conn.commit()

    cur.close()
    conn.close()

    return render_template('index.html', data=values)

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/addnumber", methods=['GET', 'POST'])
def add():
    sum_result = 0
    num1 = 0
    num2 = 0

    if request.method == 'POST':
        num1_str = request.form.get('num1')
        num2_str = request.form.get('num2')
        if num1_str and num1_str.isdigit():
            num1 = int(num1_str)
        if num2_str and num2_str.isdigit():
            num2 = int(num2_str)
        sum_result = num1 + num2
    return render_template('add.html', data=sum_result)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/bank", methods=['GET', 'POST'])
def bank():
    global actual_amt
    actualamount =actual_amt
    amount = request.form.get('enter_the_amount')
    option = request.form.get('options')
    if option =='option1':
       actualamount += int(amount)
    elif option =='option2':
        actualamount -= int(amount)
    print("---actal amount ---",actual_amt)
    actual_amt=actualamount
    return render_template('bank.html', data=actualamount)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sugu2002@localhost:5433/sugumar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Empdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Empdata {self.first_name} {self.last_name}>'
 
db.create_all()   

@app.route("/show", methods=['GET', 'POST'])
def show():
    details=Empdata.query.all()
    return render_template('show.html', data=details)
@app.route("/addemployee", methods=['POST','GET'])
def addemployee():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        department = request.form.get('department')
        salary = request.form.get('salary')
        
        new_employee = Empdata(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            salary=salary
        )
        db.session.add(new_employee)
        db.session.commit()
        db.session.close()

        return redirect(url_for('show'))

    return render_template('addemp.html')
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    employee = Empdata.query.get(id)

    if request.method == 'POST':
        employee.first_name = request.form.get('first_name')
        employee.last_name = request.form.get('last_name')
        employee.email = request.form.get('email')
        employee.department = request.form.get('department')
        employee.salary = request.form.get('salary')

        db.session.commit()
        db.session.close()

        return redirect(url_for('show'))

    return render_template('edit.html', employee=employee)

@app.route("/delete/<int:id>",methods=['delete'])
def delete(id):
    employee = Empdata.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    db.session.close()

    return redirect(url_for('show'))
    


if __name__ == '__main__':
    app.run(debug=True)
