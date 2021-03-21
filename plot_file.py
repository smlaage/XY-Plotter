# plot_file.py - reads an input file and sends it to the plotter
# SLW 03/21

import time
import websocket

# Global parameter ---------------------------------------
ip = "192.168.1.70:90"
filename = "plot_file"
extension = ".plt"

#---------------------------------------------------------
def send_msg(msg):
    try:
        ws.send(msg)
        result = ws.recv()
    except websocket._exceptions.WebSocketTimeoutException:
        print("timeout occured")
        result = None
    return result

#----------------------------------------------------------
def get_buffer_size():
    result = send_msg("F")
    if result:
        buffer_size = int(result.split(':')[1])
        return buffer_size
    else:
        return 0

#----------------------------------------------------------
# open communication channel
ws = websocket.WebSocket()
ws.connect("ws://" + ip, timeout=5)
print("Connected to WebSocket server on IP", ip)

# read input file
if filename.find(extension) < 0:
    filename += extension
try:
    with open(filename, "r") as f:
        lines = f.readlines()
    print(len(lines), "lines read")
except IOError:
    print("File '" + filename + "' not available or accessible")
    lines = None

# send data to plotter
if lines:
    buffer_okay = False
    for n, l in enumerate(lines):
        while True:
            buf = get_buffer_size()
            if buf > 10000:
                buffer_okay = True
            elif buf < 1000:
                buffer_okay = False
            if buffer_okay:
                send_msg(l)
            if n % 20 == 0:
                print(" - {:d} lines sent".format(n))
                break;
            else:
                time.sleep(1)

# finish plot and close connection
#send_msg("H; P")
ws.close()
print("Connection closed")
