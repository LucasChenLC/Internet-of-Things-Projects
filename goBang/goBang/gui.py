import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from tkmacosx import Button
from board import GameBoard
from threading import Thread
from tkinter import ttk
import json
import socket
from search_engine import *

BLACK_CHESS = -1
WHITE_CHESS = 1

first_player = None
side = None
upper_chess = None

ori_board = None

mode = None
self_user_name = None

s = None


def round_label(canvas, x, y, color, text, text_color, h=30, r=10, w=None, font_size=None, tag=None):
    if w is None:
        w = len(text) * 8
    if font_size is not None:
        w *= font_size / 15
        h *= font_size / 17
    canvas.create_arc(x, y, x + 2 * r - 2, y + 2 * r - 2, start=90, extent=90, fill=color, outline=color, tags=tag)
    canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color, tags=tag)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color,
                      tags=tag)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color, tags=tag)
    canvas.create_rectangle(x + r - 1, y, x + w - r + 1, y + r, fill=color, width=0, outline=color, tags=tag)
    canvas.create_rectangle(x + w - r, y + r, x + w + 1, y + h - r + 1, fill=color, width=0, outline=color, tags=tag)
    canvas.create_rectangle(x + r, y + h - r, x + w - r + 1, y + h + 1, fill=color, width=0, outline=color, tags=tag)
    canvas.create_rectangle(x, y + r - 1, x + r, y + h - r + 1, fill=color, width=0, outline=color, tags=tag)
    canvas.create_rectangle(x + r, y + r, x + w - r, y + h - r, fill=color, width=0, outline=color, tags=tag)
    if font_size is None:
        canvas.create_text(x + w / 2, y + h / 2, text=text, fill=text_color, tags=tag)
    else:
        canvas.create_text(x + w / 2, y + h / 2, text=text, fill=text_color, font=('Arial', font_size), tags=tag)


class MainUI:

    def __init__(self):
        global ori_board, mode
        mode = None
        self.win = tk.Tk()
        self.canvas = tk.Canvas(self.win, width=1024, height=576)
        ori_board = cv2.imread('resources/pictures/UIBegin.jpeg')
        ori_board = ori_board[..., ::-1]
        ori_board = ImageTk.PhotoImage(Image.fromarray(ori_board))
        self.canvas.create_image(1024 / 2, 576 / 2, image=ori_board)
        self.canvas.create_text(250, 100, text='Gobang', font=('Arial', 70))
        round_label(self.canvas, 70, 200, 'LightCyan2', 'Play Online', 'RoyalBlue1', font_size=35, tag='button1')
        round_label(self.canvas, 70, 290, 'pale green', 'Play with AI', 'dark green', font_size=35, tag='button2')
        round_label(self.canvas, 70, 380, 'pink', 'Play with Person', 'red2', font_size=35, tag='button3')
        self.canvas.bind('<Button-1>', func=self.click)
        self.canvas.bind('<ButtonRelease-1>', func=self.released)
        self.canvas.pack()
        self.win.mainloop()

    def click(self, event):
        if 70 < event.x < 275 and 200 < event.y < 261:
            self.canvas.delete('button1')
            round_label(self.canvas, 70, 200, 'RoyalBlue1', 'Play Online', 'Black', font_size=35, tag='button1')
        elif 70 < event.x < 296 and 290 < event.y < 351:
            self.canvas.delete('button2')
            round_label(self.canvas, 70, 290, 'dark green', 'Play with AI', 'Black', font_size=35, tag='button2')
        elif 70 < event.x < 373 and 380 < event.y < 461:
            self.canvas.delete('button3')
            round_label(self.canvas, 70, 380, 'red2', 'Play with Person', 'Black', font_size=35, tag='button3')

    def released(self, event):
        global mode
        if 70 < event.x < 275 and 200 < event.y < 261:
            self.canvas.delete('button1')
            round_label(self.canvas, 70, 200, 'LightCyan2', 'Play Online', 'RoyalBlue1', font_size=35, tag='button1')
            mode = 1
            self.win.destroy()
        elif 70 < event.x < 296 and 290 < event.y < 351:
            self.canvas.delete('button2')
            round_label(self.canvas, 70, 290, 'pale green', 'Play with AI', 'dark green', font_size=35, tag='button2')
            mode = 2
            self.win.destroy()
        elif 70 < event.x < 373 and 380 < event.y < 461:
            self.canvas.delete('button3')
            round_label(self.canvas, 70, 380, 'pink', 'Play with Person', 'red2', font_size=35, tag='button3')
            mode = 3
            self.win.destroy()


class UserName:

    def __init__(self):
        global ori_board
        self.win = tk.Tk()
        self.canvas = tk.Canvas(self.win, width=1024, height=576)
        ori_board = cv2.imread('resources/pictures/UIBeginDark.jpeg')
        ori_board = ori_board[..., ::-1]
        ori_board = ImageTk.PhotoImage(Image.fromarray(ori_board))
        self.canvas.create_image(1024 / 2, 576 / 2, image=ori_board)
        str_ = '                 '
        round_label(self.canvas, 1024 / 2 - 220, 576 / 2 - 100, 'LightCyan2', str_, 'Black', h=50, font_size=50)
        self.canvas.create_text(1024 / 2 + 10, 576 / 2 - 70, text='Please enter your username', font=('Arial', 30),
                                fill='RoyalBlue1')
        self.name_set = tk.Entry(self.canvas, width=15, font=('Arial', 30))
        self.name_set.place(x=1024 / 2 - 130, y=576 / 2 - 30)
        self.canvas.pack()
        self.win.bind('<Return>', func=self.confirm)
        self.win.mainloop()

    def confirm(self, event):
        global self_user_name
        self_user_name = self.name_set.get()
        self.win.destroy()


class WaitingRoom:

    def __init__(self):
        self.s = socket.socket()
        self.s.connect(('10.26.49.167', 12345))
        self.s.send(bytes(self_user_name, 'utf-8'))
        self.previous_info = None
        self.win = tk.Tk()
        self.a = tk.Label(self.win)
        t = Thread(target=self.refresh)
        t.start()
        self.win.mainloop()

    def del_win(self):
        self.win.destroy()

    def refresh(self):
        global s
        while self.win.children:
            info = self.s.recv(1024)
            info = info.decode('utf-8')
            try:
                user_dic = json.loads(info)
                if user_dic != self.previous_info:
                    columns = ("User Name", "Available")
                    try:
                        self.treeview.destroy()
                    except AttributeError:
                        pass
                    self.treeview = ttk.Treeview(self.win, height=18, show="headings", columns=columns)  # 表格

                    self.treeview.column('User Name', width=200, anchor='center')  # 表示列,不显示
                    self.treeview.column("Available", width=100, anchor='center')

                    self.treeview.heading("User Name", text="User Name")  # 显示表头
                    self.treeview.heading("Available", text="Available")

                    self.treeview.pack(side=tk.LEFT, fill=tk.BOTH)
                    user_list = []
                    available_list = []
                    for user_name, available in user_dic.items():
                        user_list.append(user_name)
                        available_list.append(available)

                    for i in range(min(len(user_list), len(available_list))):  # 写入数据
                        self.treeview.insert('', i, values=(user_list[i], available_list[i]))

                    self.treeview.bind('<Double-1>', self.set_cell_value)  # 双击左键进入编辑
            except json.decoder.JSONDecodeError:
                print(info)
                info = info.split('.')
                if info[0] == 'request':
                    answer = messagebox.askyesno('combat request',
                                                 'Do you want to join the game with ' + info[1] + ' ?')
                    if answer:
                        self.s.send(bytes('answer.accept', 'utf-8'))
                        self.win.quit()
                        print(info)
                        s = self.s
                        return
                    else:
                        self.s.send(bytes('answer.deny', 'utf-8'))
                elif info[0] == 'answer':
                    if info[1] == 'accept':
                        for wdiget in self.win.winfo_children():
                            wdiget.destroy()
                        self.win.quit()
                        print(info)
                        s = self.s
                        return
                    else:
                        messagebox.showinfo('Request Denied', 'Your request has been denied')

            self.previous_info = user_dic

    def set_cell_value(self, event):  # 双击进入编辑状态
        for item in self.treeview.selection():
            item_text = self.treeview.item(item, "values")
            info = tuple(item_text)
            (user_name, available) = info
            if available and user_name != self_user_name:
                self.s.send(bytes('request.' + user_name, 'utf-8'))

    def wait_confirm(self, event):
        self.win.destroy()
        pass


class RoundSettings:

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Round Settings")
        self.choose_frame = tk.Frame(self.win)
        self.confirm_frame = tk.Frame(self.win, width=100)
        self.frame1 = tk.Frame(self.choose_frame)
        self.frame2 = tk.Frame(self.choose_frame)
        self.frame3 = tk.Frame(self.choose_frame)
        self.first_hint = tk.Label(self.frame1, text="Choose which side will play first")
        self.me_first = Button(self.frame1, text="Me", command=self.click_me_first)
        self.opponent_first = Button(self.frame1, text="Opponent", command=self.click_opponent_first)
        self.player_hint = tk.Label(self.frame2, text="Choose which side you will play for")
        self.for_black = Button(self.frame2, text="Black Chess", command=self.click_for_black)
        self.for_white = Button(self.frame2, text="White Chess", command=self.click_for_white)
        self.up_hint = tk.Label(self.frame3, text="Choose which side will on the upper")
        self.white_up = Button(self.frame3, text="White Chess", command=self.click_white_up)
        self.black_up = Button(self.frame3, text="Black Chess", command=self.click_black_up)
        self.confirm_button = tk.Button(self.confirm_frame, width=10, height=10, text='play',
                                        command=self.click_confirm)

    def choose(self):
        self.first_hint.pack(side=tk.TOP)
        self.me_first.pack(side=tk.LEFT)
        self.opponent_first.pack(side=tk.RIGHT)
        self.player_hint.pack(side=tk.TOP)
        self.for_black.pack(side=tk.LEFT)
        self.for_white.pack(side=tk.RIGHT)
        self.up_hint.pack(side=tk.TOP)
        self.white_up.pack(side=tk.LEFT)
        self.black_up.pack(side=tk.RIGHT)
        self.confirm_button.pack()
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.choose_frame.pack(side=tk.LEFT)
        self.confirm_frame.pack(side=tk.RIGHT)
        self.win.mainloop()

    def click_me_first(self):
        global first_player
        first_player = 'me'
        self.me_first.configure(fg='white', bg='deepskyblue')
        self.opponent_first.configure(fg='black', bg='white')

    def click_opponent_first(self):
        global first_player
        first_player = 'opponent'
        self.opponent_first.configure(fg='white', bg='deepskyblue')
        self.me_first.configure(fg='black', bg='white')

    def click_for_black(self):
        global side
        side = 'black'
        self.for_black.configure(fg='white', bg='deepskyblue')
        self.for_white.configure(fg='black', bg='white')

    def click_for_white(self):
        global side
        side = 'white'
        self.for_white.configure(fg='white', bg='deepskyblue')
        self.for_black.configure(fg='black', bg='white')

    def click_white_up(self):
        global upper_chess
        upper_chess = 'white'
        self.white_up.configure(fg='white', bg='deepskyblue')
        self.black_up.configure(fg='black', bg='white')

    def click_black_up(self):
        global upper_chess
        upper_chess = 'black'
        self.black_up.configure(fg='white', bg='deepskyblue')
        self.white_up.configure(fg='black', bg='white')

    def click_confirm(self):
        self.win.destroy()


class Display:

    def __init__(self, board=None, pipe=None, mode=None):
        global ori_board
        if board is None:
            self.game_board = GameBoard()
        else:
            self.game_board = board
        self.s = pipe
        self.turn = 1
        self.win = tk.Tk()
        self.win.title("Surakarta")
        self.buffer = []
        ori_board = cv2.imread('resources/pictures/board.jpeg')
        ori_board = ori_board[..., ::-1]
        ori_board = cv2.resize(ori_board, (600, 600), interpolation=cv2.INTER_NEAREST)
        ori_board = ImageTk.PhotoImage(Image.fromarray(ori_board))
        self.board_frame = tk.Frame(self.win)
        self.control_panel = tk.Frame(self.win, bg='WHITE', bd=0, height=600, width=200)
        self.display_canvas = tk.Canvas(self.board_frame, bg='WHITE', bd=0, heigh=600, width=600)
        self.display_canvas.create_image(0, 0, anchor='nw', image=ori_board)
        self.r = 15
        self.a = None
        self.b = None
        self.x = None
        self.y = None
        self.p = None
        self.mode = mode
        self.display_posi = []
        self.my_turn_flag = None
        for i in range(15):
            line_display_posi = []
            for j in range(15):
                x = 39.2 * j + 25
                y = 39.2 * i + 25
                line_display_posi.append(Position(x, y))
            self.display_posi.append(line_display_posi)
        if self.s is not None:
            while self.my_turn_flag is None:
                try:
                    print('try receiving1')
                    info = self.receive()
                    print(info)
                    info = info.split('.')
                    if info[1] == 'first':
                        self.my_turn_flag = True
                        t = Thread(target=self.receive_position)
                        t.start()
                    elif info[1] == 'second':
                        self.my_turn_flag = False
                        t = Thread(target=self.receive_position)
                        t.start()
                except IndexError:
                    pass

    def receive_position(self):
        while True:
            if self.my_turn_flag is False:
                print('receiving')
                if self.buffer == ['']:
                    self.buffer.pop()
                if self.buffer:
                    print('info', self.buffer)
                    info = self.buffer.pop(0)
                    info = info.split('.')[1].split(',')
                    self.game_board.make_move([int(info[0]), int(info[1])], self.turn)
                    self.display_chess(self.game_board)
                    self.turn = -self.turn
                    self.change_turn()
                else:
                    info = self.s.recv(1024).decode('utf-8')
                    info = info.split('#')
                    for info_ in info:
                        self.buffer.append(info_)
                    info = self.buffer.pop(0)
                    info = info.split('.')[1].split(',')
                    self.game_board.make_move([int(info[0]), int(info[1])], self.turn)
                    self.display_chess(self.game_board)
                    self.turn = -self.turn
                    self.change_turn()

    def change_turn(self):
        if self.my_turn_flag:
            self.my_turn_flag = False
        else:
            self.my_turn_flag = True

    def receive(self):
        if self.buffer:
            info = self.buffer.pop(0)
            print('return', info)
            return info
        else:
            info = self.s.recv(1024).decode('utf-8')
            info = info.split('#')
            for info_ in info:
                self.buffer.append(info_)
            info = self.buffer.pop(0)
            print('return', info)
            return info

    def display_chess(self, game_board):
        self.display_canvas.delete("chess")
        for i in range(15):
            for j in range(15):
                if game_board.board[i][j] == WHITE_CHESS:
                    self.display_canvas.create_oval(self.display_posi[i][j].x - self.r,
                                                    self.display_posi[i][j].y - self.r,
                                                    self.display_posi[i][j].x + self.r,
                                                    self.display_posi[i][j].y + self.r, fill='GhostWhite', tag='chess')
                elif game_board.board[i][j] == BLACK_CHESS:
                    self.display_canvas.create_oval(self.display_posi[i][j].x - self.r,
                                                    self.display_posi[i][j].y - self.r,
                                                    self.display_posi[i][j].x + self.r,
                                                    self.display_posi[i][j].y + self.r, fill='Black', tag='chess')
        self.win.update()
        if game_board.judge() is not None:
            messagebox.showinfo('Game End', 'The Game is End!')
            self.win.quit()


    def place_chess(self, event):
        if self.my_turn_flag or self.s is None:
            for row_index in range(15):
                for col_index in range(15):
                    if self.display_posi[row_index][col_index].x - self.r < event.x < self.display_posi[row_index][
                        col_index].x + self.r and self.display_posi[row_index][col_index].y - self.r < event.y < \
                            self.display_posi[row_index][col_index].y + self.r:
                        if self.game_board.board[row_index][col_index] == NO_CHESS:
                            self.game_board.make_move([row_index, col_index], self.turn)
                            self.turn = -self.turn
                            self.display_chess(self.game_board)
                            if self.s is not None:
                                print('position.' + str(row_index) + ',' + str(col_index))
                                self.s.send(bytes('position.' + str(row_index) + ',' + str(col_index), 'utf-8'))
                                self.change_turn()
                            if self.mode is not None:
                                #ai = SearchEngine(self.game_board, self.turn)
                                ai = AlphaBeta(self.game_board, self.turn)
                                move = ai.search()
                                self.game_board.make_move([move[0], move[1]], self.turn)
                                self.turn = -self.turn
                                self.display_chess(self.game_board)
                            return

    def check_play_legal(self):
        if self.a != self.x or self.b != self.y:
            return True
        return False

    def display(self):
        self.display_chess(self.game_board)
        self.board_frame.pack(side=tk.LEFT)
        #self.control_panel.pack(side=tk.RIGHT)
        self.display_canvas.pack()
        self.win.bind("<Button-1>", self.place_chess)
        self.win.bind("<Return>", self.retract)
        self.win.mainloop()

    def retract(self, event):
        print('enr')
        if self.s is None:
            move = self.game_board.history.pop()
            self.game_board.board[move[0]][move[1]] = NO_CHESS
            self.turn = -self.turn
            self.display_chess(self.game_board)

    def refresh(self):
        self.board_frame.pack(side=tk.LEFT)
        self.control_panel.pack(side=tk.RIGHT)
        self.display_canvas.pack()
        # self.display_chess(board)
        self.win.update()


if __name__ == "__main__":
    while True:
        ui = MainUI()
        if mode == 1:
            UserName()
            w = WaitingRoom()
            w.win.destroy()
            v = Display(pipe=s)
            v.display()
            v.win.destroy()
        elif mode == 2:
            v = Display(mode='AI')
            v.display()
            v.win.destroy()
        elif mode == 3:
            print('enter')
            v = Display()
            v.display()
            v.win.destroy()
        else:
            break

