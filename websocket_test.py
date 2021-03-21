# websocket_test.py - gets input from the keyboard and sends it to the plotter
# SLW 03/21

import time
import websocket

#------------------------------------------
def send_msg(msg):
    """ Sends a message to websocket server.
        Returns the response """
    try:
        ws.send(msg)
        result = ws.recv()
    except OSError as err:
        print(err)
        result = ""
    return result

#------------------------------------------
ws = websocket.WebSocket()
ip = "192.168.1.70:90"
try:
    ws.connect("ws://" + ip, timeout=3)
    print("Connected to WebSocket server, IP", ip)
    connection = True
except OSError as err:
    connection = False
    print(err)

if connection:
    while True:
        instr = input("> ")
        if len(instr) == 0:
            break
        print(send_msg(instr))
    ws.close()
    print("Connection closed")
