from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, join_room, leave_room
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("app_key")
socketio = SocketIO(app)

open_rooms = {}

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/room/<room_id>")
def room(room_id):
    print("Room redirection successful")
    print(f"Session id: {open_rooms[str(room_id)]['session id']}")
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@socketio.on("connect")
def connect():
    print("A user has connected")
    socketio.emit("connect user", to=request.sid)

@socketio.on("disconnect")
def disconnect():
    print("A user has disconnected")
    print(f"sid of user disconnecting: {request.sid}")
    socketio.emit("disconnect user", {"sid": request.sid}, to=request.sid)

@socketio.on("leave room")
def on_leave(data):
    print(f"A user left room {data[0]}")
    print(open_rooms)
    open_rooms[data[0]]["users online"].remove(data[1])
    socketio.emit("leave message", to=open_rooms[str(data[0])]["session id"], include_self=False)
    leave_room(open_rooms[str(data[0])]["session id"])

@socketio.on("make room")
def make_room():
    new_room_id = str(uuid.uuid4())
    print("A room has been made!!")
    print(open_rooms)
    open_rooms[new_room_id] = {}
    open_rooms[new_room_id]["session id"] = request.sid
    open_rooms[new_room_id]["users online"] = []
    print(f"Open rooms: {open_rooms}")

    socketio.emit("redirect", {"url": url_for("room", room_id = new_room_id), "room_id": new_room_id})

@socketio.on("join room")
def on_join(room_id):
    print(f"A user joined room {room_id}")
    join_room(open_rooms[str(room_id)]["session id"])
    open_rooms[room_id]["users online"].append(request.sid)
    print(open_rooms)
    socketio.emit("join message", to=open_rooms[str(room_id)]["session id"], include_self=False)


# @socketio.on("system message")
# def handle_system_message(client_room_id, msg)

@socketio.on("chat message")
def handle_message(client_room_id, username, msg):
    print(f"Received message '{msg}' sent by '{username}' in url '{client_room_id}'")
    print(f"Corresponding session ID: {open_rooms[client_room_id]['session id']}")
    print(f"Open rooms: {open_rooms}")

    join_room(open_rooms[client_room_id]["session id"])

    socketio.emit("chat message", {"username": username, "message": msg}, to=open_rooms[client_room_id]["session id"], include_self=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)



# def message_received(methods=["GET", "POST"]):
#     print("message was received!!!")

# @socketio.on("my event")
# def handle_my_custom_event(json, methods=["GET", "POST"]):
#     print("received my event: " + str(json))
#     socketio.emit("my response", json, callback=message_received)

# @socketio.on("hello")
# def handle_hello(message):
#     send(message)

# if __name__ == "__main__":
#     socketio.run(app, debug=True)

# import asyncio
# import socketio

# sio = socketio.AsyncClient()

# @sio.event
# async def connect():
#     print("Connected to server")

# @sio.event
# async def disconnect():
#     print("Disconnected from server")

# async def start_server():
#     await sio.connect("https://localhost:5000")
#     await sio.wait()

# if __name__ == "__main__":
#     asyncio.run(start_server(), debug=True)