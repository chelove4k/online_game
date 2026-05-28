from tkinter import *
from tkinter import ttk
from functools import partial
import socket
import json
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))
while True:
    try:

        def join_server(server_ip, root):
            root.destroy()
            import data.game as game
            game.run(server_ip)

        def get_servers_stats():
            # ip = socket.gethostbyname(socket.gethostname())
            ip = input('Inter IP:\n>> ')
            port = 60001


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))



            s.send(b'get_servers')
            data = s.recv(4096).decode()

            s.close()
            return json.loads(data)

        def make_GUI():

            root = Tk()

            root.title('test')
            root.geometry('400x400')



            ttk.Label(text='Choose server:\n').pack(anchor='nw')
            frame = ttk.Frame()
            server_list = get_servers_stats()


            for i in server_list:
                i = (i, server_list[i])

                Button(frame, text = f'join : "{i[0]}"', command=partial(join_server, i[1], root)).pack(anchor='nw')
            frame.pack(anchor='nw')


            def update(frame):
                server_list = get_servers_stats()
                frame.destroy()
                frame = ttk.Frame()
                for i in server_list:
                    i = (i, server_list[i])

                    Button(frame, text = f'join : "{i[0]}"', command=partial(join_server, i[1], root)).pack(anchor='nw')

                frame.pack(anchor='nw')
                frame.after(1000, partial(update, frame))
                
                
            frame.after(1000, partial(update, frame))

            root.mainloop()

        def run():
            make_GUI()

        run()
    except Exception as e:
        print(e)