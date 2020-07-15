# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import Image,ImageTk
import pandas as pd
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip

#間違ったフラグ、復習したいフラグを立てる

"""
#------awsログイン～S3上のtxt取得------

import boto3
from boto3.session import Session

profile = '2929'
session=Session(profile_name=profile)
s3 = session.resource('s3')
bucket = s3.Bucket("tashimatraining")
obj = bucket.Object("testtest.txt")
response = obj.get()
body = response['Body'].read()
print(body.decode('utf-8'))
"""

#------csv読み込み～書き込み------
"""
csv_file = open("./wordlist.csv","r+",encoding="utf-8",errors="",newline="")
creader = csv.reader(csv_file,delimiter=",",doublequote=True,lineterminator="\r\n", quotechar='"', skipinitialspace=True)
cwriter = csv.writer(csv_file)


def opencsv(csv_file)
"""
def update_csv(csv_file, wordbook, csv_name):
    new_count = 0 #複数新規追加時に被らない命名をするための識別子
    for word in wordbook:
        a = int(word.id)
        if(word.proc_flag==1):
            new_count += 1
            csv_file.loc["new"+str(new_count)]=[str(word.id),word.word,word.read,word.genre," ".join(word.tag_list),word.description]
            word.proc_flag = 0
            #print(csv_file)
        if(word.proc_flag==2):
            print(csv_file)
            csv_column=csv_file.query("id==@a").index[0] #idが一致するcsv行名
            csv_file.loc[csv_column]=[word.id,word.word,word.read,word.genre," ".join(word.tag_list),word.description]
            word.proc_flag = 0
        if(word.proc_flag==3):
            print("ccc")
            csv_column=csv_file.query("id==@a").index[0] #idが一致するcsv行名
            csv_file.drop(index = csv_column,inplace=True)
            print(csv_file)
            word.proc_flag = 0
    csv_file.to_csv(csv_name,index=False)
    csv_file, wordbook = read_csv_clear_wordbook(csv_name)
    return csv_file,wordbook

def clear_flag(wordbook):#wordbookの変更キャンセル    
    for word in wordbook:
        word.proc_flag = 0
    return wordbook

#------WordとWordbook------

class Word:

    def __init__(self, id=0, word="", read="", genre="", tag="", description="", proc_flag=0):
        self.id=int(id)
        self.word=word
        self.read=read
        self.genre=genre
        if tag is None:
            self.tag_list = ""
        else:
            self.tag_list=tag.split(' ')
        self.description=description
        self.proc_flag=proc_flag

    def show_info(self):
        print("ID:"+str(self.id),"Word:"+self.word,"Read:"+self.read,"Genre:"+self.genre,"tag:"+str(self.tag_list),"Desc:"+self.description,"flag:"+str(self.proc_flag))

    def get_info(self):
        return [str(self.id),self.word,self.read,self.genre,self.tag_list,self.description]


class Wordbook(list):

    def show_info(self):
        for row in self:
            row.show_info()

    def get_info(self):
        info_list = []
        for row in self:
            info_list.append(row.get_info())
        return info_list

    def search(self, search_flag=0, target=""):
        #search_flagが0:id 1:word or read 2:genre 3:tag 100:全部
        hit_word = []
        if search_flag==0:
            for i in self:
                if i.id == str(target):
                    #i.show_info()
                    hit_word.append(i.get_info())
                    break
        elif search_flag ==1:
            for i in self:
                if target in i.word or target in i.read:
                    #i.show_info()
                    hit_word.append(i.get_info())
        elif search_flag == 2:
            for i in self:
                if target in i.genre:
                    #i.show_info()
                    hit_word.append(i.get_info())
        elif search_flag == 3:
            for i in self:
                #tag_listを1次元にしてから検索(スマートにしたい)
                flat_tag_list = ""
                for j in i.tag_list:
                    flat_tag_list += " " + j
                if target in flat_tag_list:
                    #i.show_info()
                    hit_word.append(i.get_info())

        elif search_flag == 100:
            for i in self:
                #tag_listを1次元にしてから検索(スマートにしたい)
                flat_tag_list = ""
                for j in i.tag_list:
                    flat_tag_list += " " + j
                if i.id == str(target) or target in i.word or target in i.read or target in i.genre or target in flat_tag_list:
                    hit_word.append(i.get_info())
        return hit_word

    def search_test(self, search_flag=0, target=""):
        #search_flagが0:id 1:word or read 2:genre 3:tag
        if search_flag==0:
            for i in self:
                if i.id == str(target):
                    i.show_info()
                    break
        elif search_flag ==1:
            for i in self:
                if target in i.word or target in i.read:
                    i.show_info()
        elif search_flag == 2:
            for i in self:
                if target in i.genre:
                    i.show_info()
        elif search_flag == 3:
            for i in self:
                for j in i.tag_list:
                    if target in j:
                        i.show_info()

#csvアップデートの方式は2つ
#1 追加、削除の都度csvの書き換え実施→→→必ず保存される、差分のみ保存作業ができる
#2 追加、削除の後にsave関数で実施→→→誤った登録や削除がされない、差分のみ書き込み作業にするにはword内にnewとdelの削除フラグが必要
#一旦2で作る
#newdel_flag==1(新規)のときは、new_wordでwordbookにappendまで行う、save時にフラグの行をcsvの後ろに書き込みしソート
#newdel_flag==2(更新)のときは、update_wordでwordbookに更新。save時にフラグの行を更新。
#newdel_flag==3(削除)のときは、del_wordでフラグを立てるだけ。save時にフラグの行を削除したcsvを書きこんだあとにwordbookから削除

    def new_word(self, word="", read="", genre="", tag="", description=""):
    #空きIDか
        i = 0
        new_id = 0
        while(1):
            i += 1
            for j in range(0, len(self)-1):
                flag = 0
                if i == self[j].id:
                    break
                flag = 1
            if flag == 1 or i > self[len(self)-1].id:
                new_id = i
                break

        new_word = Word(new_id,word,read,genre,tag,description,1)
        self.append(new_word)

    def update_word(self, up_id=0, up_word="", up_read="", up_genre="", up_tag="", up_description=""):
        for word in self:
            if word.id == up_id:
                word.proc_flag=2
                if (up_word!=""):
                    word.word=up_word
                if(up_read!=""):
                    word.read=up_read
                if(up_genre!=""):
                    word.genre=up_genre
                if(up_tag!=""):
                    word.tag_list=up_tag.split(" ")
                if(up_description!=""):
                    word.description=up_description
                return
        print("更新エラー：該当のIDが存在しません！")

    def del_word(self, del_id=0):
        for word in self:
            if word.id == del_id:
                word.proc_flag = 3
                return
        print("削除エラー：該当のIDが存在しません！")

    def clear_proc_flag(self):
        for word in self:
            word.proc_flag=0


#------csv読み込んでwordbookに入れる------
def read_csv_clear_wordbook(csv_name):    
    csv_file=pd.read_csv(csv_name)
    csv_file=csv_file.sort_values("id")
    wordbook=Wordbook()
    wordbook.clear()
    val_list = csv_file.values.tolist()
    for val in val_list:
        word = Word(val[0],val[1],val[2],val[3],val[4],val[5])
        wordbook.append(word)
    return csv_file,wordbook


#GUI作っていこう

#global
my_color = "snow"
csv_name = ""
csv_file = None
wordbook = None

class FrameBase(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1200x800")
        self.frame = StartPageFrame(self)
        self.frame.pack(expand = True,fill="both")

    def change(self, frame):
        self.frame.pack_forget()
        self.frame = frame(self)
        self.frame.pack(expand = True,fill="both")

    def change_startpage(self):
        self.frame.pack_forget()
        self.frame = StartPageFrame(self)
        self.frame.pack(expand = True, fill = "both")

class StartPageFrame(tk.Frame):

    def __init__(self,master = None, **kwargs):

        tk.Frame.__init__(self,master,**kwargs)
        master.title("単語帳")
        self.configure(bg=my_color)

        title_label = tk.Label(self,text = "単語帳",font = ("Meiryo UI",80),bg=my_color)
        title_label.place(relwidth=0.5,relheight = 0.4,relx=0.25,rely=0.2)
        start_button = tk.Button(self,text = "単語帳を選択してスタート", font = ("Meiryo UI",9), command = self.start_clicked,bg=my_color)
        start_button.place(relwidth=0.3,relx=0.35,rely=0.55)
        start_button2 = tk.Button(self,text = "デモ単語帳でスタート", font = ("Meiryo UI",9), command = self.start_clicked_demo,bg=my_color)
        start_button2.place(relwidth=0.3, relx = 0.35, rely = 0.6)
        fin_button = tk.Button(self,text = "画面を閉じて終了", font = ("Meiryo UI",9), command = self.fin_clicked,bg=my_color)
        fin_button.place(relwidth=0.3,relx=0.35,rely=0.65)

    def start_clicked(self):
        print("aaa")

    def start_clicked_demo(self):

        global csv_file, wordbook, csv_name
        csv_name = "./wordlist.csv"
        csv_file, wordbook = read_csv_clear_wordbook(csv_name)
        self.master.change(WordbookdemoFrame)


    def fin_clicked(self):
        root.quit()

class WordbookdemoFrame(tk.Frame):

    def __init__(self, master = None,**kwargs):

        tk.Frame.__init__(self,master,**kwargs)

        self.configure(bg=my_color)
        self.my_font = font.Font(master,family="Meiryo UI",size = 9)
        self.apimagecanvas = tk.Canvas(self,width=140,height=50,bg=my_color)
        self.apimage = tk.PhotoImage(file="./image/logo.png")
        self.tree = ttk.Treeview(self)
        self.search_button = tk.Button(self,text = "検索",font = self.my_font, command = lambda:self.search(master),bg=my_color)
        self.return_button = tk.Button(self,text = "戻る",font = self.my_font, command = lambda:self.reload(master),bg=my_color)
        self.reload_button = tk.Button(self, text = "再読み込み", font = self.my_font, command = lambda:self.reload(master),bg=my_color)
        self.register_button = tk.Button(self,text = "新規単語登録",font = self.my_font, command = self.register_clicked,bg=my_color)
        self.textbox = tk.Entry(font = self.my_font)
        #reload
        self.reload(master)


    def reload(self, master = None, **kwargs):    
        #ウィジェット配置
        self.apimagecanvas.place(relx=0.023,rely=0.002)
        self.apimagecanvas.create_image(0, 0, image=self.apimage, anchor=tk.NW)
        self.apimagecanvas.bind("<Button-1>", lambda event:self.master.change_startpage())
        self.return_button.place_forget()
        self.search_button.place(relwidth=0.05,relx=0.825,rely=0.072)
        self.textbox.place(relwidth=0.69,relx=0.13,rely = 0.077)
        self.register_button.place(relwidth=0.1,relx=0.025,rely = 0.072)
        self.reload_button.place(relwidth=0.1,relx=0.3,rely=0.002)
        master.title("単語一覧")
        self.tree.place_forget()
        self.tree = ttk.Treeview(self)

        self.tree["columns"]=(1,2,3,4,5,6)
        self.tree["show"]="headings"
        self.tree.column(1,width=20)
        self.tree.column(2,width=200)
        self.tree.column(3,width=200)
        self.tree.column(4,width=200)
        self.tree.column(5,width=200)
        self.tree.column(6,width=280)

        self.tree.heading(1,text="ID")
        self.tree.heading(2,text="単語")
        self.tree.heading(3,text="読み")
        self.tree.heading(4,text="ジャンル")
        self.tree.heading(5,text="タグ")
        self.tree.heading(6,text="意味")

        self.tree.bind("<Double-1>",lambda event:self.gotoWordFrame(event,master))

        wordlist = wordbook.get_info()
        for row in wordlist:
            if(len(row[5])<30):
                self.tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5][:30]))
            else:
                self.tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5][:31][:-1]+"..."))  #30文字以上の表記省略        
        self.tree.place(relwidth=0.95,relx=0.025,rely=0.11,height = 700)

    def gotoWordFrame(self,event,master):

        if not self.tree.selection():
            return

        item = self.tree.selection()[0]
        for word in wordbook:
            if self.tree.item(item,'value')[0] == str(word.id):
                temp = WordFrameBase(word)
                temp.update()


    def search(self, master = None):
        self.reload(master)
        self.return_button.place(relwidth=0.05,relx=0.885,rely=0.01)
        self.tree.place_forget()
        self.tree = ttk.Treeview(self)

        self.tree["columns"]=(1,2,3,4,5,6)
        self.tree["show"]="headings"
        self.tree.column(1,width=20)
        self.tree.column(2,width=200)
        self.tree.column(3,width=200)
        self.tree.column(4,width=200)
        self.tree.column(5,width=200)
        self.tree.column(6,width=280)

        self.tree.heading(1,text="ID")
        self.tree.heading(2,text="単語")
        self.tree.heading(3,text="読み")
        self.tree.heading(4,text="ジャンル")
        self.tree.heading(5,text="タグ")
        self.tree.heading(6,text="意味")


        self.tree.bind("<Double-1>",lambda event:self.gotoWordFrame(event,master))

        for row in wordbook.search(100,self.textbox.get()):
            if(len(row[5])<30):
                self.tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5][:30]))
            else:
                self.tree.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5][:31][:-1]+"...")) 
        self.tree.place(relwidth=0.95,relx=0.025,rely=0.11,height = 700)

    def register_clicked(self):
        global csv_file, wordbook, csv_name
        csv_name = "./wordlist.csv"
        csv_file, wordbook = read_csv_clear_wordbook(csv_name)
        self.master.change(RegisterwordFrame)

class RegisterwordFrame(tk.Frame):

    def __init__(self, master = None, **kwargs):
        tk.Frame.__init__(self,master,**kwargs)
        #ウィジェット宣言
        self.configure(bg=my_color)
        self.wordbox = tk.Entry(self)
        self.readbox = tk.Entry(self)
        self.genrebox = tk.Entry(self)
        self.taglistbox = tk.Entry(self)
        self.descriptionbox = tk.Text(self)
        self.wordlabel = tk.Label(self, text = "単語",font = ("Meiryo UI",15),bg=my_color)
        self.readlabel = tk.Label(self, text = "読み",font = ("Meiryo UI",15),bg=my_color)
        self.genrelabel = tk.Label(self, text = "ジャンル",font = ("Meiryo UI",15),bg=my_color)
        self.taglistlabel = tk.Label(self, text = "タグ",font = ("Meiryo UI",15),bg=my_color)
        self.taglistlabel2 = tk.Label(self, text = "※複数登録したい場合は半角スペースで区切る",font = ("Meiryo UI",11),bg=my_color)
        self.descriptionlabel = tk.Label(self, text = "説明",font = ("Meiryo UI",15),bg=my_color)
        self.register_button = tk.Button(self,text = "登録",command = lambda:self.register_clicked(master),bg=my_color)
        self.return_button = tk.Button(self,text = "戻る",command = lambda:self.master.change(WordbookdemoFrame),bg=my_color)

        self.wordbox.place(relwidth=0.5,relx=0.4,rely=0.1)
        self.readbox.place(relwidth=0.5,relx=0.4,rely=0.2)
        self.genrebox.place(relwidth=0.5,relx=0.4,rely=0.3)
        self.taglistbox.place(relwidth=0.5,relx=0.4,rely=0.4)
        self.descriptionbox.place(relwidth=0.5,relx=0.4,rely=0.5,height = 180)
        self.wordlabel.place(relwidth=0.1,relx=0.2,rely=0.1)
        self.readlabel.place(relwidth=0.1,relx=0.2,rely=0.2)

        self.genrelabel.place(relwidth=0.1,relx=0.2,rely=0.3)
        self.taglistlabel.place(relwidth=0.1,relx=0.2,rely=0.4)
        self.taglistlabel2.place(relwidth=0.3,relx=0.1,rely=0.43)
        self.descriptionlabel.place(relwidth=0.1,relx=0.2,rely=0.5)
        self.register_button.place(relwidth=0.35,relx=0.3,rely=0.8)
        self.return_button.place(relwidth=0.35,relx=0.3,rely=0.9)


    def register_clicked(self, master = None):
        global wordbook, csv_file
        wordbook.new_word(self.wordbox.get(),self.readbox.get(),self.genrebox.get(),self.taglistbox.get(),self.descriptionbox.get('1.0', tk.END))
        csv_file, wordbook = update_csv(csv_file, wordbook, "./wordlist.csv")
        master.change(WordbookdemoFrame)
        #reload


class WordFrameBase(tk.Tk):

    def __init__(self,word):
        tk.Tk.__init__(self)
        self.geometry("1100x700")
        self.frame = WordPageFrame(self,word)
        self.frame.pack(expand = True, fill="both")
#        self.wm_attributes("-transparentcolor", "green")

    def change(self, frame, word = None):
        self.frame.pack_forget()
        self.frame = frame(self, word)
        self.frame.pack(expand = True, fill="both")

class WordPageFrame(tk.Frame):

    def __init__(self,master = None, word=None):
        tk.Frame.__init__(self,master)

        self.canvas = tk.Canvas(self,width=1100,height=700,bg="snow")
        self.canvas.place(x=0, y=0)
        self.canvas.create_line(113,147,113,136,102,136,102,147,109,147,109,140,102,140,102,147,989,147,fill="gray60")
        self.canvas.create_line(116,180,116,173,109,173,109,180,389,180,fill="gray60")
        self.canvas.create_line(116,220,116,213,109,213,109,220,589,220,fill="gray60")
        self.canvas.create_line(116,260,116,253,109,253,109,260,589,260,fill="gray60")
        self.canvas.create_rectangle(102, 300, 989, 570, fill = "ghost white")#塗りつぶし

        self.update_button = tk.Button(self,text = "更新", command = lambda:self.gotoUpdateFrame(master, word))
        self.delete_button = tk.Button(self,text = "削除",command = lambda:self.delete_clicked(master, word),bg=my_color)
        self.return_button = tk.Button(self,text = "戻る",command = lambda:self.master.destroy())

        self.wordlabel = tk.Label(self, text = word.word,font = ("Meiryo UI",40),anchor="w",bg="snow")# """green""")
        self.readlabel = tk.Label(self, text = word.read,font = ("Meiryo UI",13),anchor="w",bg="snow")
        self.readlabel2 = tk.Label(self, text = "【読み】：",font = ("Meiryo UI",13),anchor="e",bg="snow")
        self.genrelabel = tk.Label(self, text = word.genre,font = ("Meiryo UI",13),anchor="w",bg="snow")
        self.genrelabel2 = tk.Label(self, text = "【ジャンル】：",font = ("Meiryo UI",13),anchor="e",bg="snow")
        self.taglistlabel = tk.Label(self, text = word.tag_list,font = ("Meiryo UI",13),anchor="w",bg="snow")
        self.taglistlabel2 = tk.Label(self, text = "【タグ】：",font = ("Meiryo UI",13),anchor="e",bg="snow")
        self.descriptionlabel = tk.Label(self, text = word.description,font = ("Meiryo UI",13),anchor="w",bg="ghost white")
        self.wordlabel.place(relwidth=0.8,x=120,y=74)
        self.readlabel.place(relwidth=0.7,x=220,y=152)
        self.readlabel2.place(width=100,x=120,y=152)
        self.genrelabel.place(relwidth=0.7,x=220,y=192)
        self.genrelabel2.place(width=100,x=120,y=192)
        self.taglistlabel.place(relwidth=0.7,x=220,y=232)
        self.taglistlabel2.place(width=100,x=120,y=232)
        self.descriptionlabel.place(width=880,x=105,y=305)

        self.update_button.place(width=120,x=110,y=600)
        self.delete_button.place(width=120,x=500,y=600)
        self.return_button.place(width=120,x=870,y=600)
        
    def gotoUpdateFrame(self, master = None, word = None):
        master.change(UpdatePageFrame, word)

    def delete_clicked(self, master = None, word = None):
        global wordbook,csv_file
        wordbook.del_word(word.id)
        csv_file, wordbook = update_csv(csv_file, wordbook, "./wordlist.csv")
        master.destroy()

class UpdatePageFrame(tk.Frame):

    def __init__(self,master = None, word = None):
        tk.Frame.__init__(self,master)

        self.wordbox = tk.Entry(self)
        self.readbox = tk.Entry(self)
        self.genrebox = tk.Entry(self)
        self.taglistbox = tk.Entry(self)
        self.descriptionbox = tk.Text(self)
        self.wordbox.insert(tk.END,word.word)
        self.readbox.insert(tk.END,word.read)
        self.genrebox.insert(tk.END,word.genre)
        self.taglistbox.insert(tk.END,word.tag_list)
        self.descriptionbox.insert(tk.END,word.description)
        self.wordlabel = tk.Label(self, text = "単語",font = ("",15))
        self.readlabel = tk.Label(self, text = "読み",font = ("",15))
        self.genrelabel = tk.Label(self, text = "ジャンル",font = ("",15))
        self.taglistlabel = tk.Label(self, text = "タグ",font = ("",15))
        self.taglistlabel2 = tk.Label(self, text = "※複数登録したい場合は半角スペースで区切る",font = ("",11))
        self.descriptionlabel = tk.Label(self, text = "説明",font = ("",15))
        self.update_button = tk.Button(self,text = "更新", command = lambda:self.update(master,word))
        self.return_button = tk.Button(self,text = "戻る",command = lambda:self.master.change(WordPageFrame,word))

        self.wordbox.place(relwidth=0.5,relx=0.4,rely=0.1)
        self.readbox.place(relwidth=0.5,relx=0.4,rely=0.2)
        self.genrebox.place(relwidth=0.5,relx=0.4,rely=0.3)
        self.taglistbox.place(relwidth=0.5,relx=0.4,rely=0.4)
        self.descriptionbox.place(relwidth=0.5,relx=0.4,rely=0.5,height = 180)
        self.wordlabel.place(relwidth=0.1,relx=0.2,rely=0.1)
        self.readlabel.place(relwidth=0.1,relx=0.2,rely=0.2)
        self.genrelabel.place(relwidth=0.1,relx=0.2,rely=0.3)
        self.taglistlabel.place(relwidth=0.1,relx=0.2,rely=0.4)
        self.taglistlabel2.place(relwidth=0.3,relx=0.1,rely=0.43)
        self.descriptionlabel.place(relwidth=0.1,relx=0.2,rely=0.5)
        self.return_button.place(relwidth=0.35,relx=0.3,rely=0.9)
        self.update_button.place(relwidth=0.35,relx=0.3,rely=0.85)

    def update(self, master, word):
        global wordbook, csv_file
        wordbook.update_word(word.id,self.wordbox.get(),self.readbox.get(),self.genrebox.get(),self.taglistbox.get(),self.descriptionbox.get('1.0', tk.END))
        update_csv(csv_file, wordbook, "./wordlist.csv")
        word = Word(word.id, self.wordbox.get(), self.readbox.get(), self.genrebox.get(), self.taglistbox.get(), self.descriptionbox.get('1.0', tk.END),proc_flag = 0)
#        master.change(WordPageFrame,csv_file,wordbook,word)
        master.destroy()


root = FrameBase()
root.mainloop()



