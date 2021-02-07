from socket import *
from base64 import b64encode
import os


def send_file(dir, filename):
    client = socket()
    hostname = gethostname()
    ip = gethostbyname(hostname)
    client.connect((ip, 8888))
    client.send(filename.encode())
    flag = client.recv(1024)
    if flag == b'ok':
        pass
    filenames = os.listdir(dir)
    new_filename = '/'.join(filenames)
    client.send(new_filename.encode())
    for name in filenames:
        with open(dir+'\\'+name, 'rb') as f:
            for i in f:
                client.send(i)
                data = client.recv(1024)
                if data != b'success':
                    break
        client.send(b'quit')
        f.close()
        flag = client.recv(1024)
        if flag == b'ok':
            continue
    client.close()
