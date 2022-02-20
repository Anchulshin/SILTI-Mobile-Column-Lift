# SocketIO - 채팅기능
from flask_socketio import SocketIO
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET KEY']='silti'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')




if __name__ == '__main__':
    socketio.run(app, host="192.168.0.6", debug=True, port=9999)
