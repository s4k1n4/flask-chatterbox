from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# It's a good practice to set a secret key for Flask sessions
app.config['SECRET_KEY'] = 'a_very_secret_key'
socketio = SocketIO(app)
users = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    users[request.sid] = "Anonymous"
    emit('user_list', list(users.values()), broadcast=True)
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]
        emit('user_list', list(users.values()), broadcast=True)
        print(f"Client disconnected: {request.sid}")

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)