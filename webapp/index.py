from flask import Flask, request, render_template, redirect
import pymysql
from module import dbModule
from bluetooth import *
import time
from flask import flash


app = Flask(__name__)
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e' #CSRF 방지용 문자열 


@app.route('/')
def index():
    db_class = dbModule.Database()
    sql = "SELECT * FROM product ORDER BY id"
    result = db_class.executeAll(sql)
    db_class.close()
    
    return render_template('html_main.html', result = result)
    

@app.route('/bring/<int:id>')
def bring(id):
    return render_template('html_bring.html', id = id)


@app.route('/bring/<int:id>/activate')
def bring_activate(id):
    
    # DB에 저장된 위치 정보 가져오기
    id = str(id)
    db_class = dbModule.Database()
    sql = "SELECT location FROM product WHERE id =" + id
    loc = db_class.executeAll(sql)
    loc = ''.join(loc[0])
    msg = loc + "d"
    
    # 아두이노로 위치 정보전송
    client_socket=BluetoothSocket(RFCOMM)
    client_socket.connect(("98:D3:A1:FD:34:A2", 1))
    client_socket.send(msg)
    
    # 아두이노에서 완료 신호 받기
    while True:
        msg = client_socket.recv(1024).decode()
        print("recived message : {}".format(msg))
        if msg is not None:
            break
        
    client_socket.close()   
               
    # 5초동안 기다림
    #sec = 30
    #while (sec != 0 ):
    #    sec = sec-1
    #    time.sleep(1)
       
    # DB update
    sql = "UPDATE product SET exist = 'X', note = NULL, name = NULL WHERE id =" + id
    db_class.execute(sql)
    db_class.close()

    flash("로봇의 작업이 완료되었습니다!")
    return redirect('/')


@app.route('/inputForm/<int:id>',methods=['GET'])
def inputForm(id):
    id = str(id)
    db_class = dbModule.Database()
    sql = "SELECT location FROM product where id =" + id
    result = db_class.executeAll(sql)
    db_class.close()
    
    return render_template('html_input.html', loc=''.join(result[0]))


@app.route('/put', methods=["GET", "POST"])
def put():
    
    if request.method == 'GET':
        return render_template("html_input.html")
    else:
        name = request.form.get('Name')
        note = request.form.get('Note')
        loc = request.form.get('Loc')
        
        return render_template('html_put.html', name = name, note = note, loc = loc)


@app.route('/put/activate', methods=['POST'])
def put_activate():
        
        name = request.form.get('Name')
        note = request.form.get('Note')
        loc = request.form.get('Loc')
        
        msg = loc + "u"
        
        # 아두이노로 위치 정보전송
        client_socket=BluetoothSocket(RFCOMM)
        client_socket.connect(("98:D3:A1:FD:34:A2", 1))
        client_socket.send(msg)
        
        # 아두이노에서 완료 신호 받기
        while True:
            msg = client_socket.recv(1024).decode()
            print("recived message : {}".format(msg))
            if msg is not None:
                break
        
        #client_socket.close()
        
        # 5초동안 기다림
        #sec = 5
        #while (sec != 0 ):
        #    sec = sec-1
        #    time.sleep(1)
            
        db_class = dbModule.Database()
        sql = "UPDATE product SET exist = 'O', note = '"+ note +"', name = '"+ name +"' WHERE location = '" + loc +"'"
        db_class.execute(sql)
        db_class.close()
        
        flash("로봇의 작업이 완료되었습니다!")
        return redirect('/')


if __name__=='__main__':
    app.run(debug=True, port=80, host='0.0.0.0')