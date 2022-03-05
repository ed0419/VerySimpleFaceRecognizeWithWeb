from flask import Flask, render_template
import sqlite3,time

app = Flask(__name__,static_folder='imgs/')

try:
    conn = sqlite3.connect('entry.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
        (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        TIME           TEXT    NOT NULL);''')
    print ("Successful")
    conn.commit()
    conn.close()
except:
    print("Cannot Conect To Sqlite3 DB")

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/entryLogs/')
def entryLogs():
    countPayload = "";error = "";logs = []
    try:
        conn = sqlite3.connect('entry.db')
        c = conn.cursor()
        cursor = c.execute("SELECT time from logs")
        for i in cursor:
            res = time.localtime(float(i[0]))
            payload = f'人員於 {res.tm_year} 年 {res.tm_mon} 月 {res.tm_mday} 日 {res.tm_hour} 時 {res.tm_min} 分 {res.tm_sec} 秒 進入區域'
            imgpayload = f'<center><img src="../imgs/{str(i[0])}.png" width=50% height=50%/></center>'
            logs.append(payload + imgpayload)
            countPayload = f"<h1>共 {len(logs)} 次進入</h1>"
            print(i[0])
        conn.close()
        if len(logs) == 0:
            error = f'<font size=5 color="red">目前沒有資料</font><br><p>現在時間 : {time.ctime()}</p>'
    except:
        error = "Cannot find Sqlite DB"
        print(error)
    return render_template('entryLogs.html', logs=logs, countPayload = countPayload, error=error)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=30010, debug=True)