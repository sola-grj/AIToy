from flask import Flask,request,json
import geventwebsocket
from geventwebsocket.server import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket

ws_app = Flask(__name__,)


socket_dict = {}

@ws_app.route("/toy/<toy_id>")
def web_ws(toy_id):
    user_socket = request.environ.get("wsgi.websocket") # type:WebSocket
    if user_socket:
        socket_dict[toy_id] = user_socket
    print(len(socket_dict),socket_dict)
    while 1:
        try:
            user_msg = user_socket.receive()
            print("user_socket",user_socket)
            user_msg_dict = json.loads(user_msg)
            print("user_msg_dict",user_msg_dict)
            receiver_id = user_msg_dict.get("to_user")
            receiver_socket = socket_dict.get(receiver_id)
            receiver_socket.send(user_msg)
        except geventwebsocket.exceptions.WebSocketError:
            pass



@ws_app.route("/app/<app_id>")
def app_ws(app_id):
    user_socket = request.environ.get("wsgi.websocket") # type:WebSocket
    if user_socket:
        socket_dict[app_id] = user_socket
    print(len(socket_dict),socket_dict)
    while 1:
        try:
            user_msg = user_socket.receive()
            print(user_msg)
            user_msg_dict = json.loads(user_msg)
            receiver_id = user_msg_dict.get("to_user")
            receiver_socket = socket_dict.get(receiver_id)
            receiver_socket.send(user_msg)
        except geventwebsocket.exceptions.WebSocketError:
            pass


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0",9528),ws_app,handler_class=WebSocketHandler)
    http_server.serve_forever()