import socket
import json
from threading import Thread
import time


class User:

    def __init__(self, c):
        self.c = c
        self._user_name = None

    def set_name(self, name):
        self._user_name = name

    def get_info(self):
        return self._user_name


class Server:

    def __init__(self):
        self.user_list = []
        self.user_index = {}
        self.user_status = {}
        self.request_dic = {}
        self.sum = 0
        s = socket.socket()  # 创建 socket 对象
        host = socket.gethostname()  # 获取本地主机名
        port = 12345  # 设置端口
        s.bind((socket.gethostname(), port))  # 绑定端口

        s.listen(16)  # 等待客户端连接
        while True:
            c, addr = s.accept()  # 建立客户端连接
            self.user_list.append(User(c))
            t = Thread(target=self.func, args=(len(self.user_list) - 1,))
            t.start()
            time.sleep(0.5)
            t = Thread(target=self.rec, args=(len(self.user_list) - 1,))
            t.start()

    def func(self, id_):
        c = self.user_list[id_].c
        self.user_list[id_].set_name(c.recv(1024).decode("utf-8"))
        user_name = self.user_list[id_].get_info()
        self.user_status[user_name] = True
        self.user_index[user_name] = id_
        while self.user_status[self.user_list[id_].get_info()]:
            self.send_message(id_, json.dumps(self.user_status))
            time.sleep(1)

    def rec(self, id_):
        c = self.user_list[id_].c
        while True:
            try:
                info = c.recv(1024).decode('utf-8')
            except ConnectionResetError:
                user_name = self.user_list[id_].get_info()
                del self.user_list[id_]
                del self.user_index[user_name]
                id = self.request_dic[user_name]
                del self.request_dic[user_name]
                del self.request_dic[id]
                break
            except BrokenPipeError:
                user_name = self.user_list[id_].get_info()
                del self.user_list[id_]
                del self.user_index[user_name]
                id = self.request_dic[user_name]
                del self.request_dic[user_name]
                del self.request_dic[id]
                break
            print(id_, info)
            info = info.split('.')
            if info[0] == 'answer':
                if info[1] == 'accept':
                    self.user_status[self.user_list[id_].get_info()] = False
                    self.user_status[self.user_list[self.request_dic[id_]].get_info()] = False
                    print(self.user_status)
                    self.send_message(self.request_dic[id_], 'answer.accept')
                    time.sleep(1)
                    self.send_message(id_, 'round.first#')
                    print(self.user_list[id_].get_info(), 'first')
                    self.send_message(self.request_dic[id_], 'round.second#')
                    time.sleep(1)
                    print(self.user_list[self.request_dic[id_]].get_info(), 'second')
            elif info[0] == 'request':
                request_name = info[1]
                if not self.user_status[request_name]:
                    self.send_message(id_, 'answer.deny')
                else:
                    request_index = self.user_index[request_name]
                    self.request_dic[request_index] = id_
                    self.request_dic[id_] = request_index
                    self.send_message(request_index, 'request.'+self.user_list[id_].get_info())
            elif info[0] == 'position':
                print(info)
                index = self.request_dic[id_]
                self.send_message(index, 'position.'+info[1]+'#')
            else:
                print(info)

    def send_message(self, index, message):
        print('send ', index, message)
        try:
            self.user_list[index].c.send(bytes(message, 'utf-8'))
        except ConnectionResetError:
            user_name = self.user_list[index].get_info()
            print(self.user_list, self.user_status, self.user_index, self.request_dic)
            del self.user_list[index]
            del self.user_index[user_name]
            id = self.request_dic[user_name]
            del self.request_dic[user_name]
            del self.request_dic[id]
            print(self.user_list, self.user_status, self.user_index, self.request_dic)
        except BrokenPipeError:
            user_name = self.user_list[index].get_info()
            print(self.user_list, self.user_status, self.user_index, self.request_dic)
            del self.user_list[index]
            del self.user_index[user_name]
            del self.user_status[user_name]
            id = self.request_dic[user_name]
            del self.request_dic[user_name]
            del self.request_dic[id]
            print(self.user_list, self.user_status, self.user_index, self.request_dic)

server = Server()
