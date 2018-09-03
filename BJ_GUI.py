import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
import sys
import os
from time import sleep
from tkinter import messagebox


#カードのラベル（本当はcsvから取得すべき）
label_list =['A','2','3','4','5','6','7','8','9','10','J','Q','K']
#ディーラー、プレイヤーの持ち金、レベル、ターン回数、名前を保存する変数を辞書で持つ。
dealer = {"turn":"ディーラー", "hit":1, "point":0}
player = {"turn":"あなた","hit":1, "point":0}

dealer_results =[0,0,0,0,0,0,0,0,0,0,0,0,0,0]

base_folder = os.path.dirname(__file__)
print('base_folder ==> ' + base_folder)
image_path = os.path.join(base_folder, 'trump', 'png')
print('image_path ==> ' + image_path)

#カードのリスト取得
csv_path = os.path.join(base_folder, 'card.csv')
print('csv_path ==> ' + csv_path)

with open(csv_path, 'r') as f:
    df = pd.read_csv(f)
df_i = df.set_index('マーク')

#csv_file = open(os.path.join(base_folder, 'trump_list.csv'), "r", encoding="utf8")
trump_list = {
                "スペードA":"s01.png",
                "スペード2":"s02.png",
                "スペード3":"s03.png",
                "スペード4":"s04.png",
                "スペード5":"s05.png",
                "スペード6":"s06.png",
                "スペード7":"s07.png",
                "スペード8":"s08.png",
                "スペード9":"s09.png",
                "スペード10":"s10.png",
                "スペードJ":"s11.png",
                "スペードQ":"s12.png",
                "スペードK":"s13.png",
                "ダイヤA":"d01.png",
                "ダイヤ2":"d02.png",
                "ダイヤ3":"d03.png",
                "ダイヤ4":"d04.png",
                "ダイヤ5":"d05.png",
                "ダイヤ6":"d06.png",
                "ダイヤ7":"d07.png",
                "ダイヤ8":"d08.png",
                "ダイヤ9":"d09.png",
                "ダイヤ10":"d10.png",
                "ダイヤJ":"d11.png",
                "ダイヤQ":"d12.png",
                "ダイヤK":"d13.png",
                "クラブA":"c01.png",
                "クラブ2":"c02.png",
                "クラブ3":"c03.png",
                "クラブ4":"c04.png",
                "クラブ5":"c05.png",
                "クラブ6":"c06.png",
                "クラブ7":"c07.png",
                "クラブ8":"c08.png",
                "クラブ9":"c09.png",
                "クラブ10":"c10.png",
                "クラブJ":"c11.png",
                "クラブQ":"c12.png",
                "クラブK":"c13.png",
                "ハートA":"h01.png",
                "ハート2":"h02.png",
                "ハート3":"h03.png",
                "ハート4":"h04.png",
                "ハート5":"h05.png",
                "ハート6":"h06.png",
                "ハート7":"h07.png",
                "ハート8":"h08.png",
                "ハート9":"h09.png",
                "ハート10":"h10.png",
                "ハートJ":"h11.png",
                "ハートQ":"h12.png",
                "ハートK":"h13.png"
                }

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("The Black Jack")
        self.create_widgets(master)

    def create_widgets(self,master):
        super().__init__(master)
        frame = tk.LabelFrame(master,bd=2,relief="ridge",text="menu")
        frame.pack(fill="x")

        self.Start_button = tk.Button(frame,text="Start Game", command=self.Start_Game)
        #self.Start_button = tk.Button(frame,text="Start Game", command=TurnProcess())
        self.Start_button.pack(anchor="nw",side="left")

        self.Quit_button = tk.Button(frame,text="Leave Game", command=master.destroy)
        self.Quit_button.pack(anchor="ne")

        frame2 = tk.Frame(master,bd=2,relief="ridge")
        frame2.pack(fill="x")
        self.dealer_boad = tk.Canvas(frame2, width=1030, height=310, bg='dark green')
        self.dealer_boad.pack(fill='both')
        self.player_boad = tk.Canvas(frame2, width=1030, height=310, bg='dark blue')
        self.player_boad.pack(fill='both')

        self.dealer_im = {}
        self.player_im = {}

        return

    def Start_Game(self):
        #初期化する処理の追加が必要

        messagebox.showinfo ("ディーラーより","ゲームを始めます")
        #im1 = tk.PhotoImage(file=os.path.join(image_path, trump_list['ダイヤQ']))
        #self.dealer_boad.create_image(5,5, anchor='nw', image = im1)
        dealer["hit"], dealer["point"] ,dealer_result = self.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
        player["hit"], player["point"] ,dealer_result = self.choice_card(player["turn"], player["hit"], player["point"])
        dealer["hit"], dealer["point"] ,dealer_result = self.choice_card(dealer["turn"], dealer["hit"], dealer["point"])

        i = 0
        while(i == 0):
            player["hit"], player["point"],dealer_result = self.choice_card(player["turn"], player["hit"], player["point"])
            #self.text_area.insert('end','もう一枚引きますか？続けるには y を入力してください。\n')
            result = messagebox.askquestion("ディーラーより","もう一枚引きますか？")
            if result == 'no':
                i = 1
        i = 0
        while(i == 0):
            i = self.decide_dealer(dealer["turn"], dealer["hit"], dealer["point"])

        self.V_Check(player["point"], dealer["point"], dealer["hit"], dealer_result)

        return

    def choice_card(self, turn, hit, point):
        #print(turn + 'の番です')
        messagebox.showinfo ("ディーラーより", turn + 'の番です')

        i = 0
        while(i == 0):
            #ランダムにスイート（行）を選択
            suit_df = df_i.sample(n=1)
            #不要な文字列を削除してスイートのみにする。改善の余地あり
            suit = str(suit_df.index)
            suit = suit.replace("Index(['", "")
            suit = suit.replace("'], dtype='object', name='マーク')", "")
            #print('suit ==> ' + suit)
            #数字のリストの中から、ランダムに数字（列）を選択
            rank = random.choice(label_list)
            #print('rank ==> ' + str(rank))
            #カードがNULLでないかの判定
            if (str(df_i.loc[suit,rank]) != 'nan'):
                i = 1

        if(hit > 1 and turn == 'ディーラー'):
            #print(turn + 'は' + 'カードを引きました')
            messagebox.showinfo ("ディーラーより",turn + 'はカードを引きました')
        else:
            #print(turn + 'は' + suit + 'の' + str(suit_df[rank].name) + 'を引きました')
            messagebox.showinfo ("ディーラーより", turn + 'は' + suit + 'の' + str(suit_df[rank].name) + 'を引きました')

        xrange = (hit-1) * 205 + 5

        if(hit > 1 and turn == 'ディーラー'):
            dealer_results[hit] = trump_list[suit + rank]
            #messagebox.showinfo ("dealer_results[hit]",'dealer_results[hit]==>' + str(dealer_results[hit]))
            self.dealer_im[hit] = tk.PhotoImage(file=os.path.join(image_path, 'z01.png'))
            self.dealer_boad.create_image(xrange ,5, anchor='nw', image = self.dealer_im[hit])
        elif(turn == 'ディーラー'):
            dealer_results[hit] = trump_list[suit + rank]
            self.dealer_im[hit] = tk.PhotoImage(file=os.path.join(image_path, trump_list[suit + rank]))
            self.dealer_boad.create_image(xrange ,5, anchor='nw', image = self.dealer_im[hit])
        else:
            self.player_im[hit] = tk.PhotoImage(file=os.path.join(image_path, trump_list[suit + rank]))
            self.player_boad.create_image(xrange ,5, anchor='nw', image = self.player_im[hit])
        hit += 1
        point += int(suit_df[rank])
        df_i.at[suit,rank] = None

        return hit, point, dealer_results

    def decide_dealer(self,turn,hit,point):
        if(point < 17):
            dealer["hit"], dealer["point"], dealer_results = self.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
            #print("dealer_hit ==>" + str(dealer["hit"]) + " dealer_point ==>" + str(dealer["point"]))
            return 0
        else:
            pass
            return 1

    def V_Check(self, player_point, dealer_point, hit, dealer_results):
        #messagebox.showinfo ("Vcheck",'Vcheck')
        for i in range(hit-1):
            #messagebox.showinfo ("Vcheck",'dealer_results ==> '+ str(dealer_results))
            #messagebox.showinfo ("Vcheck",'i ==> '+ str(i) + ' hit ==> '+ str(hit))
            #messagebox.showinfo ("Vcheck",'dealer_results[i]==> '+ str(dealer_results[i+2]))
            xrange = (i) * 205 + 5
            #messagebox.showinfo ("Vcheck",'xrange ==> '+ str(xrange))
            self.dealer_im[i] = tk.PhotoImage(file=os.path.join(image_path, str(dealer_results[i+1])))
            self.dealer_boad.create_image(xrange ,5, anchor='nw', image = self.dealer_im[i])

        #self.dealer_im[0] = tk.PhotoImage(file=os.path.join(image_path, str(dealer_results[1])))
        #self.dealer_boad.create_image(5 ,5, anchor='nw', image = self.dealer_im[0])

        messagebox.showinfo ("ディーラーより", "あなたの得点 ： " + str(player["point"]) + '\n' + "ディーラーの得点 ： " + str(dealer["point"]))
        if(player_point > 21 and dealer_point > 21):
            messagebox.showinfo ("ディーラーより", '引き分けです')
        if(player_point > 21 and dealer_point <= 21):
            messagebox.showinfo ("ディーラーより", '残念でした！\nあなたの負けです')
        if(player_point <= 21 and dealer_point > 21):
            messagebox.showinfo ("ディーラーより",'おめでとう！\nあなたの勝ちです')
        if(player_point <= 21 and dealer_point <= 21 and player_point > dealer_point):
            messagebox.showinfo ("ディーラーより",'おめでとう！\nあなたの勝ちです')
        if(player_point <= 21 and dealer_point <= 21 and player_point == dealer_point):
            messagebox.showinfo ("ディーラーより",'引き分けです')
        if(player_point <= 21 and dealer_point <= 21 and player_point < dealer_point):
            messagebox.showinfo ("ディーラーより",'残念でした！\nあなたの負けです')
        return


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
