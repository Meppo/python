#!/usr/bin/python3

#
# 插件签名 [页面]类
#   d = MySignOpkWin(title)
#     使用了 MyAddNewToolialog(title)类用来增加新的签名工具
#
#   注: 每个签名工具 只能针对指定型号，插件中心，插件来一对一签名, 不能一对多.
#
# 包含功能:
#   1) 现有签名工具的显示(所属型号,插件中心,支持签名的插件名字,到期时间)， 签名工具的增加/删除功能
#   2）使用签名工具对指针插件进行签名
#   3) 提供签名后工具"另存为"功能
#
# 注: 具体签名工具增/删/显示功能实现在 sign_tool 包中
#     具体给插件签名功能实现在 sign_opk 包中
#

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import main_view as v_main
import sign_tool
import sign_opk
import os
import shutil
import datetime

sign_win_txt = "插件签名工具"
sign_exit_txt = "退出"
sign_func_menu_txt = "功能"
list_frame_txt = "签名工具列表"
detail_frame_txt = "执行详细"
add_tool_txt = "添加签名工具"
del_tool_txt = "删除签名工具"
main_frame_txt = "签名工具详细(只能从上面列表中选择)"
select_opk_txt = "选择插件"
sign_opk_txt = "签名"
clean_txt = "清除"
save_txt = "插件另存为"
add_tool_win_txt = "添加签名工具"
select_tool_txt = "选择签名工具"
add_txt = "确定"
cancel_txt = "取消"

def is_not_null(i):
    if not i:
        return False

    return True

class MyAddNewToolialog(tk.Toplevel):

    def __init__(self, parent, title=None, m=None, c=None, s=None, t=None, p=None):
        """ 在传入的父窗口上画"添加签名工具"页面 
            可以在构建时传入要添加的工具参数:
                m:型号  c:插件中心 s:插件名称
                t:到期时间 p:工具路径
        """

        # 主窗口
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None
        self.tool_path = ""

        # 开始画内容
        self.model = tk.StringVar(self)
        if m:
            self.model.set(m)
        lb = tk.Label(self, text="型号:")
        lb.grid(row=0, column=0, padx=10, pady=5)
        self.model_e = tk.Entry(self, textvariable=self.model)
        self.model_e.grid(row=0, column=1, pady=5)

        self.app_center = tk.StringVar(self)
        if c:
            self.app_center.set(c)
        lb = tk.Label(self, text="插件中心:")
        lb.grid(row=0, column=2, padx=10, pady=5)
        self.app_center_e = tk.Entry(self, textvariable=self.app_center)
        self.app_center_e.grid(row=0, column=3, pady=5)

        self.app_sign = tk.StringVar(self)
        if s:
            self.app_sign.set(s)
        lb = tk.Label(self, text="插件名称:")
        lb.grid(row=1, column=0, padx=10, pady=5)
        self.app_sign_e = tk.Entry(self, textvariable=self.app_sign)
        self.app_sign_e.grid(row=1, column=1, pady=5)


        self.expire_time = tk.StringVar(self)
        if t:
            self.expire_time.set(t)
        lb = tk.Label(self, text="到期时间:")
        lb.grid(row=1, column=2, padx=10, pady=5)
        self.expire_time_e = tk.Entry(self, textvariable=self.expire_time)
        self.expire_time_e.grid(row=1, column=3, pady=5)

        self.tool_name = tk.StringVar(self)
        if p:
            self.tool_path = p
            self.tool_name.set(os.path.basename(p))
        lb = tk.Label(self, text="签名工具:")
        lb.grid(row=2, column=0, padx=10, pady=5)
        self.tool_name_e = tk.Entry(self, textvariable=self.tool_name, state='readonly')
        self.tool_name_e.grid(row=2, column=1, pady=5)

        tk.Button(self,
                  text=select_tool_txt,
                  justify=tk.CENTER,
                  command=self.select_tool).grid(row=2, column=2, padx=10, pady=5)

        btn = tk.Button(self,
                  text=add_txt,
                  justify=tk.CENTER,
                  command=self.add_new_item, default=tk.ACTIVE)
        btn.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)

        tk.Button(self,
                  text=cancel_txt,
                  justify=tk.CENTER,
                  command=self.cancel_add).grid(row=3, column=2, padx=10, pady=5)

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

    def select_tool(self):
        """ "选择插件工具" 按钮执行函数"""

        self.tool_path = filedialog.askopenfilename(master=self)
        print("select tool: %s" % self.tool_path)
        self.tool_name.set(os.path.basename(self.tool_path))

    def add_new_item(self, event=None):
        """ "确定"按钮执行动作函数 """

        print ("click the add tool button!" )
        model = self.model_e.get()
        app_center = self.app_center_e.get()
        app_sign = self.app_sign_e.get()
        expire_time = self.expire_time_e.get()
        print ("all value: model:%s appcenter:%s sign:%s time:%s tool_path:%s " 
                % (model, app_center, app_sign, expire_time, self.tool_path))
        if not model:
            self.model_e.focus()
            messagebox.showerror("Error", "型号不能为空", parent=self)
            return False
        if not app_center:
            self.app_center_e.focus()
            messagebox.showerror("Error", "插件中心不能为空", parent=self)
            return False
        if not app_sign:
            self.app_sign_e.focus()
            messagebox.showerror("Error", "插件名不能为空", parent=self)
            return False
        if not expire_time:
            self.expire_time_e.focus()
            messagebox.showerror("Error", "到期时间不能为空", parent=self)
            return False
        if not self.tool_path:
            self.tool_name_e.focus()
            messagebox.showerror("Error", "工具文件不能为空", parent=self)
            return False

        # 检测时间格式
        try:
            d_expire = datetime.datetime.strptime(expire_time, "%Y-%m-%d")
            if (d_expire - datetime.datetime.now()).total_seconds() <= 0:
                self.expire_time_e.focus()
                messagebox.showerror("时间错误", "到期时间必须大于当前时间", parent=self)
                return False
        except:
            self.expire_time_e.focus()
            messagebox.showerror("日期格式错误", "正确格式: 2018-01-01", parent=self)
            return False

        msg = "型号: %s\n插件中心: %s\n插件名称: %s\n到期时间: %s\n签名工具: %s\n" %\
                (model, app_center, app_sign, expire_time, os.path.basename(self.tool_path))

        # 添加工具前的信息确认
        if not messagebox.askyesno("信息确认", "工具信息:\n" + msg + "\n" + "确定添加?", parent=self):
            return False

        res = sign_tool.add_new_tool(model, app_center, app_sign, expire_time, self.tool_path)
        print("res type=%s res=%s" % (type(res), str(res)))
        if not res:
            self.model_e.focus()
            messagebox.showerror("Error", "添加新的签名工具失败!", parent=self)
            return False

        messagebox.showinfo("添加成功", msg, parent=self)

        self.cancel_add()
        return True

    def clean_entry(self):
        """ 清除所有输入框 """

        self.model.set("")
        self.app_center.set("")
        self.app_sign.set("")
        self.expire_time.set("")
        self.tool_name.set("")

    def cancel_add(self, event=None):
        """ "取消"按钮执行动作函数 """

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

class MySignOpkWin(tk.Tk):

    def __init__(self, title):
        """ 在传入的父窗口上画"插件签名工具"页面 """

        # 其他成员
        # 用于生成工具的事件定时器ID

        # 主窗口
        tk.Tk.__init__(self)
        self.title(title)
        self.update()

        self.sign_id = ""
        self.opk_path = ""

        # 设置窗口居中
        v_main.just_center_window(self)

        # 创建主菜单
        menubar = tk.Menu(self)

        # 创建功能子菜单
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=sign_exit_txt, command=self.m_quit)

        # 加入子菜单
        menubar.add_cascade(label=sign_func_menu_txt, menu=filemenu)

        # 画菜单
        self.config(menu=menubar)

        # 已有的KEY
        list_frame = tk.Frame(self)
        list_frame  = tk.LabelFrame(self, text=list_frame_txt, padx=5, pady=5)
        list_frame.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        self.list_b = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.flush_list_b()
        self.list_b.bind("<ButtonRelease-1>", self.chosen)
        self.list_b.grid(column=0, columnspan=4, sticky=tk.W+tk.E)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.config(command=self.list_b .yview)
        scrollbar.grid(row=0, column=4, sticky=tk.N+tk.S)

        tk.Button(list_frame,
                  text=add_tool_txt,
                  justify=tk.CENTER,
                  command=self.add_new_tool).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(list_frame,
                  text=del_tool_txt,
                  justify=tk.CENTER,
                  command=self.del_tool).grid(row=1, column=1, padx=10, pady=5)

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
        lb = tk.Label(self.main_frame, text="插件名称:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.app_sign_e = tk.Entry(self.main_frame, textvariable=self.app_sign, state='readonly')
        self.app_sign_e.grid(row=m_row, column=m_col, padx=1, pady=5)

        m_col += 1
        self.expire_time = tk.StringVar(self)
        lb = tk.Label(self.main_frame, text="到期时间:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.expire_time_e = tk.Entry(self.main_frame, textvariable=self.expire_time, state='readonly')
        self.expire_time_e.grid(row=m_row, column=m_col, padx=1, pady=5)


        m_row += 1 
        m_col = 0
        self.opk_file = tk.StringVar(self)
        lb = tk.Label(self.main_frame, text="插件文件:")
        lb.grid(row=m_row, column=m_col, padx=10, pady=5, sticky=tk.E)
        m_col += 1
        self.opk_file_e = tk.Entry(self.main_frame, textvariable=self.opk_file, state='readonly')
        self.opk_file_e.grid(row=m_row, column=m_col, padx=1, pady=5)

        m_col += 1
        tk.Button(self.main_frame,
                  text=select_opk_txt,
                  justify=tk.CENTER,
                  command=self.select_opk).grid(row=m_row, column=m_col,
                                              padx=10, pady=5)

        m_row += 1 
        m_col = 1
        tk.Button(self.main_frame,
                  text=sign_opk_txt,
                  justify=tk.CENTER,
                  background="green",
                  command=self.do_sign_opk).grid(row=m_row, column=m_col,
                                              padx=10, pady=5)

        m_col += 1
        tk.Button(self.main_frame,
                  text=clean_txt,
                  justify=tk.CENTER,
                  command=self.clean_entry).grid(row=m_row, column=m_col,
                                             padx=10, pady=5)

        m_col += 1
        tk.Button(self.main_frame,
                  text=sign_exit_txt,
                  justify=tk.CENTER,
                  command=self.m_quit).grid(row=m_row, column=m_col,
                                             padx=10, pady=5)

        self.detail_frame = tk.LabelFrame(self, text=detail_frame_txt, padx=5, pady=5)
        self.detail_frame.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        self.detail = tk.Text(self.detail_frame)
        self.detail.insert(tk.INSERT, "插件签名执行结果将输出在这里...")
        self.detail.grid(pady=5, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        self.detail.config(state=tk.DISABLED)

        m_row = 1
        m_col = 0
        self.sign_opk_name = tk.StringVar(self)
        lb = tk.Label(self.detail_frame, text="签名后的插件:")
        lb.grid(row=m_row, padx=10, pady=5, sticky=tk.W)
        m_col += 1
        self.sign_opk_name_e = tk.Entry(self.detail_frame, textvariable=self.sign_opk_name, state='readonly',)
        self.sign_opk_name_e.grid(row=m_row, padx=1, pady=5, sticky=tk.E)

        m_row += 1
        tk.Button(self.detail_frame,
                  text=save_txt,
                  justify=tk.CENTER,
                  command=self.save_sign_tool).grid(row=m_row,
                                             padx=10, pady=5)

        # 绑定Enter 和 Escape键
        self.bind("<Return>", self.do_sign_opk)
        self.bind("<Escape>", self.m_quit)

        # make the dialog modal?
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.m_quit)

        self.model_e.focus()

        self.mainloop()

    def select_opk(self):
        """ "选择插件" 按钮执行函数 """

        self.opk_path = filedialog.askopenfilename(master=self)
        print("select opk path: %s" % self.opk_path)
        self.opk_file.set(os.path.basename(self.opk_path))

    def flush_list_b(self):
        """ 刷新 "签名工具列表" """

        self.list_b.delete(0, tk.END)
        for line in sign_tool.get_all_tools():
            item = "%-10s %-10s %-10s %-10s" % (line[0], line[1], line[2], line[3])
            self.list_b.insert(tk.END, item)

    def del_tool(self):
        """ "删除"签名工具 按钮执行函数 """
        select = self.list_b.curselection()
        if not select:
            return False

        index = select[0]
        item = self.list_b.get(index)
        item_list = list(filter(is_not_null, item.split(" ")))
        print("item_list=%s " % (str(item_list)))

        msg = "型号:%s\n插件中心:%s\n插件名称:%s\n过期时间:%s\n" % \
                (item_list[0], item_list[1], item_list[2], item_list[3])
        if not messagebox.askyesno("删除确认", "工具信息:\n" + msg + "\n" + "确定删除?", parent=self):
            return False

        result = sign_tool.del_tool(item_list[0], item_list[1],
                                   item_list[2], item_list[3])

        if not result:
            messagebox.showerror("删除失败", msg, parent=self)
        else:
            messagebox.showinfo("删除成功", msg, parent=self)
            self.flush_list_b()

        return True


    def add_new_tool(self, event=None):
        """ "添加"签名工具 按钮执行函数 """

        d = MyAddNewToolialog(self, add_tool_win_txt)

        self.flush_list_b()
        pass


    def save_sign_tool(self):
        """ "签名后插件另存为" 按钮执行函数 """

        if not self.opk_path:
            return False

        t_path = filedialog.asksaveasfilename(master=self, title="签名后插件另存为", initialfile=os.path.basename(self.opk_path))
        if not t_path:
            return False

        print ("copy %s => %s" % (self.opk_path, t_path))
        try:
            msg = "保存地址:%s" % t_path
            res = shutil.copy(self.opk_path, t_path)
            messagebox.showinfo(
                "保存成功", msg, parent=self)
        except:
            msg = "从%s拷贝到%s失败." % (self.opk_path, t_path)
            messagebox.showerror(
                "保存失败", msg, parent=self)


    def chosen(self, e):
        """ "签名工具列表" 选择动作函数 """

        select = self.list_b.curselection()
        if not select:
            return False

        index = select[0]
        item = self.list_b.get(index)
        item_list = list(filter(is_not_null, item.split(" ")))
        print("item_list=%s " % (str(item_list)))
        self.model.set(item_list[0])
        self.app_center.set(item_list[1])
        self.app_sign.set(item_list[2])
        self.expire_time.set(item_list[3])

    def clean_entry(self):
        """ 清除所有输入框 """

        self.model.set("")
        self.app_center.set("")
        self.app_sign.set("")
        self.expire_time.set("")
        self.opk_file.set("")


    def __disable_all_widget(self):
        """ 禁用所有的主要组件，排除"退出"组件 """

        for w in self.main_frame.winfo_children():
            value = w.cget("text")
            if value != sign_exit_txt:
                w.config(state=tk.DISABLED)

    def __enable_all_widget(self):
        """ 还原禁用的主要组件 """

        for w in self.main_frame.winfo_children():
            value = w.cget("text")
            if value != sign_exit_txt:
                w.config(state=tk.NORMAL)

        self.model_e.config(state='readonly')
        self.app_center_e.config(state='readonly')
        self.app_sign_e.config(state='readonly')
        self.expire_time_e.config(state='readonly')
        self.opk_file_e.config(state='readonly')


    def __sign_opk(self):
        """ 插件签名实现函数 """

        print("do real sign opk in alarm")
        model = self.model_e.get()
        app_center = self.app_center_e.get()
        app_sign = self.app_sign_e.get()
        expire_time = self.expire_time_e.get()
        opk_file = self.opk_file_e.get()

        var_list = []

        var_list.append(model)
        var_list.append(app_center)
        var_list.append(app_sign)
        var_list.append(expire_time)
        var_list.append(self.opk_path)

        state, output = sign_opk.sign_opk(var_list)

        print ("after do sign opk")

        # 显示执行结果
        msg = "型号: %s\n插件中心: %s\n插件名称: %s\n到期时间: %s\n插件文件: %s\n" %\
                (model, app_center, app_sign, expire_time, os.path.basename(self.opk_path))

        self.detail.config(state=tk.NORMAL)
        self.detail.delete(1.0, tk.END)
        if state == 0:
            self.detail.insert(tk.END, output)
            self.sign_opk_name.set(os.path.basename(self.opk_path))
        else:
            self.detail.insert(tk.END, "签名信息:\n" + msg + "\n")
            self.detail.insert(tk.END, "执行结果:\n插件签名失败\n 错误代码:%d\n 错误描述:%s\n"\
                               % (state, output))
        self.detail.config(state=tk.DISABLED)

        if state == 0:
            messagebox.showinfo("签名成功", msg, parent=self)
        else:
            messagebox.showerror("签名失败", msg, parent=self)

        self.__enable_all_widget()

    def do_sign_opk(self, event=None):
        """ "签名"按钮 执行函数 """

        print ("click the gen button!" )
        model = self.model_e.get()
        app_center = self.app_center_e.get()
        app_sign = self.app_sign_e.get()
        expire_time = self.expire_time_e.get()
        opk_file = self.opk_file_e.get()
        print ("all value: model:%s appcenter:%s appsign:%s expire_time:%s opk_file:%s " 
                % (model, app_center, app_sign, expire_time, opk_file))
        if not model:
            self.list_b.focus()
            messagebox.showerror("Error", "型号不能为空", parent=self)
            return False
        if not app_center:
            self.list_b.focus()
            messagebox.showerror("Error", "插件中心不能为空", parent=self)
            return False
        if not app_sign:
            self.list_b.focus()
            messagebox.showerror("Error", "插件名不能为空", parent=self)
            return False
        if not expire_time:
            self.list_b.focus()
            messagebox.showerror("Error", "到期时间不能为空", parent=self)
            return False
        if not opk_file:
            self.opk_file_e.focus()
            messagebox.showerror("Error", "插件不能为空", parent=self)
        elif '.opk' != opk_file[-4:]:
            self.opk_file_e.focus()
            messagebox.showerror("Error", "选择.opk后缀的插件", parent=self)
            return False

        # 三天之内到期 给予提示是否要使用此工具签名
        d_expire = datetime.datetime.strptime(expire_time, "%Y-%m-%d")
        d_next_three_days = datetime.datetime.now() + datetime.timedelta(days = 3)
        if (d_expire - d_next_three_days).total_seconds() <= 0:
            if not messagebox.askyesno("工具到期提醒", "到期时间: %s\n\n确定要使用此工具签名?" % expire_time, parent=self):
                return False

        # 签名前的信息确认
        msg = "型号: %s\n插件中心: %s\n插件名称: %s\n到期时间: %s\n需签名插件: %s\n" %\
                (model, app_center, app_sign, expire_time, opk_file)
        if not messagebox.askyesno("信息确认", "签名信息:\n" + msg + "\n" + "确定签名?", parent=self):
            return False

        print("good!")

        self.__disable_all_widget()

        self.sign_id = self.after(100, self.__sign_opk)

    def m_quit(self, event=None):
        """ "退出"按钮执行动作函数 """

        print ("click the quit button!")
        if self.sign_id: 
            self.after_cancel(self.sign_id)
        self.destroy()

def test():

    d = MySignOpkWin(sign_win_txt)


if __name__ == '__main__':
    test()
