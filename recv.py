from socket import *
import os
from threading import Thread

mainpath = os.getcwd()  # 获取当前路径


def mkdir(path):  # 建立路径
    path = path.strip()  # 去除首位空格
    path = path.rstrip("\\")  # 去除尾部 \ 符号
    isExists = os.path.exists(path)
    if not isExists:  # 不存在时创建路径
        os.makedirs(path)  # 穿件文件夹


class FileTransferHandler(Thread):

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        client, addr = self.server.accept()
        print(str(addr) + '连接到了服务器.')
        print('开始传输')
        filename = client.recv(1024).decode()
        client.send('ok'.encode())
        path = mainpath+'\\'+'temp'+'\\'+filename
        mkdir(path)
        filenames = client.recv(1024)
        allname = filenames.decode()
        testname = allname.split('/')
        name_list = []
        name_list = testname
        print(name_list)
        for name in name_list:
            f = open(path, 'wb')
            f.close()
            while True:
                with open(path, 'ab') as f:
                    data = client.recv(1024)
                    if data == b'quit':
                        client.send(b'ok')
                        break
                    f.write(data)
                    client.send(b'success')
        print('传输完成')
        os.system('attrib +s '+mainpath+'\\'+filename)  # 刷新是该文件生效
        client.close()


def recv_file():
    server = socket(family=AF_INET, type=SOCK_STREAM)
    hostname = gethostname()
    ip = gethostbyname(hostname)
    server.bind((ip, 8888))
    server.listen(5)
    print('服务器启动开始监听...')
    FileTransferHandler(server).start()
