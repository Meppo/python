#!/usr/bin/python3

#
# 生成签名工具 [页面]类
#   d = MyBuildSignToolWin(title)
#     使用了 MyAddNewModelDialog(title)类用来增加新的秘钥
#
# 包含功能:
#   1) 现有秘钥的显示(所属型号,插件中心)， 秘钥的增加/删除功能
#   2）使用秘钥生成指定的签名工具，包括临时，正式签名工具
#   3) 将生成的工具加到本机工具列表, 供"插件签名"功能页面使用
#
# 注: 具体秘钥增/删/显示功能实现在 sign_key 包中
#     具体生成签名工具功能实现在 build_sign_tool 包中
#

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil
import datetime

# 自定义模块
import main_view as v_main
import build_sign_tool as bst
import sign_opk_view as v_so
import sign_key
import config

bst_win_txt = "生成签名工具"
bst_func_menu_txt = "功能"
add_model_txt = "添加新秘钥"
del_model_txt = "删除"
add_model_win_txt = "添加新秘钥"
select_key_txt = "选择密钥"
add_txt = "确定"
cancel_txt = "取消"
bst_gen_txt = "生成"
bst_exit_txt = "退出"
clean_txt = "清除"
save_txt = "工具另存为"
add_local_txt = "添加到本地工具列表"
list_frame_txt = "选择指定(型号,插件中心)所属秘钥"
main_frame_txt = "插件相关信息"
detail_frame_txt = "执行详细"
sign_author_hint = " valid value:\n \
      0:temp 1:ifenglian 3:netcore\n \
      4~100:reserve\n \
      101~1000:360's developer\n \
      1001~2000:ifenglian's developer\n \
      2001~3000:netcore's developer\n \
      3001~5000:reserve\n"

class MyAddNewModelDialog(tk.Toplevel):

    def __init__(self, parent, title=None):
        """ 在传入的父窗口上画"添加新型号/插件中心"页面 """

        # 主窗口
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None
        self.key_path = ""

        # 开始画内容
        self.model = tk.StringVar(self)
        lb = tk.Label(self, text="型号:")
        lb.grid(row=0, column=0, padx=10, pady=5)
        self.model_e = tk.Entry(self, textvariable=self.model)
        self.model_e.grid(row=0, column=1, pady=5)

        self.app_center = tk.StringVar(self)
        lb = tk.Label(self, text="插件中心:")
        lb.grid(row=0, column=2, padx=10, pady=5)
        self.app_center_e = tk.Entry(self, textvariable=self.app_center)
        self.app_center_e.grid(row=0, column=3, pady=5)

        self.key_name = tk.StringVar(self)
        lb = tk.Label(self, text="密钥:")
        lb.grid(row=1, padx=10, pady=5)
        self.key_e = tk.Entry(self, textvariable=self.key_name, state='readonly')
        self.key_e.grid(row=1, column=1, pady=5)

        tk.Button(self,
                  text=select_key_txt,
                  justify=tk.CENTER,
                  command=self.select_key).grid(row=1, column=2, padx=10, pady=5)

        btn = tk.Button(self,
                  text=add_txt,
                  justify=tk.CENTER,
                  command=self.add_new_item, default=tk.ACTIVE)
        btn.grid(row=2, column=1, padx=10, pady=5, sticky=tk.E)

        tk.Button(self,
                  text=cancel_txt,
                  justify=tk.CENTER,
                  command=self.cancel_add).grid(row=2, column=2, padx=10, pady=5)

        # 绑定Enter 和 Escape键
        self.bind("<Return>", self.add_new_item)
        self.bind("<Escape>", self.cancel_add)

        # make the dialog modal?
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.cancel_add)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.model_e.focus()

        self.wait_window(self)

    def select_key(self):
        """ "选择"秘钥按钮 执行函数 """

        self.key_path = filedialog.askopenfilename(master=self)
        print(self.key_path)
        self.key_name.set(os.path.basename(self.key_path))

    def add_new_item(self, event=None):
        """ "确定"按钮执行动作函数 """

        print ("click the add button!" )
        model = self.model_e.get()
        app_center = self.app_center_e.get()
        print ("all value: model:%s appcenter:%s key_path:%s " 
                % (model, app_center, self.key_path))
        if not model:
            self.model_e.focus()
            messagebox.showerror("Error", "型号不能为空", parent=self)
            return False
        if not app_center:
            self.app_center_e.focus()
            messagebox.showerror("Error", "插件中心不能为空", parent=self)
            return False
        if not self.key_path:
            self.key_e.focus()
            messagebox.showerror("Error", "必须选择密钥文件", parent=self)
            return False

        msg = "型号: %s\n插件中心: %s\n秘钥: %s\n" % (model, app_center, os.path.basename(self.key_path))
        if not messagebox.askyesno("添加确认", "秘钥相关信息:\n" + msg + "\n" + "确定添加?", parent=self):
            return False

        res = sign_key.add_new_key(model, app_center, self.key_path)
        if not res:
            self.model_e.focus()
            messagebox.showerror("Error", "添加新的型号,插件中心失败!", parent=self)
            return False

        messagebox.showinfo("添加成功", msg, parent=self)

        self.cancel_add()
        return True

    def cancel_add(self, event=None):
        """ "取消"按钮执行动作函数 """

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()


def is_not_null(i):
    if not i:
        return False

    return True


class MyBuildSignToolWin(tk.Tk):

    def __init__(self, title):
        """ 在传入的父窗口上画"生成签名工具"页面 """

        # 其他成员
        # 用于生成工具的事件定时器ID

        # 主窗口
        tk.Tk.__init__(self)
        self.title(title)
        self.update()

        self.gen_id = ""
        self.target_path = ""

        # 设置窗口居中
        v_main.just_center_window(self)

        # 创建主菜单
        menubar = tk.Menu(self)

        # 创建功能子菜单
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=bst_exit_txt, command=self.m_quit)

        # 加入子菜单
        menubar.add_cascade(label=bst_func_menu_txt, menu=filemenu)

        # 画菜单
        self.config(menu=menubar)

        # 已有的KEY
        list_frame = tk.Frame(self)
        list_frame  = tk.LabelFrame(self, text=list_frame_txt, padx=5, pady=5)
        list_frame.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        self.list_b = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.flush_list_b()
        self.list_b.bind("<ButtonRelease-1>", self.chosen)
        self.list_b.grid(column=0, sticky=tk.W+tk.E)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.config(command=self.list_b .yview)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

        tk.Button(list_frame,
                  text=add_model_txt,
                  justify=tk.CENTER,
                  command=self.add_new_model).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(list_frame,
                  text=del_model_txt,
                  justify=tk.CENTER,
                  command=self.del_model).grid(row=1, column=1, padx=10, pady=5)


        self.main_frame  = tk.LabelFrame(self, text=main_frame_txt, padx=5, pady=5)
        self.main_frame.grid(sticky=tk.W+tk.E+tk.N+tk.S)


        m_row = 0
        m_col = 0
        self.model = tk.StringVar(self)
        lb = tk.Label(self.main_frame, text="型号:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.model_e = tk.Entry(self.main_frame, textvariable=self.model, state='readonly')
        self.model_e.grid(row=m_row, column=m_col, pady=5)

        m_col += 1
        self.app_center = tk.StringVar(self)
        lb = tk.Label(self.main_frame, text="插件中心:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.app_center_e = tk.Entry(self.main_frame, textvariable=self.app_center, state='readonly')
        self.app_center_e.grid(row=m_row, column=m_col, padx=1, pady=5)

        m_row += 1 
        m_col = 0
        self.app_sign = tk.StringVar(self)
        self.app_sign.set("airlink_app")
        lb = tk.Label(self.main_frame, text="插件名称:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.app_sign_e = tk.Entry(self.main_frame, textvariable=self.app_sign)
        self.app_sign_e.grid(row=m_row, column=m_col, padx=1, pady=5)

        m_col += 1
        self.author = tk.StringVar(self)
        self.author.set("xxx")
        lb = tk.Label(self.main_frame, text="作者:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1

        self.author_e = tk.Entry(self.main_frame, textvariable=self.author)
        self.author_e.grid(row=m_row, column=m_col, padx=1, pady=5)

        m_row += 1 
        m_col = 0
        self.sign_author = tk.StringVar(self)
        self.sign_author.set("0")
        lb = tk.Label(self.main_frame, text="插件签发者:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.sign_author_e = tk.Entry(self.main_frame, textvariable=self.sign_author)
        self.sign_author_e.grid(row=m_row, column=m_col, padx=1, pady=5)

        m_col += 1
        tk.Button(self.main_frame, text="签发者?", justify=tk.CENTER,
                  command=self.show_sign_author_help).grid(row=m_row, column=m_col,
                                              padx=10, pady=5)


        m_row += 1 
        m_col = 1
        tk.Button(self.main_frame,
                  text=bst_gen_txt,
                  justify=tk.CENTER,
                  background="green",
                  command=self.gen_sign_tool).grid(row=m_row, column=m_col,
                                              padx=10, pady=5)

        m_col += 1
        tk.Button(self.main_frame,
                  text=clean_txt,
                  justify=tk.CENTER,
                  command=self.clean_entry).grid(row=m_row, column=m_col,
                                             padx=10, pady=5)

        m_col += 1
        tk.Button(self.main_frame,
                  text=bst_exit_txt,
                  justify=tk.CENTER,
                  command=self.m_quit).grid(row=m_row, column=m_col,
                                             padx=10, pady=5)

        self.detail_frame = tk.LabelFrame(self, text=detail_frame_txt, padx=5, pady=5)
        self.detail_frame.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        self.detail = tk.Text(self.detail_frame)
        self.detail.insert(tk.INSERT, "生成工具执行结果将输出在这里...")
        self.detail.grid(pady=5, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        self.detail.config(state=tk.DISABLED)

        m_row = 1
        m_col = 0
        self.tar_name = tk.StringVar(self)
        lb = tk.Label(self.detail_frame, text="生成的签名工具:")
        lb.grid(row=m_row, padx=10, pady=5, sticky=tk.W)
        m_col += 1
        self.tar_name_e = tk.Entry(self.detail_frame, textvariable=self.tar_name, state='readonly',)
        self.tar_name_e.grid(row=m_row, padx=1, pady=5, sticky=tk.E)

        m_row += 1
        m_col = 0
        tk.Button(self.detail_frame,
                  text=save_txt,
                  justify=tk.CENTER,
                  command=self.save_sign_tool).grid(row=m_row, column=m_col
                                                    ,padx=10, pady=5)

        m_col += 1
        tk.Button(self.detail_frame,
                  text=add_local_txt,
                  justify=tk.CENTER,
                  command=self.add_tool).grid(row=m_row, column=m_col
                                              ,padx=10, pady=5)

        # 绑定Enter 和 Escape键
        self.bind("<Return>", self.gen_sign_tool)
        self.bind("<Escape>", self.m_quit)

        # make the dialog modal?
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.m_quit)

        self.model_e.focus()

        self.mainloop()

    def flush_list_b(self):
        """ 刷新秘钥列表函数 """

        self.list_b.delete(0, tk.END)
        for line in sign_key.get_all_keys():
            item = "%-10s %-10s" % (line[0], line[1])
            self.list_b.insert(tk.END, item)

    def del_model(self):
        """ "删除秘钥" 按钮执行函数 """
        select = self.list_b.curselection()
        if not select:
            return False

        index = select[0]
        item = self.list_b.get(index)
        item_list = list(filter(is_not_null, item.split(" ")))
        self.model.set(item_list[0])
        self.app_center.set(item_list[1])

        msg = "型号:%s\n插件中心:%s\n" % (item_list[0], item_list[1])
        if not messagebox.askyesno("删除确认", "秘钥相关信息:\n" + msg + "\n" + "确定删除?", parent=self):
            return False

        result = sign_key.del_key(item_list[0], item_list[1])
        if not result:
            messagebox.showerror("删除失败", msg, parent=self)
        else:
            messagebox.showinfo("删除成功", msg, parent=self)
            self.flush_list_b()

        return True


    def add_new_model(self, event=None):
        """ "添加秘钥" 按钮执行函数 """

        d = MyAddNewModelDialog(self, add_model_win_txt)

        self.flush_list_b()


    def save_sign_tool(self):
        """ "另存为" 按钮执行函数 """

        if not self.target_path:
            return False

        t_path = filedialog.asksaveasfilename(master=self, title="签名工具另存为",\
                                                initialfile=self.tar_name_e.get(), 
                                                initialdir=config.get_tmp_config("global", "tool_save_path"))
        if not t_path:
            return False
        # 保存用户 常用的另存为路径
        config.save_tmp_config("global", "tool_save_path", os.path.dirname(t_path))

        print ("copy %s => %s" % (self.target_path, t_path))
        try:
            msg = "保存地址:%s" % t_path
            res = shutil.copy(self.target_path, t_path)
            messagebox.showinfo(
                "保存成功", msg, parent=self)
        except:
            msg = "从%s拷贝到%s失败." % (self.target_path, t_path)
            messagebox.showerror(
                "保存失败", msg, parent=self)

    def valid_check(self):
        """ 检查输入框中的值是否正确 """

        model = self.model_e.get()
        app_center = self.app_center_e.get()
        app_sign = self.app_sign_e.get()
        author = self.author_e.get()
        sign_author = self.sign_author_e.get()
        print ("all value: model:%s appcenter:%s appsign:%s author:%s sign_author:%s " 
                % (model, app_center, app_sign, author, sign_author))
        if not model:
            self.list_b.focus()
            messagebox.showerror("Error", "型号不能为空", parent=self)
            return False
        if not app_center:
            self.list_b.focus()
            messagebox.showerror("Error", "插件中心不能为空", parent=self)
            return False
        if not app_sign:
            self.app_sign_e.focus()
            messagebox.showerror("Error", "插件名不能为空", parent=self)
            return False
        if not author:
            self.author_e.focus()
            messagebox.showerror("Error", "插件作者不能为空", parent=self)
            return False
        if not sign_author:
            self.sign_author_e.focus()
            messagebox.showerror("Error", "插件签发者不能为空", parent=self)
            return False
        else:
            sign_a = int(sign_author)
            if int(sign_author) < 0 or int(sign_author) > 5000:
                messagebox.showerror("Error", "插件签发者值错误!\n" + sign_author_hint, parent=self)
                return False

        return True

    def add_tool(self):
        """ "签名工具加入本地工具列表" 按钮执行函数 """

        if not self.tar_name_e.get():
            return False

        if not self.valid_check():
            return False

        sign_author = self.sign_author_e.get()
        if sign_author == "0":
            expire_time = (datetime.datetime.now() + datetime.timedelta(days = 30)).strftime("%Y-%m-%d")
        else:
            expire_time = "2030-01-01"

        d = v_so.MyAddNewToolialog(self, "添加签名工具",\
                m=self.model_e.get(), c=self.app_center_e.get(), s=self.app_sign_e.get(),\
                t=expire_time, p=self.target_path)

    def chosen(self, e):
        """ "秘钥(插件/插件中心)列表" 鼠标单击动作函数 """

        select = self.list_b.curselection()
        if not select:
            return False

        index = select[0]
        item = self.list_b.get(index)
        item_list = list(filter(is_not_null, item.split(" ")))
        self.model.set(item_list[0])
        self.app_center.set(item_list[1])

    def show_sign_author_help(self):
        """ "插件者?"按钮执行动作函数 """

        messagebox.showinfo(
            "sign author", sign_author_hint, parent=self)

    def clean_entry(self):
        """ 清除所有输入框 """

        self.model.set("")
        self.app_center.set("")
        self.app_sign.set("")
        self.author.set("")
        self.sign_author.set("")


    def __disable_all_widget(self):
        """ 禁用所有的主要组件，排除"退出"组件 """

        for w in self.main_frame.winfo_children():
            value = w.cget("text")
            if value != bst_exit_txt:
                w.config(state=tk.DISABLED)

    def __enable_all_widget(self):
        """ 还原禁用的主要组件 """

        for w in self.main_frame.winfo_children():
            value = w.cget("text")
            if value != bst_exit_txt:
                w.config(state=tk.NORMAL)

        self.model_e.config(state='readonly')
        self.app_center_e .config(state='readonly')


    def __gen_sign_tool(self):
        """ 生成插件工具实现函数 """

        print("do real gen sign_tool in alarm")

        model = self.model_e.get()
        app_center = self.app_center_e.get()
        app_sign = self.app_sign_e.get()
        author = self.author_e.get()
        sign_author = self.sign_author_e.get()

        var_list = []
        var_list.append(model)
        var_list.append(app_center)
        var_list.append(app_sign)
        var_list.append(author)
        var_list.append(sign_author)

        state, target, output = bst.build_sign_tool(var_list)

        print ("after do sign_tool")

        msg = "型号: %s\n插件中心: %s\n插件名称: %s\n作者: %s\n签发者: %s\n" %\
                (model, app_center, app_sign, author, sign_author)

        self.detail.config(state=tk.NORMAL)
        self.detail.delete(1.0, tk.END)
        if state == 0:
            if target:
                self.target_path = target
                self.tar_name.set(os.path.basename(target))
            self.detail.insert(tk.END, output)
        else:
            self.detail.insert(tk.END, "工具信息:\n" + msg + "\n")
            self.detail.insert(tk.END, "执行结果:\n生成插件失败\n 错误代码:%d\n 错误描述:%s\n"\
                               % (state, output))
        self.detail.config(state=tk.DISABLED)

        if state == 0:
            messagebox.showinfo("生成工具成功", msg + "签名工具: %s\n"%os.path.basename(target), parent=self)
        else:
            messagebox.showerror("生成工具失败", msg, parent=self)

        self.__enable_all_widget()

    def gen_sign_tool(self, event=None):
        """ "生成"按钮执行动作函数 """

        print ("click the gen button!" )

        if not self.valid_check():
            return False

        msg = "型号: %s\n插件中心: %s\n插件名称: %s\n作者: %s\n签发者: %s\n" %\
                (self.model_e.get(), self.app_center_e.get(), \
                 self.app_sign_e.get(), self.author_e.get(), self.sign_author_e.get())

        if not messagebox.askyesno("生成工具确认", "工具相关信息:\n" + msg + "\n" + "确定生成?", parent=self):
            return False

        print("good!")

        self.__disable_all_widget()

        self.gen_id = self.after(100, self.__gen_sign_tool)
        return True

    def m_quit(self, event=None):
        """ "退出"按钮执行动作函数 """

        print ("click the quit button!")
        if self.gen_id: 
            self.after_cancel(self.gen_id)
        self.destroy()

def test():
    d = MyBuildSignToolWin(bst_win_txt)


if __name__ == '__main__':
    test()
