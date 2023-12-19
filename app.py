import os
import psycopg2
from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run(debug=True)
