#!/usr/bin/python3

#
# 主界面 [页面]类
#   d = MyMainWin(title, width, height)
#
# 包含功能:
#   1) 包含 "生成签名工具" 和 "插件签名" 两个功能入口
#
# 注: 生成签名工具 在build_sign_tool_view 包中
#     插件签名  在sign_opk_view 包中
#

import tkinter as tk
from tkinter import messagebox
import build_sign_tool_view as v_bst
import sign_opk_view as v_so
import main_view as v_main

# 全局变量
win_txt = "签名工具"
default_win_width = 700
default_win_height = 600
bst_txt = "生成签名工具"
so_txt = "插件签名"
exit_txt = "退出"
help_txt = "帮助"
about_txt = "关于..."
func_menu_txt = "功能"
help_menu_txt = "帮助"


class MyMainWin(tk.Tk):
    """ "签名工具"主界面 
        TODO: 窗口可变化 可拖放, 按钮设置图像背景
    """

    def __init__(self, title, win_width, win_height):
        """ 初始化"签名工具"页面 """

        # 主窗口
        tk.Tk.__init__(self)
        self.title(title)
        self.update()

        self.win_width = win_width
        self.win_height = win_height

        # 设置主窗口居中和最大尺寸
        v_main.center_window(self, self.win_width, self.win_height)

        # 创建主菜单
        menubar = tk.Menu(self)

        # 创建功能子菜单
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=bst_txt, command=self.show_build_sign_tool_win)
        filemenu.add_command(label=so_txt, command=self.show_sign_opk_view)
        filemenu.add_separator()
        filemenu.add_command(label=exit_txt, command=self.quit)

        # 帮助子菜单
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label=help_txt, command=self.help_usgae)
        helpmenu.add_command(label=about_txt, command=self.about_usgae)

        # 加入子菜单
        menubar.add_cascade(label=func_menu_txt, menu=filemenu)
        menubar.add_cascade(label=help_menu_txt, menu=helpmenu)

        # 画菜单
        self.config(menu=menubar)

        # 画主功能界面
        my_canvas = v_main.show_backgroud(self, (self.win_width, self.win_height))

        # FIXME: 需要使用图片, 因使用相对长宽
        # 生成主界面按钮
        build_sign_tool_btn = tk.Button(my_canvas,
                                        text=bst_txt,
                                        width=50,
                                        command=self.show_build_sign_tool_win)
        sign_opk_btn = tk.Button(my_canvas,
                                 text=so_txt,
                                 width=50,
                                 command=self.show_sign_opk_view)

        # 画按钮
        build_sign_tool_btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        sign_opk_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # 绑定Enter 和 Escape键
        self.bind("<Return>", self.show_build_sign_tool_win)
        self.bind("<Escape>", self.m_quit)

        # make the dialog modal?
        # self.grab_set()

        self.focus()

        self.protocol("WM_DELETE_WINDOW", self.m_quit)

        # 显示并开始循环
        self.mainloop()

    def m_quit(self, event=None):
        """调用"退出"执行动作"""

        print("click the main win quit")
        self.destroy()

    def show_build_sign_tool_win(self, event=None):
        """调用"生成签名工具"功能函数显示功能页面"""

        print("click show build sign tool window")
        d = v_bst.MyBuildSignToolWin("生成签名工具")

    def show_sign_opk_view(self, event=None):
        """调用"插件签名"功能函数显示功能页面"""

        print("click show sign opk window")
        d = v_so.MySignOpkWin("插件签名工具")


    def help_usgae(self):
        """帮助页"""

        messagebox.showinfo("帮助", "选择功能后,请按照界面操作.")


    def about_usgae(self):
        """关于页"""

        messagebox.showinfo("关于", "这是一个方便OPK签名的小程序.")



if __name__ == '__main__':

    d = MyMainWin(win_txt, default_win_width, default_win_height)
