from tinydb import TinyDB,Query
from tinydb.operations import add
from flask import Flask,render_template
import random
import os


banking = Flask(__name__)

def gen_acc_no():
    return random.randint(541111111111, 991111111111)

user_db = TinyDB('user_db.json')

user_table = user_db.table('Users')
User = Query()




def add_user(full_name,user_name,password,user_ph_no,email,acc_no,ifsc_code,acc_bal):
    user_table.insert({'full_name': full_name,'user_name':user_name,'password':password,'User_ph_no': user_ph_no,'User_email':email,'acc_no':acc_no,'ifsc_code': ifsc_code,'acc_bal':acc_bal})

def user_login_db(user):
    os.system('cls')
    print(f"Hey,{user['full_name']} Welcome To Bank Of RI.\nYour Profile : ")
    print(f"Name = {user['full_name']}\n Acc no = {user['acc_no']}\nIFSC CODE = {user['ifsc_code']} \nAccount Balance : {user['acc_bal']}")
    print("\n\nMenu : \n1. Add Money \n2. Withdraw Money\n3.Transaction history")
    opt_t = input("Enter Prefered Option")
    if opt_t == '1':
        add_money(user)
    elif opt_t == '2':
        withdraw_money(user)
    elif opt_t == '3':
        print("Your Transaction History:\n\n")
        opt_t2 = input("Enter 0 To Go To Main Menu : ")
        if opt_t2 == '0':
            main()
        else:
            print("Invalid Input! Please Press 0 To Go Back To HomePage : ")
    else:
        main()

def add_money(user):
    new_bal = float(input("Enter Amount You Want To Add : "))
    username = user['user_name']
    updated_bal = float(user['acc_bal']) + new_bal

    # Update the user's balance in the database
    user_table.update({'acc_bal': updated_bal}, User.user_name == username)

    # Fetch the updated user info to display the new balance
    user = user_table.get(User.user_name == username)

    print("Transaction Successfully Completed.")
    print(f"Your New Balance Is : {user['acc_bal']}")

def withdraw_money(user):
    wit_bal = float(input("Enter Amount You Want To Withdraw : "))
    username = user['user_name']
    updated_bal = float(user['acc_bal']) - wit_bal

    # Update the user's balance in the database
    user_table.update({'acc_bal': updated_bal}, User.user_name == username)

    # Fetch the updated user info to display the new balance
    user = user_table.get(User.user_name == username)

    print("Transaction Successfully Completed.")
    print(f"Your New Balance Is : {user['acc_bal']}")

def user_login():
    os.system('cls')
    user_name = input("Enter Your UserName : ")
    password = input("Enter Your password : ")
    if user_table.search(User.user_name==user_name) and user_table.search(User.password==password):
        user = user_table.get(User.user_name == user_name)
        user_login_db(user)
    else:
        print("Not login")
def user_signup():#New Bank Acc Creation.
    os.system('cls')
    user_name = input("Enter A Unique User Name : ")
    if user_table.search(User.user_name == user_name):
        print("This UserName Is Already taken.")
        user_signup()
    full_name = input("Enter Your Full Name: ")
    password = input("Enter A Strong Password")
    user_ph_no = input("Enter Your Phone Number : (+91)")
    email = input("Enter Your Email Id : ")
    user_acc_no = gen_acc_no()
    if user_table.search(User.acc_no==user_acc_no):
        user_acc_no = gen_acc_no()
    add_user(full_name,user_name,password,user_ph_no,email,user_acc_no,'RI00001',0)
    print("Your Account Has Been SuccessFully created...")
    print(f"Your Account Number Is : {user_acc_no}")
    print("Your IFSC Code Is : RI00001")
    print(f"UserName Is : {user_name}")
    print(f"Password is : {password}")
    print("Please Don't Share Your Credential With Anyone.")
    key_t = input("Press 0 To Go Back To Home Page : ")
    if key_t=='0':
        main()
    else:
        print("Invalid Input! Please Press 0 To Go Back To HomePage : ")

def main():
    os.system('cls')
    print("Welcome To Bank Of RI.")
    print("Menu : ")
    print("1.Login(If Already Have account).\n2. Create a New Account.")
    opt = int(input("Enter Prefered Option : "))
    if opt == 1:
        user_login()
    if opt == 2:
        user_signup()

if __name__=="__main__":
    main()