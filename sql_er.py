import sqlite3

conn = sqlite3.connect('slot_machine.db')

c = conn.cursor()


#sql tab
c.execute('''
          
          CREATE TABLE IF NOT EXISTS users
          ([user_id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, [user_name] TEXT NOT NULL,
          [hash] TEXT NOT NULL, [cash] NUMERIC NOT NULL DEFAULT 0);

          ''')

c.execute('''
          
          CREATE TABLE IF NOT EXISTS bets
          ([id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, [user_name] TEXT NOT NULL,
          [bet_amt] NUMERIC NOT NULL,
          [seq] TEXT NOT NULL,
          [win_amt] NUMERIC NOT NULL,
          [spin_amt] NUMERIC NOT NULL DEFAULT 1);

          ''')


           
conn.commit()
conn.close()

