#!/usr/bin/python3

#
# 界面操作函数
#   修改窗口大小并居中: center_window(root, width, height):
#   根据给的窗口大小画背景: show_backgroud(app, size) 
#   背景图片: image/my_bg.GIF 
#
# 包含功能:
#   1) 包含 "生成签名工具" 和 "插件签名" 两个功能入口
#
# 注: 生成签名工具 在build_sign_tool_view 包中
#     插件签名  在sign_opk_view 包中
#

import tkinter as tk
from PIL import Image
import os

# 全局变量
cache_path = os.path.join(os.getcwd(), ".cache")
default_bg_file = os.path.join(os.getcwd(), "image", "my_bg.GIF")

def get_screen_size(window):
    """获取屏蔽的宽度，高度"""

    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    """获取指定窗口的宽度，高度"""

    window.update_idletasks()
    return window.winfo_width(), window.winfo_height()


def just_center_window(root):
    size = get_window_size(root)
    width = size[0]
    height = size[1]
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


def get_resize_photo(size):
    """根据指定的宽和高得到相应缩放后的背景图片."""

    tmp_bg_photo_file = cache_path + "/" + "bg_photo_resize.png"
    default_bg_photo = Image.open(default_bg_file)
    bg_photo_resize = default_bg_photo.resize(size, Image.ANTIALIAS)
    bg_photo_resize.save(tmp_bg_photo_file)
    print("return resize photo %s" % tmp_bg_photo_file)
    return tk.PhotoImage(file=tmp_bg_photo_file)


def show_backgroud(app, size):
    """重画背景 返回背景画布对象"""

    # 必须使用全局的bg_photo, 不然会导致函数退出后背景图片显示不出来
    global bg_photo
    bg_photo = get_resize_photo(size)

    # 画背景图片
    win_width = size[0]
    win_height = size[1]
    app.wm_maxsize(win_width, win_height)
    my_canvas = tk.Canvas(app, width=win_width, height=win_height)
    my_canvas.pack()
    my_canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
    return my_canvas
