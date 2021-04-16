# my_bursa
Prerequisites
-------------
1. Anaconda (https://www.anaconda.com)
   Intalls Python plus modules such as Pandas, NumPy, MatPlotLib, and more.
2. sqlite3 (https://www.sqlite.org/index.html)
   For storing trading and analysis.
3. telegram-send (https://pypi.org/project/telegram-send/)
   For broadcasting messages to Telegram channel using bot
   Configure after install using below command, and follow the instructions
   telegram-send --config OSTrade.conf --configure-channel
4. streamlit (https://streamlit.io/)
   Turns data scripts into shareable web apps in minutes.

Configure Database
------------------
1. Create database

Configure Telegram
------------------
https://bogomolov.tech/Telegram-notification-on-SSH-login/
1. Create Telegram bot
   a. Search @BotFather
   b. Type /start
2. Create channel (not group)
3. Add bot to the channel as admin
4. Add contacts to the channel either as admin or subscribers

Configure Python Schedules
--------------------------
1. Check variables in schedule.bat, and verify/modify the values:
   - PYTHON_EXE: path to python.exe
   - WORK_DIR: This directory
   - PYTHONPATH: must include path to libs folder
2. Configure task scheduler (in Windows) or (untested) crontab (in Linux)
   For Windows, you may refer to task_scheduler.xml

Sample queries in database
--------------------------
select count(*) from (select Symbol, Date from staging except select Symbol, Date from stock_prices);

insert into stock_prices select Date, Open, High, Low, Close, Volume, Symbol from staging where Date > (select max(Date) from stock_prices);

select Date, Open, High, Low, Close, Volume, Symbol from staging except select Date, Open, High, Low, Close, Volume, Symbol from stock_prices;

select symbol, count(*) from (select Date, Open, High, Low, Close, Volume, Symbol from staging except select Date, Open, High, Low, Close, Volume, Symbol from stock_prices);

SELECT Date, Close FROM stock_prices WHERE Symbol='TEXCYCL' AND Date >= date('now', '-9 month');