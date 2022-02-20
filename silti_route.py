# SocketIO - 채팅기능
from flask_socketio import SocketIO
from flask import Flask, jsonify, render_template, request, url_for, redirect

app = Flask(__name__)
app.config['SECRET KEY']='silti'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)



if __name__ == '__main__':
    socketio.run(app, host="192.168.0.132", debug=True, port=9999)
