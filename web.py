import sqlite3,time,shutil,os
from flask import Flask, render_template, request
app = Flask(__name__,static_folder='imgs/')
def check():
    try:
        os.mkdir("imgs")
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

@app.route('/operations/',methods=["POST","GET"])
def operations():
    if request.method == "POST":
        try:
            shutil.rmtree("imgs")
            os.remove("entry.db")
        except OSError as e:
            message = e
        else:
            message = "成功刪除"
        print(message)
        return f'<script>alert("{message}")</script><meta http-equiv="refresh" content="0; url="../../operations">'
    if request.method == "GET":
        return render_template('operations.html')
    else:
        return "Error"

@app.route('/entryLogs/')
def entryLogs():
    countPayload = "";error = "";logs = []
    check()
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
        error = "Cannot find Sqlite DB or No DATA"
        print(error)
    return render_template('entryLogs.html', logs=logs, countPayload = countPayload, error=error)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=30010, debug=True)
