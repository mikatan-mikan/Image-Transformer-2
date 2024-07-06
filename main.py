from threading import Thread
from tkinter import CENTER, N, NW, Canvas, Event, IntVar, Tk,PhotoImage, Toplevel, filedialog, ttk, messagebox
from typing import List
try:
    from PIL import ImageTk,Image,ImageDraw,ImageOps,ImageFilter
except:#pillowがない環境ならインストールする
    from subprocess import run
    run("pip install pillow==9.2.0")
    messagebox.showinfo(title="ライブラリの不足",message="pillowがインストールされていないため、インストールを行いました")
    from PIL import ImageTk,Image,ImageDraw,ImageOps
try:
    import cv2
except:
    try:
        from subprocess import run
    except:pass
    run("pip install opencv-contrib-python==4.6.0.66")
    messagebox.showinfo(title="ライブラリの不足",message="open-cvがインストールされていないため、インストールを行いました")
    import cv2


    

class take_camera:
    def camera_change(self) -> None:
        self.camera_master.unbind("<Button-1>",self.camera_button_id)
        self.camera_change_flag = True
        self.camera_master.delete("now_image")
        self.camera_master.create_text(self.camera_win_size[0] / 2,self.camera_win_size[1] / 2, text="Loading Camera...",fill="black",font=("",20),tags="delete_flag")
        self.camera_num += 1
        self.camera_capture = cv2.VideoCapture(self.camera_num)
        if not self.camera_capture.isOpened():
            self.camera_num = 0
            self.camera_capture = cv2.VideoCapture(self.camera_num)
            if not self.camera_capture.isOpened():
                self.camera_num = -1
                self.camera_capture = cv2.VideoCapture(self.camera_num)
                if not self.camera_capture.isOpened():
                    messagebox.showerror(title="エラー",message="カメラを認識できません")
                    self.camera_root.destroy()
                    return
        self.camera_change_flag = False
    def camera_bef(self) -> None:
        self.camera_num = 0
        self.camera_var = IntVar()
        self.camera_var.set(0)
        ttk.Radiobutton(self.camera_master, value=0, variable=self.camera_var, text='カラー').place(x=10, y=self.camera_win_size[1] - 100,relheight=0.04)
        ttk.Radiobutton(self.camera_master, value=1, variable=self.camera_var, text='グレースケール').place(x=80, y=self.camera_win_size[1] - 100,relheight=0.04)
        self.camera_master.create_text(200,self.camera_win_size[1] - 100 + 3,text="カメラ映像をクリックで撮影",anchor=NW)
        self.camera_thread = Thread(target=self.camera_change)
        self.camera_change_button = ttk.Button(self.camera_master,text="カメラを変更",command = self.camera_thread.start)
        self.camera_change_button.place(x = 350,y = self.camera_win_size[1] - 100,relheight=0.04)
        self.camera_capture = cv2.VideoCapture(self.camera_num)
        if not self.camera_capture.isOpened():
            self.camera_num += 1
            self.camera_capture = cv2.VideoCapture(self.camera_num)
            if not self.camera_capture.isOpened():
                messagebox.showerror(title="エラー",message="カメラを認識できません")
                self.camera_root.destroy()
                return
        self.camera_change_flag = False
        self.camera()
        self.camera_master.delete("delete_flag")
    def camera(self) -> None:
        if self.camera_change_flag:
            self.camera_master.after(50, self.camera)
            return
        self.camera_master.delete("delete_flag")
        ret,frame = self.camera_capture.read()
        if self.camera_var.get() == 0:
            self.camera_cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif self.camera_var.get() == 1:
            self.camera_cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # NumPyのndarrayからPillowのImageに変換
        self.camera_pil_image = Image.fromarray(self.camera_cv_image)
        self.camera_pil_image.putalpha(255)
        # キャンバスのサイズを取得
        canvas_width = self.camera_win_size[0]
        canvas_height = self.camera_win_size[1] - 100
        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        if self.camera_var.get() == 0:
            self.camera_pil_image_win = ImageOps.pad(self.camera_pil_image, (canvas_width, canvas_height),color=(255,255,255,0))
        elif self.camera_var.get() == 1:
            self.camera_pil_image_win = ImageOps.pad(self.camera_pil_image, (canvas_width, canvas_height),color=(255))
        self.photo_image = ImageTk.PhotoImage(image=self.camera_pil_image_win)
        # 画像の描画
        self.camera_master.create_image(
                canvas_width / 2,       # 画像表示位置(Canvasの中心)
                canvas_height / 2,                   
                image=self.photo_image,  # 表示画像データ
                tags = "now_image"
                )
        try:
            self.camera_bind()
        except:pass
        self.camera_master.after(50, self.camera)
    def camera_click(self,event:Event) -> None:
        if event.y < self.camera_win_size[1] - 100:
            self.camera_save = self.camera_pil_image
            self.camera_root.destroy()
            self.put_pic_marker("",True)
    def camera_bind(self) -> None:
        self.camera_button_id = self.camera_master.bind("<Button-1>",self.camera_click)
    def camera_win(self) -> None:
        self.camera_root = Toplevel()
        self.camera_win_size = [self.camera_root.winfo_screenwidth(),self.camera_root.winfo_screenheight()]
        self.camera_root.geometry(f"{self.camera_win_size[0]}x{self.camera_win_size[1]}")
        self.camera_root.resizable(0,0)
        self.camera_root.title("写真")
        self.camera_master = Canvas(self.camera_root,width=self.camera_win_size[0],height=self.camera_win_size[1])
        self.camera_master.pack()
        self.camera_master.create_text(self.camera_win_size[0] / 2,self.camera_win_size[1] / 2, text="Loading Camera...",fill="black",font=("",20),tags="delete_flag")
        self.camera_master.after(100,self.camera_bef)
        self.camera_master.mainloop()


class change_point:
    def return_score(self) -> None:
        for i in range(len(self.point_entry_list)):
            if int(self.sub_point_entry[i][0].get()) < 0 or int(self.sub_point_entry[i][1].get()) < 0 or int(self.sub_point_entry[i][0].get()) > self.picture_window_size[0] * (1/self.float_scale) or int(self.sub_point_entry[i][1].get()) > self.picture_window_size[1] * (1/self.float_scale) :
                messagebox.showerror(title="エラー",message="数値が画像の範囲外です")
                return
        for i in range(len(self.point_entry_list)):
            for j in range(len(self.point_entry_list[i])):
                self.point_entry_list[i][j]["state"] = "NORMAL"
                self.point_entry_list[i][j].delete(0,len(self.point_entry_list[i][j].get()))
                self.point_entry_list[i][j].insert(0,self.sub_point_entry[i][j].get())
                self.point_entry_list[i][j]["state"] = "readonly"
            self.master.moveto(f"{i + 1}_mark",int(self.point_entry_list[i][0].get()) * self.float_scale + self.point_offset[0] + 250 - 3,int(self.point_entry_list[i][1].get()) * self.float_scale + self.point_offset[0] + 100 - 3)
            self.marker_line()
        self.sub_root.destroy()
        del self.sub_root
        return
    def sub_put_score(self) -> None:
        for i in range(len(self.sub_point_entry_in)):
            for j in range(len(self.sub_point_entry_in[i])):
                self.sub_point_entry[i][j]["state"] = "NORMAL"
                self.sub_point_entry[i][j].insert(0,self.sub_point_entry_in[i][j].get())
    def sub_put_obj(self) -> None:
        #背景を作る
        self.sub_dire = ["左上","左下","右下","右上"]
        self.sub_back_image = Image.new("RGBA",(200,200),(64,64,64,255))
        self.sub_back_image_tk = ImageTk.PhotoImage(self.sub_back_image)
        self.sub_master.create_image(0,0,image = self.sub_back_image_tk , anchor = NW)
        self.sub_point_entry = [[ttk.Entry(self.sub_master,width=3),ttk.Entry(self.sub_master,width=3)],
                                [ttk.Entry(self.sub_master,width=3),ttk.Entry(self.sub_master,width=3)],
                                [ttk.Entry(self.sub_master,width=3),ttk.Entry(self.sub_master,width=3)],
                                [ttk.Entry(self.sub_master,width=3),ttk.Entry(self.sub_master,width=3)]]
        self.sub_master.create_text(120, 10,text=f"x",fill="white",anchor = NW)
        self.sub_master.create_text(140, 10,text=f"y",fill="white",anchor = NW)
        for i in range(len(self.sub_point_entry)):
            self.sub_master.create_text(40, 30 + 7 + (i * 20),text=f"point{i + 1}({self.sub_dire[i]})",fill="white",anchor = CENTER)
            for j in range(len(self.sub_point_entry[i])):
                self.sub_point_entry[i][j].place(x = 110 + (j * 25), y = 30 + (i * 20),relheight=0.04)
                self.sub_point_entry[i][j]["state"] = "readonly"
        self.change_point_button = ttk.Button(self.sub_master,text="変更",width=8,command=self.return_score)
        self.change_point_button.place(x=100,y=150,relheight=0.04)
    def sub_win_bef(self,point_entry : List[List[ttk.Entry]]):
        self.sub_point_entry_in = point_entry
        return self.sub_win
    def sub_win(self) -> None:
        self.sub_root = Toplevel()
        self.sub_root.geometry("200x200")
        self.sub_root.resizable(0,0)
        self.sub_root.title("座標の変更")
        self.sub_master = Canvas(self.sub_root,width=200,height=200)
        self.sub_master.pack()
        self.sub_put_obj()
        self.sub_put_score()
        self.sub_master.mainloop()

class main(change_point,take_camera):
    def __init__(self) -> None:
        """
        点の画像の生成
        判定に使う&初期化されていない可能性のある物を初期化しておく
        """
        #読み込んだ画像の最初のサイズを保管
        self.picture_default_size = [None,None]
        #マーカーimageを作る
        self.marker = Image.new(mode="RGBA",size=(7,7),color=(0,0,0,0))
        marker_draw = ImageDraw.Draw(self.marker)
        marker_draw.ellipse((0,0,6,6),fill=(255,190,0,255),outline=(255,255,255))
        self.move_old = None
        self.bef_move = ""
        self.point_offset = [0,0]
        self.scale = 1000 #1000倍で保存 
        self.float_scale = self.scale / 1000
        self.click_dat = {}
        self.moving_image = False
        self.win_dat = {"height":600,"width":900}
    def check_size_entry(self) -> None:
        """
        保存サイズを確認
        """
        try:
            int(self.save_size_x_entry.get())
            int(self.save_size_y_entry.get())
            return True
        except:
            messagebox.showerror("エラー","保存サイズには数字以外を入力しないでください")
            return False
    def get_point(self):
        point_location = []
        for i in range(1,5):#1-4まで(それぞれの座標のリストを作る)
            tmp = self.master.coords(f"{i}_mark")
            tmp[0] , tmp[1] = (tmp[0] - 250 - self.point_offset[0] ) * self.change_size_num_re * (1/self.float_scale), (tmp[1] - 100 - self.point_offset[1] ) * self.change_size_num_re * (1/self.float_scale) 
            point_location.append(tmp)
        return point_location
    def cut(self,show_img : bool,shadow : bool) -> Image or None:
        #変形せずにその部分だけ切り取って保存する
        if not (self.check_size_entry()): return
        point_location = self.get_point()
        #point_locationの各要素をtupleに
        point_location = list(map(tuple,point_location))
        #画像を生成し、point_locationの通りに4角形を描画(白黒)
        mask_img = Image.new(mode="L",size=self.now_picture.size,color=(0))
        draw = ImageDraw.Draw(mask_img)
        draw.polygon(point_location,fill=(255))
        #四角形を滑らかにする
        s_pic = Image.new(mode="L",size=(int(self.now_picture.size[0] + 50),int(self.now_picture.size[1] + 50)),color=(0))
        s_pic.paste(mask_img,(25,25))
        s_pic = s_pic.filter(ImageFilter.GaussianBlur(radius=3))
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=3))
        #self.now_imageをmaskする
        after_pic = self.now_picture.copy()
        after_pic.putalpha(mask_img)
        #影が必要なら、生成した画像の右下に影を付ける
        if shadow:
            s_image = Image.new(mode="RGBA",size=(int(after_pic.size[0] + 50),int(after_pic.size[1] + 50)))
            #after_pic[i] * (2/12)の位置に影(mask_imageを貼る)
            sh = Image.eval(s_pic,lambda x : 255 - int(x / 1.5))
            s_image.paste(sh,(0,0),s_pic)
            s_image.paste(after_pic,(0,0),mask_img)
            after_pic = s_image
        #プレビューモードなら生成した画像を見る
        if show_img:
            after_pic.show()
            return
        #そうでなければ画像を返す
        return after_pic
    def affine(self,show_img : bool) -> Image or None:
        """
        変形処理をする
        """
        if not (self.check_size_entry()): return
        point_location = self.get_point()
        quad_data = (
            point_location[0][0], point_location[0][1],   # 左上
            point_location[1][0], point_location[1][1],   # 左下
            point_location[2][0], point_location[2][1],   # 右下
            point_location[3][0], point_location[3][1]    # 右上
            )
        #４点からなる四角形を幅、高さからなる長方形へ変換
        after_pic = self.now_picture.transform(
                    (int(self.save_size_x_entry.get()), int(self.save_size_y_entry.get())),     #出力サイズ(幅, 高さ)
                    Image.QUAD,     #変換方法
                    quad_data,      #４点の座標
                    Image.BICUBIC   #補間方法
                    )
        #プレビューモードなら生成した画像を見る
        if show_img:
            after_pic.show()
            return
        #そうでなければ画像を返す
        return after_pic
    def save(self) -> None:
        """
        画像を保存する関数
        """
        try:
            if self.save_mode.get() == "正方形変換":# 正方形変換
                save_pic = self.affine(show_img=False)
            else:# 範囲切り取り + 影を付けるか否か
                save_pic = self.cut(show_img=False,shadow=(self.save_mode.get() == "形状維持(影)"))
            file_name = filedialog.asksaveasfilename(
                        title = "名前を付けて保存",
                        filetypes= [("PNG", ".png"), ("JPEG", ".jpg"), ("PDF",".pdf"), ("WEBP",".webp"),("ICON",".ico")],
                        initialdir="./",
                        defaultextension = "png"
            )
            save_pic.save(f"{file_name}")
            messagebox.showinfo(title="保存",message=f"保存に成功しました\n保存先：{file_name}")
        except Exception as e:
            print(e)
            messagebox.showerror(title="エラー",message="保存に失敗しました")
    def click(self,event : Event) -> None:
        """
        クリックのみの判定
        これを使用し、前回のものをつかんだままなのかを判定する。
        """
        self.change_flag = True#これがTrueになっているときのみ新しく図形を探索する
        self.click_dat["Point"] = {"x":event.x,"y":event.y}
        self.moving_image = False
    def point_move(self,event : Event) -> None:#クリック＆移動検知
        """
        点の移動を行う関数
        又は、どの点も操作しない場合画像自体を動かす
        """
        def image_move() -> None:
            #TODO 点の位置を動かさないなら画像を動かす
            #現在のメイン画像の座標をgetする
            self.moving_image = True
            x , y = self.master.coords("main_img")
            move_x, move_y = self.click_dat["Point"]["x"] - event.x , self.click_dat["Point"]["y"] - event.y
            self.master.moveto("main_img",x - move_x,y - move_y)
            self.point_offset[0] -= move_x
            self.point_offset[1] -= move_y
            self.click_dat["Point"] = {"x":event.x,"y":event.y}
            mark_put_list = [[int(self.point_entry_list[i][0].get()),int(self.point_entry_list[i][1].get()), i + 1] for i in range(4)]
            self.marker_format(mark_put_list)
            self.marker_line()
        def move_main(i) -> bool:
            if not self.change_flag:#今回は前回のものを動かすなら
                point_location = self.master.coords(self.bef_move)
                self.move_space = 1000
                c_flag = False
            elif i == None:
                point_location = self.master.find_closest(event.x,event.y)
                c_flag = True
            else:
                point_location = self.master.coords(f"{i + 1}_mark")
                c_flag = True
            if abs(point_location[0] - event.x) <= self.move_space and abs(point_location[1] - event.y) <= self.move_space:#移動確定なら
                self.move_old = i#ここで移動したものを保管しておく
                x , y = event.x -self.point_offset[0] , event.y -self.point_offset[1]#移動するはずの値
                #それぞれ画像をオーバーしているなら動かさない
                if x < 250 - 3:
                    x = 250 - 3
                elif x > 250 + self.picture_window_size[0] - 3:
                    x = 250 + self.picture_window_size[0] - 3
                if y < 100 - 3:
                    y = 100 - 3
                elif y > 100 + self.picture_window_size[1]- 3:
                    y = 100 + self.picture_window_size[1] - 3
                #要は今回つかんでいるのは新しく判定されたものなのか前回と同じなのか
                if c_flag:
                    self.bef_move = f"{i + 1}_mark"
                    self.master.moveto(f"{i + 1}_mark",x + self.point_offset[0],y + self.point_offset[1])
                    self.point_entry_list[i][0]["state"] = "NORMAL"
                    self.point_entry_list[i][1]["state"] = "NORMAL"
                    self.point_entry_list[i][0].delete(0,len(self.point_entry_list[i][0].get()))
                    self.point_entry_list[i][0].insert(0,int((x - 250 + 3) // self.float_scale))
                    self.point_entry_list[i][1].delete(0,len(self.point_entry_list[i][0].get()))
                    self.point_entry_list[i][1].insert(0,int((y - 100 + 3) // self.float_scale))
                    self.point_entry_list[i][0]["state"] = "readonly"
                    self.point_entry_list[i][1]["state"] = "readonly"
                else:
                    self.master.moveto(self.bef_move,x + self.point_offset[0],y + self.point_offset[1])
                    self.point_entry_list[int(self.bef_move[0]) - 1][0]["state"] = "NORMAL"
                    self.point_entry_list[int(self.bef_move[0]) - 1][1]["state"] = "NORMAL"
                    self.point_entry_list[int(self.bef_move[0]) - 1][0].delete(0,len(self.point_entry_list[int(self.bef_move[0]) - 1][0].get()))
                    self.point_entry_list[int(self.bef_move[0]) - 1][0].insert(0,int((x - 250 + 3) // self.float_scale))
                    self.point_entry_list[int(self.bef_move[0]) - 1][1].delete(0,len(self.point_entry_list[int(self.bef_move[0]) - 1][1].get()))
                    self.point_entry_list[int(self.bef_move[0]) - 1][1].insert(0,int((y - 100 + 3) // self.float_scale))
                    self.point_entry_list[int(self.bef_move[0]) - 1][0]["state"] = "readonly"
                    self.point_entry_list[int(self.bef_move[0]) - 1][1]["state"] = "readonly"
                #線を再描写する
                self.marker_line()
                #Trueが返ると今回の処理は終了
                return True
            else : 
                return False
        try:
            self.move_space = 10
            #外からつかんでいる場合はつかめる距離を広くとる
            if event.x < 250 - 3 or event.x > 250 + self.picture_window_size[0] - 3 or event.y < 100 - 3 or event.y > 100 + self.picture_window_size[1] - 3:
                move_main(self.move_old)
            #4本の点に対して
            if not self.moving_image:
                for i in range(4):
                    flag = move_main(i)
                    if flag: 
                        self.change_flag = False
                        return
                    
            image_move()
        except:pass#まだ画像が読まれていない
    def calc_save_size(self,point) -> None:
        self.save_size_x_entry.delete(0,len(self.save_size_x_entry.get()))
        self.save_size_x_entry.insert(0,int(max(abs(point[0][0] - point[2][0]),abs(point[1][0] - point[3][0])) * (1/self.float_scale) * self.change_size_num_re))
        self.save_size_y_entry.delete(0,len(self.save_size_y_entry.get()))
        self.save_size_y_entry.insert(0,int(max(abs(point[0][1] - point[1][1]),abs(point[2][1] - point[3][1])) * (1/self.float_scale) * self.change_size_num_re))
    def marker_line(self) -> None:
        """
        4点を結ぶ線を表示する
        """
        #自身を削除する
        self.master.delete("black_line")
        #ここにそれぞれの点の座標を入れる
        location_list = []
        for i in range(1,5):#1-4まで(それぞれの座標のリストを作る)
            location_list.append(self.master.coords(f"{i}_mark"))
        #線を引く
        for  i in range(4):
            nxt = i + 1 if i < 3 else 0
            self.master.create_line(location_list[i][0],location_list[i][1],
                                    location_list[nxt][0],location_list[nxt][1],tags="black_line")
        
        location_list = [[location_list[i][0] - self.point_offset[0],location_list[i][1] - self.point_offset[1]] for i in range(4)]

        #四角の外側をグレーにする
        self.line_out_img = Image.new(mode="RGBA",size=(self.picture_window_size[0],self.picture_window_size[1]),color=(0,0,0,0))
        self.line_out_draw = ImageDraw.Draw(self.line_out_img)
        self.line_out_draw.polygon(((location_list[0][0] - 250,location_list[0][1] - 100),
                                (location_list[1][0] - 250,location_list[1][1] - 100),
                                (location_list[2][0] - 250,location_list[2][1] - 100),
                                (location_list[3][0] - 250,location_list[3][1] - 100),
                                (location_list[0][0] - 250,location_list[0][1] - 100),
                                (0,0),
                                (0,0 + self.picture_window_size[1]),
                                (0 + self.picture_window_size[0], 0 + self.picture_window_size[1]),
                                (0 + self.picture_window_size[0], 0),
                                (0,0)),
                                fill=(0,0,0,128))
        self.line_out_tk = ImageTk.PhotoImage(self.line_out_img)
        self.master.create_image(250 + self.point_offset[0],100 + self.point_offset[1],image = self.line_out_tk,anchor = NW,tags = "black_line")
        self.master.lower("point_img","background")

        self.master.lower("black_line","point_img")

        self.calc_save_size(location_list)
    def marker_format(self,marker_pin : List[List[int]]) -> None:
        """
        4点を描写する
        """
        self.master.delete("point_img")
        i = 0
        for location in marker_pin:
            #番号を付けておく。またこの点に接する線にも同じタグを付与する事で点と同時に線も削除し、再描写する
            self.master.create_image((location[0]) * self.float_scale + self.point_offset[0] + 250,(location[1]) * self.float_scale + self.point_offset[1] + 100,image = self.marker,tags = (f"{location[2]}_mark","point_img"))
            self.point_entry_list[i][0]["state"] = "NORMAL"
            self.point_entry_list[i][1]["state"] = "NORMAL"
            self.point_entry_list[i][0].delete(0,len(self.point_entry_list[i][0].get()))
            self.point_entry_list[i][0].insert(0,str(location[0]))
            self.point_entry_list[i][1].delete(0,len(self.point_entry_list[i][1].get()))
            self.point_entry_list[i][1].insert(0,str(location[1]))
            self.point_entry_list[i][0]["state"] = "readonly"
            self.point_entry_list[i][1]["state"] = "readonly"
            i += 1
        self.master.lower("point_img","background")
    def change_img(self) -> None:
        #生成した画像をscale倍にする
        self.draw_picture = self.window_picture.resize((int(self.window_picture.size[0] * self.float_scale),int(self.window_picture.size[1] * self.float_scale)))
        try:
            self.bef_change_scale = self.now_size / self.draw_picture.size[0]   # 前回のサイズ/現在のサイズをすることでどれだけ変わったかを保管
        except:pass
        self.now_size = self.draw_picture.size[0]                           # 現在のサイズを更新

        #もし、point[0] < 0 or point[1] < 0 のとき、はみ出ている部分が必要ではないのでトリムする
        point = [self.point_offset[0],self.point_offset[1]]
        # if self.point_offset[0] < 0 or self.point_offset[1] < 0:
        #     #self.draw_pictureをトリミングする
        #     self.draw_picture = self.draw_picture.crop((0 - self.point_offset[0],0 - self.point_offset[1],self.draw_picture.size[0],self.draw_picture.size[1]))
        #     point[0] = 0 if self.point_offset[0] < 0 else self.point_offset[0]
        #     point[1] = 0 if self.point_offset[1] < 0 else self.point_offset[1]
        # if self.draw_picture.size[0] > 500 or self.draw_picture.size[1] > 400: # 画像サイズが大きすぎるとき
        #     #self.draw_pictureをトリミングする
        #     self.draw_picture = self.draw_picture.crop((0,0,500,400))

        #現在のサイズを保管して
        self.picture_window_size = self.draw_picture.size
        #tkinterの形式に変換
        self.draw_picture = ImageTk.PhotoImage(self.draw_picture)
        #画像を表示
        self.master.create_image(point[0] + 250,point[1] + 100,image = self.draw_picture, anchor=NW, tags = "main_img")

        self.master.lower("main_img","background")
    def put_pic_marker(self,path : str,load_image : bool) -> None:
        """
        元画像のサイズの変更を行う
        ここでの変更は最終保存の画質には影響しない
        """
        #画像サイズをリセット
        self.scale = 1000
        self.float_scale = 1
        #offsetリセット
        self.point_offset = [0,0]
        #まずはpictureを生成してセットする
        if not load_image:
            self.now_picture = Image.open(path)
        else:
            self.now_picture = self.camera_save
            self.image_path_entry["state"] = "NORMAL"
            self.image_path_entry.delete(0,len(self.image_path_entry.get()))
            self.image_path_entry.insert(0,"None")
            self.image_path_entry["state"] = "disabled"
        #元々のサイズを格納する(後にウィンドウ上のサイズ/初期サイズを取り、データ上の画像と表示されてる画像の比がずれないようにする)
        self.picture_default_size[0] = self.now_picture.size[0]
        self.picture_default_size[1] = self.now_picture.size[1]
        #保存サイズの初期状態を設定する
        self.save_size_x_entry.delete(0,len(self.save_size_x_entry.get()))
        self.save_size_x_entry.insert(0,self.now_picture.size[0])
        self.save_size_y_entry.delete(0,len(self.save_size_y_entry.get()))
        self.save_size_y_entry.insert(0,self.now_picture.size[1])
        try:
            self.change_point_button["state"] = "enable"
        except:pass
        #ウィンドウ用の画像生成
        if self.picture_default_size[0] * 4 <= self.picture_default_size[1] * 5:
            #ここでは対比に対して縦が大きいので縦に合わせて横のサイズを変更したい(x = ? , y = 500 * (7/9))
            #元のサイズに対しての横のサイズ比を算出(元のサイズを500 * (7 / 9)にしているので)
            self.change_size_num = 500 * (4/5) / self.picture_default_size[1]
            #であればその逆数を掛ければ元のサイズに戻るので
            self.change_size_num_re = self.picture_default_size[1] / (500 * (4/5))
            self.window_picture = self.now_picture.resize((int(500  * (4 / 5) * self.picture_default_size[0] / self.picture_default_size[1]),int(500 * (4 / 5))))
        else:
            self.change_size_num = 500 / self.picture_default_size[0]
            self.change_size_num_re = self.picture_default_size[0] / 500
            self.window_picture = self.now_picture.resize((int(500),int(500 * self.picture_default_size[1] / self.picture_default_size[0])))
        self.change_img()
        #ここからマーカーを((0,0),(0,y_max),(x_max,0),(x_max,y_max))に配置する
        mark_put_list = [[0 , 0 , 1],
                        [0 , 0 + self.picture_window_size[1] , 2],
                        [0 + self.picture_window_size[0] , 0 + self.picture_window_size[1] , 3],
                        [0 + self.picture_window_size[0] , 0 , 4]]
        #点描写関数
        self.marker_format(mark_put_list)
        #線描写関数
        self.marker_line()

    def set_img(self) -> None:
        """
        グリッド画像と左のロゴを生成
        """
        transparent_bg = Image.new(mode="RGB",size=(500,400),color=(0,0,0,255))
        #ここからピクセルの可視化用の画像を作る
        self.pixel_img = Image.new("RGBA",(520 + 10 + 10,int(500 * (4 / 5) + 20 + 10)),(0,0,0,0))
        self.pixel_img_draw = ImageDraw.Draw(self.pixel_img)
        #0だけ斜めの位置に欲しいので
        self.pixel_img_draw.text(xy = (20,10),text="0",fill=(255,255,255,255))
        #x軸
        self.pixel_img_draw.line(xy=((30,20 - 1),(530,20 - 1)),fill=(255,255,255,255))
        for wid_char_place in range(100,600,100):
            self.pixel_img_draw.text(xy = (20 + wid_char_place + 2,0),text=f"{wid_char_place}",fill=(255,255,255,255))
            self.pixel_img_draw.line(xy = ((30 + wid_char_place,10),(30 + wid_char_place,20 - 1)),fill=(255,255,255,255))
        #y軸
        self.pixel_img_draw.line(xy=((30 - 1,20),(30 - 1,420)),fill=(255,255,255,255))
        for hei_char_place in range(100,500,100):
            self.pixel_img_draw.text(xy = (0,10 + hei_char_place + 5),text=f"{hei_char_place}",fill=(255,255,255,255))
            self.pixel_img_draw.line(xy = ((20,20 + hei_char_place),(30 - 1,20 + hei_char_place)),fill=(255,255,255,255))
        self.pixel_img = ImageTk.PhotoImage(self.pixel_img)
        self.master.create_image(250 - 30, 100 - 20,image = self.pixel_img,anchor = NW)
        #縦横20*16の26ピクセル刻みのグリッドを作成
        for grid_x in range(20):#横
            for grid_y in range(16):#縦
                if (grid_x + grid_y) % 2 == 0:
                    color = (128,128,128,255) 
                else:
                    color = (96,96,96,255)
                transparent_bg.paste(Image.new("RGBA",(25,25),color),(grid_x * 25,grid_y * 25))
        #どうやらローカル変数だと参照が消えてGCされてる感じなのでself.
        self.transparent_bg_tk = ImageTk.PhotoImage(transparent_bg)
        self.master.create_image(250,100,image = self.transparent_bg_tk,anchor = NW)

        #背景を作る
        self.back_image = Image.new("RGBA",(900,700),(64,64,64,255))
        #ピクセルの可視化用画像を置く部分(x = 250 ~ 750, y = 100 ~ 500)を透明にする
        transparent_bg = Image.new(mode="RGBA",size=(500,400),color=(0,0,0,0))
        self.back_image.paste(transparent_bg,(250,100))
        self.back_image_tk = ImageTk.PhotoImage(self.back_image)
        self.master.create_image(0,0,image = self.back_image_tk , anchor = NW, tag = "background")

        #ロゴ読み込み
        self.logo = PhotoImage(file = "./assets/picture/logo_gradation.png")
        self.master.create_image(-50,0,image = self.logo,anchor = NW)

    def set_obj(self) -> None:
        """
        初期から置かれているボタン等を設置
        """
        def view_image(show_bool : bool):
            def tmp():
                af = self.save_mode.get() == "正方形変換"
                if af:
                    self.affine(show_bool)
                else:
                    self.cut(show_bool,self.save_mode.get() == "形状維持(影)")
            return tmp
        def make_marker() -> PhotoImage:
            """
            マーカーの画像を返す
            """
            image = ImageTk.PhotoImage(self.marker)
            return image
        def file_reference() -> None:
            """
            ファイル参照処理
            """
            path = filedialog.askopenfilename(filetypes=[("Image", "*.png;*.jpg;*.webp;*.ico")])
            if path == "":
                pass
            else:
                self.image_path_entry["state"] = "NORMAL"
                self.image_path_entry.delete(0,len(self.image_path_entry.get()))
                self.image_path_entry.insert(0,path)
                self.image_path_entry["state"] = "disabled"
                self.put_pic_marker(path,False)
        self.marker = make_marker()
        self.master.create_text(250,30 + 4,text="参照path",fill="white",tags="reference_path",anchor=N)
        self.image_path_entry = ttk.Entry(width=80, state='disabled')
        self.image_path_entry.place(relx=300/self.win_dat["width"],rely=30/self.win_dat["height"],relheight=0.04)
        self.reference_path_button = ttk.Button(text="参照",command=file_reference)
        self.reference_path_button.place(relx = 800/self.win_dat["width"] , rely = (30 - 2)/self.win_dat["height"],relheight=0.04)
        self.save_button = ttk.Button(text="保存",command=self.save)
        self.save_button.place(relx = 840/self.win_dat["width"] , rely = 450/self.win_dat["height"],relheight=0.04,relwidth=0.06)
        self.preview_button = ttk.Button(text="プレビュー",command=view_image(True))
        self.preview_button.place(relx = 840/self.win_dat["width"] , rely = 420/self.win_dat["height"],relheight=0.04,relwidth=0.06)
        self.master.create_text(800,300,text="保存サイズ",fill="white",anchor=NW)
        self.master.create_text(800,330,text="x",fill="white",anchor=NW)
        self.save_size_x_entry = ttk.Entry(width=5)
        self.save_size_x_entry.place(relx = 820/self.win_dat["width"],rely = 330/self.win_dat["height"],relheight=0.04)
        self.master.create_text(800,350,text="y",fill="white",anchor=NW)
        self.save_size_y_entry = ttk.Entry(width=5)
        self.save_size_y_entry.place(relx = 820/self.win_dat["width"],rely = 350/self.win_dat["height"],relheight=0.04)
        self.point_entry_list = [[ttk.Entry(width=3),ttk.Entry(width=3)],
                                [ttk.Entry(width=3),ttk.Entry(width=3)],
                                [ttk.Entry(width=3),ttk.Entry(width=3)],
                                [ttk.Entry(width=3),ttk.Entry(width=3)]]
        self.master.create_text(830 + 10, 170 - 20,text=f"x",fill="white",anchor = NW)
        self.master.create_text(850 + 10, 170 - 20,text=f"y",fill="white",anchor = NW)
        for i in range(len(self.point_entry_list)):
            self.master.create_text(800, 170 + 7 + (i * 20),text=f"point{i + 1}",fill="white",anchor = CENTER)
            for j in range(len(self.point_entry_list[i])):
                self.point_entry_list[i][j].place(relx = (830 + (j * 25))/self.win_dat["width"], rely = (170 + (i * 20))/self.win_dat["height"],relheight=0.04)
                self.point_entry_list[i][j]["state"] = "readonly"
        self.change_point_button = ttk.Button(text="座標変更",width=8,command=self.sub_win_bef(self.point_entry_list))
        self.change_point_button.place(relx=822/self.win_dat["width"],rely=260/self.win_dat["height"],relheight=0.04)
        self.change_point_button["state"] = "disable"
        self.master.create_text(835 ,70 , text="または",fill="white")
        self.app_camera_button = ttk.Button(text="写真を撮る",command = self.camera_win)
        self.app_camera_button.place(relx = 800/self.win_dat["width"],rely = 90/self.win_dat["height"],relheight=0.04)
        self.save_mode = ttk.Combobox(values=["正方形変換","形状維持","形状維持(影)"],state="readonly")
        self.save_mode.current(0)
        self.save_mode.place(relx = 760/self.win_dat["width"],rely = 450/self.win_dat["height"],relheight=0.04,relwidth=0.08)

    def control_click(self,event):
        bef = [self.scale, self.float_scale]
        if event.delta > 0:
            self.scale += 50 if self.scale < 3000 else 0
        else:
            self.scale -= 50 if self.scale > 50 else 0
        self.float_scale = self.scale / 1000
        #再描写
        try:
            self.change_img()
            #点描写関数
            mark_put_list = [[int(self.point_entry_list[i][0].get()),int(self.point_entry_list[i][1].get()), i + 1] for i in range(4)]
            self.marker_format(mark_put_list)
            #線描写関数
            self.marker_line()
        except Exception as e:# まだ画像が読み込まれてないなら
            print(e)
            [self.scale, self.float_scale] = bef
    def bind(self) -> None:
        """
        ドラッグ操作とクリックをバインド
        """
        # 点を動かす
        self.master.bind("<Button1-Motion>",self.point_move)
        # クリック
        self.master.bind("<Button-1>",self.click)
        # コントロール + スクロールで画像の拡大縮小
        self.master.bind("<Control-MouseWheel>",self.control_click)


    def main(self) -> None:
        """
        windowを生成し、各種処理を開始する
        """
        self.root = Tk()
        self.root.geometry("900x600")
        self.root.title("image deformation")
        # self.root.resizable(0,0)
        self.root.iconbitmap("./assets/icon/mi.ico")
        self.master = Canvas(self.root,width=900,height=600)
        self.master.place(relx=0,rely=0,relwidth=1,relheight=1)
        self.bind()
        self.set_img()
        self.set_obj()
        self.master.mainloop()


if __name__ == "__main__":
    main_instance = main()
    main_instance.main()