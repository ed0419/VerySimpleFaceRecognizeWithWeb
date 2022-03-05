def runcam():
    import cv2, time, sqlite3, os
    detectTime = 0 ; detectLast = 0
    clearTrig = 3 #在未輸入幾秒重置計算張數
    confirmTrig = 30 #30張圖就算成功
    start = time.time() #設置起始時間
    #判斷imgs目錄是否存在
    if not os.path.exists(os.path.join(os.getcwd(), 'imgs')):
        os.mkdir("imgs")
        print("Created imgs Folder")
    cap = cv2.VideoCapture(0)
    #判斷資料庫是否存在
    try:
        conn = sqlite3.connect('entry.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
            TIME           VARCHAR(150)    NOT NULL);''')
        print ("Successful")
        conn.commit()
    except:
        print("Cannot Conect To Sqlite3 DB")
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faceCascade = cv2.CascadeClassifier('face_detect.xml')
            faceRect = faceCascade.detectMultiScale(gray, 1.5, 3)
            for (x, y, w, h) in faceRect:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('video', frame)
            detectTime += len(faceRect)
            if detectTime > detectLast:
                detectLast = detectTime
        else:
            break
        print(detectTime)
        #確定有達到一定的辨識次數
        if detectTime > confirmTrig:
            print("座標: ",faceRect)
            nowTime = round(float(time.time()),4)
            cv2.imwrite(f"imgs/{str(nowTime)}.png", frame)
            c.execute(f"INSERT INTO logs (time) VALUES ({str(nowTime)})")
            conn.commit()
            detectTime = 0
            print("Got Your Face")
            start = time.time()
        #輸入超時判斷&是否有持續輸入
        if time.time()-start > clearTrig and detectTime!=detectLast:
            print(time.time()-start)
            detectTime = 0
            start = time.time()
            print("TIME OUT")
        if cv2.waitKey(10) == ord('q'):
            break
    # 釋放攝影機
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()

    conn.close()

if __name__ == "__main__":
    runcam()