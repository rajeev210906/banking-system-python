from tinydb import TinyDB, Query
from flask import Flask, render_template, request,jsonify
import random
import time

user_db = TinyDB('user_db.json')
card_db = TinyDB('card_db.json')
user_table = user_db.table('Users')
card_table = card_db.table('Cards')
Card = Query()
User = Query()

app = Flask(__name__)

def gen_acc_no():
    return random.randint(541111111111, 991111111111)
# card_table.insert({'name': "DARK RANJAN",'card_no':"7479549808747954",'expiry':"2030-12-31",'card_cvv':"567",'c_type':"dark_card",'c_bal':"1000"})
def add_user(full_name, user_name, password, user_ph_no, email, acc_no, ifsc_code, acc_bal):
    user_table.insert({
        'full_name': full_name,
        'user_name': user_name,
        'password': password,
        'User_ph_no': user_ph_no,
        'User_email': email,
        'acc_no': acc_no,
        'ifsc_code': ifsc_code,
        'acc_bal': acc_bal
    })


def add_money(user_name,amount):
    user = user_table.get(User.user_name == user_name)
    new_bal = float(amount)
    username = user['user_name']
    updated_bal = float(user['acc_bal']) + new_bal

    # Update the user's balance in the database
    user_table.update({'acc_bal': updated_bal}, User.user_name == username)

    # Fetch the updated user info to display the new balance
    user = user_table.get(User.user_name == username)

def deduct_money(user_name,amount):
    user = user_table.get(User.user_name == user_name)
    new_bal = float(amount)
    username = user['user_name']
    updated_bal = float(user['acc_bal']) - new_bal

    # Update the user's balance in the database
    user_table.update({'acc_bal': updated_bal}, User.user_name == username)

    # Fetch the updated user info to display the new balance
    user = user_table.get(User.user_name == username)

def deduct_card(card_no,amount):
    card = card_table.get(Card.card_no == card_no)
    card_bal = float(card['c_bal'])
    amount = float(amount)
    new_bal = card_bal-amount
    card_table.update({'c_bal':new_bal},Card.card_no == card_no)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        if user_table.search(User.user_name == user_name) and user_table.search(User.password == password):
            user = user_table.get(User.user_name == user_name)
            print(user_name + " Logged In")
            return render_template('profile.html', user=user)  
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        full_name = request.form['full_name']
        password = request.form['password']
        user_ph_no = request.form['user_ph_no']
        user_email = request.form['user_email']
        user_acc_no = gen_acc_no()
        if user_table.search(User.acc_no == user_acc_no):
            user_acc_no = gen_acc_no()
        add_user(full_name, user_name, password, user_ph_no, user_email, user_acc_no, 'RI00001', 0)
        print(full_name + " Created A Account")
        return render_template('new_acc_success.html')
    return render_template('signup.html')

@app.route('/deposit_page', methods=['GET','POST'])
def deposit_page():
    if request.method == 'POST':
        amount = request.form['amount']
        method = request.form['method']
        user_name = request.form['user_name']
        user = user_table.get(User.user_name == user_name)
        if method == 'dark_card':
            return render_template('card_pay.html',amount = amount,method = method,user_name = user_name)
    return render_template('deposit_page.html', user=user)

@app.route('/card_pay',methods = ['POST','GET'])
def card_pay():
    if request.method == 'POST':
        user_name = request.form['user_name']
        name = request.form['name']
        card_num = request.form['c_no']
        expiry = request.form['expiry']
        card_cvv = request.form['cvv']
        amount = request.form['amount']
        c_type = request.form['c_type']
        deduct_card(card_num,amount)
        add_money(user_name,amount)
        return render_template('tran_success.html',user_name = user_name)
        if card_table.search(Card.card_no==card_num):
            m_card =  card_table.get(Card.card_no==card_num)
            if m_card['name'] == name and m_card['expiry'] == expiry and m_card['card_cvv'] == card_cvv :
                print(m_card['name'])
                if float(amount)>float(m_card['c_bal']):
                     return jsonify({"message":"Payment Declined By Bank. ! Reason: Insufficient Balance....."})
                else:
                    deduct_card(card_num,amount)
                    add_money(user_name,amount)
                    return render_template('tran_success.html',user_name = user_name)
        else:
            return jsonify({"message": "Invalid Card Details! Please Enter Valid Card Details."}), 200
        
@app.route('/tran_success',methods = ['POST','GET'])
def tran_success():
    if request.method == 'POST':
        user_name = request.form['user_name']
        print(user_name)
        user = user_table.get(User.user_name == user_name)
        return render_template('profile.html',user = user)

@app.route('/profile', methods = ['POST','GET'])
def profile():
    if request.method == 'POST':
        user_name = request.form['user_name']
        work = request.form['work']
        print(user_name)
        user = user_table.get(User.user_name == user_name)
        if work == 'deposit':
            return render_template('deposit_page.html',user = user)
        elif work == 'transfer':
            return render_template('transfer_page.html',user = user)

@app.route('/add_money/<username>', methods=['POST'])
def add_money_route(username):
    amount = float(request.form['amount'])
    user = user_table.get(User.user_name == username)
    updated_bal = float(user['acc_bal']) + amount
    user_table.update({'acc_bal': updated_bal}, User.user_name == username)
    return render_template('deposit_page.html', user=user)

@app.route('/transfer',methods = ['POST'])
def transfer():
    if request.method == 'POST':
        user1_name = request.form['user_name']
        new_acc_no = request.form['acc_no']
        user2_name = request.form['user2_name']
        t_amount = request.form['amount']
        user1 = user_table.get(User.user_name == user1_name)
        user2 = user_table.get(User.user_name==user2_name)
        user2_acc_no = user2['acc_no']
        if float(user1['acc_bal'])<float(t_amount):
            return jsonify({"Transaction Failed": "Your Acc Balanace Is Low."}),200
        else:
            deduct_money(user1_name,t_amount)
            add_money(user2_name,t_amount)
            return render_template('tran_success.html',user_name = user1_name)

if __name__ == '__main__':
    app.run(debug=True, port=5004)
