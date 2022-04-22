import argparse
import os
import struct
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import Menu
import cv2
from PIL import Image, ImageTk # 将图片转化为二进制数据
from tools import test_net_single_image

class MainWindows(tk.Tk):
    def __init__(self):
        super().__init__()  # 初始化基类

        self.title("三维重建系统")
        self.resizable(width=True, height=True) #是否可变窗口大小
        self.geometry("1024x768")
        # self.minsize(640, 320)
        self.tabControl = ttk.Notebook(self)  # Create Tab Control
        self.tab1 = ttk.Frame(self.tabControl)  # Create a tab
        self.menu_bar = Menu(self)  # Creating a Menu Bar

        self.init_ui()

        self.selected_files = []  # 被选中的文件，获取识别结果被使用
        self.photo_libs = []  # 本地图片库
        self.feature_libs = []  # 本地特征向量库
        self.lib_path = './images/libs'  # 本地库文件路径


    def init_ui(self):

        self.tabControl.add(self.tab1, text='选择图片')  # Add the tab
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

        self.init_tab1()

        self.config(menu=self.menu_bar)
        self.init_menu()

    def init_tab1(self):
        mighty = ttk.Frame(self.tab1)
        mighty.pack()
        self.label1 = tk.Label(mighty, text='检测图片',font=('Noto Sans CJK SC Black',10), bg="Silver", padx=15, pady=15)
        # self.label2 = tk.Label(mighty, text='检测图片2', bg="Silver", padx=15, pady=15)
        self.label1.grid(column=0, row=0, sticky='WN')
        # cself.label2.grid(column=1, row=0, sticky='W')
        btn1 = ttk.Button(mighty, text="选择文件", command=self.select_btn_tab1, width=15)
        btn2 = ttk.Button(mighty, text="获取结果", command=self.get_result1, width=15)

        btn1.grid(column=0, row=1, sticky='W')
        btn2.grid(column=0, row=2, sticky='W')
        label3 = tk.Label(mighty, text='相似度(一般70%以上可以表示为同一个人):')
        label3.grid(column=0, row=3, sticky='W')
        self.name = tk.StringVar()
        name_entered = ttk.Entry(mighty, width=12, textvariable=self.name)
        name_entered.grid(column=1, row=3, sticky='W')  # align left/West



    def init_menu(self):
        # Add menu items
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add another Menu to the Menu Bar and an item
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def show_img(self, labels, filename, length=1):
        if len(filename) < 1:
            return
        for i in range(length):
            img = Image.open(filename[i])
            half_size = (256,256)
            img.thumbnail(half_size, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            labels[i].configure(image=photo)
            labels[i].image = photo

    def select_file(self):
        self.selected_files = []
        ftypes = [('Image Files', '*.tif *.jpg *.png')]
        dlg = filedialog.Open(filetypes=ftypes, multiple=True)
        filename = dlg.show()
        self.selected_files = filename
        return filename

    def select_btn_tab1(self):
        self.show_img([self.label1], self.select_file())

    def get_result1(self):

        img_path = self.selected_files[0]

        print(1)
        parser = argparse.ArgumentParser()
        # parser.add_argument("--input", "-i", type=str, default="data/front3d-sample/test19.jpg")
        parser.add_argument("--input", "-i", type=str, default= img_path)
        parser.add_argument("--output", "-o", type=str, default="output/sample_0020/")
        parser.add_argument("--config-file", "-c", type=str, default="configs/front3d_sample.yaml")
        parser.add_argument("--model", "-m", type=str, default="data/panoptic_front3d_v2.pth")
        parser.add_argument("opts", default=None, nargs=argparse.REMAINDER)

        args = parser.parse_args()
        test_net_single_image.main(args)



        # # 计算两张图片的余弦相似度
        # res = self.face_recog.cos_sim(v1, v2).tolist()[0][0]
        # res = format(res * 100, '.2f')
        # self.name.set(res + '%')

    def select_btn_tab2(self):
        self.show_img([self.label_rec], self.select_file())




    def _quit(self):
        self.quit()
        self.destroy()
        exit()


if __name__ == '__main__':
    app = MainWindows()
    app.mainloop()