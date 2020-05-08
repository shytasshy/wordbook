# -*- coding: utf-8 -*-
#import tkinter

import csv
import pandas as pd
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip

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
csv_name = "./wordlist.csv"

def update_csv(csv_file, wordbook):
    new_count = 0 #複数新規追加時に被らない命名をするための識別子
    for word in wordbook:
        a = int(word.id)
        if(word.nudflag==1):
            new_count += 1
            csv_file.loc["new"+str(new_count)]=[str(word.id),word.word,word.read,word.genre," ".join(word.tag_list),word.description]
            word.nudflag = 0
            #print(csv_file)
        if(word.nudflag==2):
            csv_column=csv_file.query("id==@a").index[0] #idが一致するcsv行名
            csv_file.loc[csv_column]=[str(word.id),word.word,word.read,word.genre," ".join(word.tag_list),word.description]
           # print(csv_file)
            word.nudflag = 0
        if(word.nudflag==3):
            csv_column=csv_file.query("id==@a").index[0] #idが一致するcsv行名
            csv_file.drop(index = csv_column,inplace=True)
            print(csv_file)
            word.nudflag = 0
    csv_file.to_csv(csv_name,index=False)
    csv_file, wordbook = read_csv_clear_wordbook()
    return csv_file,wordbook

def clear_flag(wordbook):#wordbookの変更キャンセル    
    for word in wordbook:
        word.nudflag = 0
    return wordbook

"""
def update_csv(csv_writer, wordbook):
    for word in wordbook:
        if(word.nudflag==1):
            csv_writer.writerow([str(word.id),word.word,word.read,word.genre,word.tag_list,word.description])
            word.nudflag = 0
        if(word.nudflag==2):
            for row in cwriter:
                if(row[0]==word.id):
                    print("aaa")
            #csv内をidで検索してword.idと一致する場所を探す
            #その行を書き換え
            word.nudflag = 0
        if(word.nudflag==3):
            #csv内をidで検索してword.idと一致する場所を探す
            #その行を削除
            #wordbookからその行を削除
            word.nudflag = 0
"""
#------WordとWordbook------

class Word:

    def __init__(self, id=0, word="", read="", genre="", tag="", description="", nudflag=0):
        self.id=int(id)
        self.word=word
        self.read=read
        self.genre=genre
        self.tag_list=tag.split(' ')
        self.description=description
        self.nudflag=nudflag

    def show_info(self):
        print("ID:"+str(self.id),"Word:"+self.word,"Read:"+self.read,"Genre:"+self.genre,"tag:"+str(self.tag_list),"Desc:"+self.description,"flag:"+str(self.nudflag))


class Wordbook(list):

    def show_info(self):
        for row in self:
            row.show_info()

    def search(self, search_flag=0, target=""):
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
        new_id = len(self)+1
        new_word = Word(new_id,word,read,genre,tag,description,1)
        self.append(new_word)

    def update_word(self, up_id=0, up_word="", up_read="", up_genre="", up_tag="", up_description=""):
        for word in self:
            if word.id == up_id:
                word.nudflag=2
                if (up_word!=""):
                    word.word=up_word
                if(up_read!=""):
                    word.read=up_read
                if(up_genre!=""):
                    word.genre=up_genre
                if(up_tag!=""):
                    word.tag_list=uptag.split(" ")
                if(up_description!=""):
                    word.description=up_description
                return
        print("更新エラー：該当のIDが存在しません！")

    def del_word(self, del_id=0):
        for word in self:
            if word.id == del_id:
                word.nudflag = 3
                return
        print("削除エラー：該当のIDが存在しません！")

    def clear_nudflag(self):
        for word in self:
            word.nudflag=0


#------csv読み込んでwordbookに入れる------
def read_csv_clear_wordbook():    
    csv_file=pd.read_csv(csv_name)
    wordbook=Wordbook()
    wordbook.clear()
    val_list = csv_file.values.tolist()
    for val in val_list:
        word = Word(val[0],val[1],val[2],val[3],val[4],val[5])
        wordbook.append(word)
    return csv_file,wordbook

csv_file, wordbook = read_csv_clear_wordbook()
"""
#いろいろテスト
#気を付けること
#delの後に更新をかけることができ、その場合削除されない
wordbook.del_word(1)
wordbook.new_word(word="hogehoge", read="hoho", genre="gege", tag="hoge hoge", description="hogehoge")
wordbook.new_word(word="hogehoge2", read="hoho", genre="gege", tag="hoge hoge", description="hogehoge")
#wordbook.clear_nudflag()
csv_file, wordbook = update_csv(csv_file,wordbook)
wordbook.update_word(up_id=1,up_word="ieeeeeeeeei")
wordbook.new_word(word="hogehoge3", read="hoho", genre="gege", tag="hoge hoge", description="hogehoge")
csv_file, wordbook = update_csv(csv_file,wordbook)
"""


#GUI作っていこう