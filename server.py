import socket
import threading
import json
from game import Game
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "DISCONNECT"

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
except socket.error as e:
    print(str(e))

game = Game()

#Function starting on new thread to handle input/output data to user
def handle_client(conn, player):
    print(f"[NEW CONNECTION]")
    conn.send(str.encode(str(player)))
    game.player_connected(player)
    connected = True
    while connected:   
        try:
            #decode receieved data and convert it to json object
            data = json.loads(conn.recv(4096).decode())
            if not data:
                break
            else:
                if data["request"] == DISCONNECT_MSG:
                    game.player_disconnected(player)
                    game.ready = False
                    break
                elif data["request"] == "update":    
                    game.update_player_pos(player, data["data"]) 
                    game.update_block(data["block"])
                    game.blueKeyTaken = data["keys"][0]
                    game.redKeyTaken = data["keys"][1]
                    game.doors = data["doors"]
                reply = {
                    "player1" : game.get_player_pos(0), 
                    "player2" : game.get_player_pos(1),
                    "block" : game.blockPos,
                    "p1ready" : game.p1ready,
                    "p2ready" : game.p2ready,
                    "state" : game.ready,
                    "keys" : [game.blueKeyTaken, game.redKeyTaken],
                    "doors" : game.doors
                }
                #Converting the json to string and encode it before sending over to client
                conn.sendall(str.encode(json.dumps(reply)))
        except:
            break
    
    print("LOST CONN")
    conn.close()

#Main loop to search for new connections
def start():
    current_player = 0
    server.listen()
    print(f"[LISTNING] Server is listening on {SERVER }")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, current_player))
        thread.start()
        print(f"[ACTIVE CONECTIONS] {threading.activeCount() - 1}")
        current_player += 1

print("[STARTING] server is starting...")
start()