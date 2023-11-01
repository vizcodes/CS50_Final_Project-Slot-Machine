
import random
import time
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required,spin,calculate_win_amt
import plotly.express as px
import pandas as pd
import numpy as np





app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///slot_machine.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/", methods =['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        user_data = db.execute("SELECT * FROM users where user_id =  ?",session['user_id'])
        if user_data[0]['user_name'] == 'admin':
            return redirect('/dashboard')
        cash = user_data[0]['cash']
        fin_lst = ['❓','❓','❓']
        return render_template('index.html',cash = round(cash,2),fin_lst = fin_lst, win_amt = 0)
    elif request.method == "POST":
        time.sleep(1)
        user_data = db.execute("SELECT * FROM users where user_id =  ?",session['user_id'])
        cash = user_data[0]['cash']
        casino_cash = db.execute("SELECT cash FROM users where user_name = 'admin';")[0]['cash']
        if cash <= 0:
            fin_lst = ['❓','❓','❓']
            return render_template('index.html',cash = round(cash,2),fin_lst = fin_lst, win_amt=0,message = 'No cash left!')
        else:
            fin_lst = spin()
            cash = cash - 1
            bet_amt = float(request.form.get('bet_amt'))
            win_amt = calculate_win_amt(fin_lst,bet_amt)
            tot_cash = cash + win_amt
            casino_cash += (-win_amt + 1)
            user_name = user_data[0]['user_name']
            db.execute("UPDATE users SET cash = ? WHERE user_id = ?",tot_cash,session['user_id'])
            db.execute("UPDATE users SET cash = ? WHERE user_name = 'admin'; ",casino_cash)
            db.execute("INSERT INTO bets (user_name,bet_amt,seq,win_amt,spin_amt) VALUES (?,?,?,?,?)",
                       user_name,bet_amt,str(fin_lst),win_amt,1)
            
            return render_template('index.html',cash = round(tot_cash,2),fin_lst = fin_lst, win_amt=round(win_amt,2))





@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html",top = "user name cannot be empty")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html",top = "password cannot be empty")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html",top = "invalid username/password")

        # Remember which user has logged in
        if rows[0]['user_name'] == 'admin':
            return render_template("login.html",top = "Admins cannot play!")                     

        session["user_id"] = rows[0]["user_id"]
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        #user name check
        user_dict = db.execute('SELECT user_name from users;')
        user_lst = list()
        for dct in user_dict:
            user_lst.append(dct.get('user_name'))

        if (username == ''):
            return render_template('register.html',top = 'Username cannot be empty!')

        elif (username in user_lst):
            return render_template('register.html',top = 'Username already exists!')

        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        #password check
        if (password == ''):
            return render_template('register.html',top = 'Password cannot be empty!')
        elif password != confirmation:
            return render_template('register.html',top = 'Confirm password doesnt match with password!')

        hash_password = generate_password_hash(password,method='pbkdf2', salt_length=16)

        #inserting into database
        db.execute("INSERT INTO users (user_name,hash) VALUES (?,?)",username,hash_password)
        return render_template("login.html",message = 'Registeration Successfull, Please login!')

    else:
        return render_template("register.html")


@app.route("/money", methods=["GET"])
def money():
    return render_template("money.html")


@app.route("/money_confirm", methods=["GET","POST"])
def money_confirm():
    if request.method =="POST":
        if request.form.get('answer') == request.form.get('og_answer'):
            new_cash  = request.form.get('money')
            cash = db.execute("SELECT cash FROM users where user_id =  ?",session['user_id'])[0]['cash']   
            tot_cash = float(cash) + float(new_cash)
            db.execute("UPDATE users SET cash = ? WHERE user_id = ?",tot_cash,session['user_id'])
            time.sleep(2)
            return redirect('/')
        else:
            return render_template('money_confirm.html',
                                   equation = request.form.get('eqn'),
                                   og_answer = request.form.get('og_answer'), cash = request.form.get('money'),
                                    message = "wrong answer" )



    else:
        try:
            money = int(request.args['money'])
        except:
            return render_template("money.html",message = "Please enter a valid number!")

        first_num = random.choice(range(0,money))
        second_num = random.choice(range(0,money))
        third_num = random.choice(range(0,money))
        equation = f'({first_num} * {second_num}) + {third_num}'
        og_answer = first_num * second_num + third_num
        return render_template('money_confirm.html',equation = equation,cash = money, og_answer=og_answer)
    
@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect('/login')


@app.route('/adminlogin', methods = ['GET','POST'])
def admin_login():
    session.clear()
    if request.method == 'GET':
        return render_template('admin_login.html')
    elif request.method == "POST":
            # Ensure username was submitted
            if not request.form.get("username"):
                return render_template("login.html",top = "user name cannot be empty")
            elif not request.form.get("password"):
                return render_template("login.html",top = "password cannot be empty")
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))
            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                return render_template("login.html",top = "invalid username/password")
            # Remember which user has logged in
            if rows[0]['user_name'] == 'admin':
                session["user_id"] = rows[0]["user_id"]
                return redirect('/dashboard')
            else:
                session["user_id"] = rows[0]["user_id"]
                return redirect('/')


@app.route('/dashboard', methods = ['GET'])
def dashboard():
    customer_count = db.execute('SELECT COUNT(user_name) AS cust_count FROM users;')[0]['cust_count']
    cust_cash = db.execute('SELECT SUM(cash) AS cust_cash FROM users WHERE user_name != "admin";')[0]['cust_cash']

    casino_profit = (db.execute('SELECT sum(win_amt) AS cas_prft FROM bets WHERE win_amt < 0;')[0]['cas_prft'] 
                    + db.execute('SELECT sum(spin_amt) AS spin_prft FROM bets')[0]['spin_prft'])
    
    total_casino_cash = db.execute('SELECT cash FROM users WHERE user_name = "admin";')[0]['cash']

    rewards_given =  db.execute('SELECT sum(win_amt) AS cas_prft FROM bets WHERE win_amt > 0;')[0]['cas_prft']

    fig_lst = db.execute('SELECT id, win_amt FROM bets;')

    fig_df = pd.DataFrame({'id':[x['id'] for x in fig_lst],'win_amt':[x['win_amt'] for x in fig_lst]})
    fig_df['win_amt'] = - (fig_df['win_amt'] )
    fig_df['ind'] = np.where(fig_df['win_amt']<0,'loss','profit')
    fig_df = fig_df.tail(50)



    fig = px.bar(fig_df, x='id', y='win_amt', color = 'ind',title = 'Casino Profit over past 50 spins',
                 labels = dict(id='spin_id',win_amt = "Casino Profit ($)"),
                 color_discrete_map = {'profit':'green','loss':'red'})
    fig.write_html('templates/cash_flow.html', auto_open=True)

    return render_template('dashboard.html',customer_count = customer_count,
                           cust_cash = round(cust_cash,0),casino_profit=round(-1*casino_profit,0),
                           total_casino_cash=round(total_casino_cash,0),rewards_given= round(rewards_given,0))
            
    
