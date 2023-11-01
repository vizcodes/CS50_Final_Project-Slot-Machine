import random
import time
from functools import wraps
from flask import redirect, render_template, session

global rand_lst
global val_lst
rand_lst = ['🍌','🍎','🍒','💲','🔥','💀']



def spin():
        time.sleep(random.choice([2]))
        choice_lst = list()
        for i in range(0,3):
                choice_lst.append(random.choice(rand_lst))
        return choice_lst

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def calculate_win_amt(fin_lst,bet_amt):
    win_amt = 0
    if fin_lst == ['🔥','🔥','🔥']:
        win_amt = bet_amt * 50
        return win_amt
    elif fin_lst == ['💲','💲','💲']:
        win_amt = bet_amt * 10
        return win_amt
    elif fin_lst == ['🍒','🍒','🍒']:
        win_amt = bet_amt * 5
        return win_amt
    elif fin_lst == ['🍎','🍎','🍎']:
        win_amt = bet_amt * 2
        return win_amt
    else:
        win_dict = { '🍌':bet_amt/9,
                     '🍎':1,
                     '🍒':0,
                     '💲':0,
                     '🔥':0,
                     '💀':-bet_amt/3}
        for x in fin_lst:
         win_amt += win_dict[x]
        return win_amt
         
         




            
    
            
            
      
      


