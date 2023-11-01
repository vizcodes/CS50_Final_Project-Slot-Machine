# CS50 Final Project-Slot Royale 🎰
### Video Demo: [App Demo](https://youtu.be/C4Rz36tr4Q0?si=C_xCeVa8s86wsMSu)

### Description:

- Do you love playing slot machines? Do you want to experience the thrill of winning big without risking real money? If yes, then Slot Royale is the perfect game for you!

- Slot Royale is a web-based slot machine simulator that lets you enjoy the fun and excitement of a virtual slot machine game with virtual cash. You can choose how much to bet, spin the reels, and see if you get lucky. The game also has a jackpot prize that is randomly awarded when you get three same emojis on the payline.

![image](https://i.ibb.co/Hp00g8F/image.png)

- Slot Royale is written in HTML, CSS, JS, Python & SQL and uses the Flask library as the backend. The game is inspired by the classic slot machines found in casinos and arcades, with colorful graphics and realistic sound effects.

- The game uses javascript to make the website dynamic and interactive. It also plays sound effects when you spin the reels, win or lose cash, or hit the jackpot. The game also validates your input and prevents you from betting more than you have or less than the minimum amount.

- The game also has a special admin login feature that allows admins to view the dashboard and monitor the monetary performance of slot machines. The dashboard shows the total number of spins, wins, losses, and jackpots for each slot machine, as well as the average payout ratio and profit margin. The dashboard also allows admins to reset the data or change the settings of each slot machine.

![image](https://i.ibb.co/qxC28gc/image.png)

- The graphs in the dashboard are plotted using pandas and plotly, where the data is extracted from the SQLITE3 database and read as a dataframe before feeding the spin records in the plotly graph. Once the graph is plotted, it is saved to a html page and the html page gets extended into the `dashboard.html` page usinh JINJA.

### How to play?

-vIn order to play Slot Royale, you need to register an account with your username and password. You will start with a balance of 0 virtual cash. You can then add money to your account by using the add money tab. once you enter the amount you will be asked to solve an equation which, if solved successfully the cash will be added to your account. Each slot reel has different symbols and payouts. You can also see the jackpot amount for each patten on the below the slot machine.

- To place a bet, you need to enter an amount between 5 and 50 in the input slider below the slot reel. Then, you can click on the spin button to start spinning the reels. You will hear a sound effect when the reels stop. If you get a winning combination on the payline, you will see a message showing how much you won and your balance will increase accordingly. If you get three same emojis on the payline, you will win the jackpot prize. If you lose, your balance will decrease by the amount of your bet.

- You can play as many times as you want until you run out of cash or decide to quit. Your balance and spin records will be saved in the database for each session.


Slot Royale is a fun and addictive game that will keep you entertained for hours. Try it out and see if you can hit the jackpot! 🎰

Cheers,

Vizcodes
