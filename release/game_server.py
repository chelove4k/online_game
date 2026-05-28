import socket
import json
import os
import random


os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = socket.gethostbyname(socket.gethostname())
print(ip)
port = 60002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(10)

players = {}
users = []
conn_list = []

max_players = int(input('max players:\n>>> '))

mode = 2
while True:
    try:
# Стадия принятия
        if mode == 0:
            conn_, add = s.accept()
            print(f'connected by {add}')
            conn_list.append(conn_)
            print(conn_list)
            if len(conn_list) == max_players:
                mode = 1
                print('START')
                for conn in conn_list:
                    # trash [[x, y], [x, y]]
                    trash = []
                    for i in range(100):
                        trash.append([random.randint(40, 790), random.randint(40, 790)])
                    
                    trash = json.dumps(trash)
                    conn.send(trash.encode())
# ============
# Пошло поехало
        if mode == 1:
            for conn in conn_list:
                data = json.loads(conn.recv(1024).decode())
                if data['name'] not in users:
                    users.append(data['name'])
                    players.update(
                        {
                            data['name']: 
                                {
                                'cord' : [data['x'], data['y']],
                                'stats': [data['m'], data['color']]
                                }
                        })
                else:
                    players[data['name']] = {
                                'cord' : [data['x'], data['y']],
                                'stats': [data['m'], data['color']]
                                }
                # print(json.dumps(players).encode())
                print(players)
                data = json.dumps(players).encode()
                conn.send(data)
# ============
        if mode == 2:
            # ======================================================
            name = input("server name:\n>>> ")
            server_name = f'server: {name}'
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.connect((ip, 60001))
            data = {server_name: ip}
            data = json.dumps(data)
            s1.send(b'new_server')
            s1.recv(1024)
            s1.send(data.encode())
            s1.close()
            mode = 0
            # =======================================================
    except Exception:
# Обнуление в случае лива
        conn_list = []
        mode = 2
        players = {}
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((ip, 60001))
        s1.send(b'close_server')
        print('close')
        s1.recv(1024)
        s1.send(server_name.encode())
        s1.close()
        
# =================================      
        
        for conn in conn_list:
            conn.recv(1024)
            conn.send(b'close')

        exit('Finish')
# ============