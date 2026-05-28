import socket
import json
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = socket.gethostbyname(socket.gethostname())
print(ip)
port = 60001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(10)


while True:
    conn, add = s.accept()
    print(f'connected by {add}')
    
    command = conn.recv(1024).decode()
    print(command)
    
    if command == 'get_servers':
        conn.sendfile(open('data\\servers.json', 'rb'))
        conn.close()
        
    if command == 'new_server':
        conn.send(b'1')
        server_data = conn.recv(1024).decode()
        
        data = json.load(open('data\\servers.json'))
        
        data.update(json.loads(server_data))
        print(data)
        
        json.dump(data, open('data\\servers.json', 'w'))
        conn.close()
        
    if command == 'close_server':
        conn.send(b'1')
        server_name = conn.recv(1024).decode()
        
        data = json.load(open('data\\servers.json'))
        
        data.pop(server_name)

        json.dump(data, open('data\\servers.json', 'w'))
        conn.close()