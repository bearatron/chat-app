from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "wMWk0lVHK4W8t0MEgyTY"
socketio = SocketIO(app)

@app.route("/")
def sessions():
    return render_template("index.html")

@socketio.on("connect")
def connect():
    print("A user has connected")
    socketio.emit("user connected")

@socketio.on("disconnect")
def disconnect():
    print("A user has disconnected")
    socketio.emit("user disconnected")

@socketio.on("chat message")
def handle_message(username, msg):
    print(f"Received message '{msg}' sent by '{username}'")
    socketio.emit("chat message", [username, msg])

if __name__ == "__main__":
    socketio.run(app, debug=True)