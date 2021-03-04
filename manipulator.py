#!/usr/bin/python3

import socket
import signal
import logging
#---------------------------------------------
from get_config import get_config
params = get_config();
#---------------------------------------------  
internal_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP);
internal_sock_port = int(params['MANIPULATOR_PORT']);
internal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
internal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1);
internal_socket.setblocking(False);
internal_socket.settimeout(None);
internal_socket.bind(('',int(internal_sock_port)));
internal_socket.listen(5);
#---------------------------------------------  
logging.basicConfig(filename='manipulator.log', level=logging.INFO);
logging.info('manipulator started!');
def normal_exit(signal_num, frame):
    internal_socket.close();
    logging.info('manipulator stopped!');
    exit(0);
signal.signal(signal.SIGINT,normal_exit);
while True:
    conn, addr = internal_socket.accept();
    packet = conn.recv(1024);
    if packet:
        packet = packet.decode().rstrip();
        print(packet);
        logging.info(packet);

        
    
        
