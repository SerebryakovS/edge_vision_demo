import socket
from get_config import get_config
#---------------------------------------------
params = get_config();
internal_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP);
internal_sock_port = int(params['MANIPULATOR_PORT']);
#-------------------------------------------------    
internal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
internal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1);
internal_socket.setblocking(False);
internal_socket.settimeout(0.1);

while True:
    conn,addr = internal_socket.accept();
    packet = conn.recv(1024);
    if packet:
        print("%s"%gcntan_data.decode().replace("'","").replace("\\n","\n"));
    
        
