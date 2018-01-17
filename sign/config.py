#!/usr/bin/python3

#
# 全局配置文件
#   INSTALL_PATH: 代码存放目录
#
import tempfile
import configparser
import os

INSTALL_PATH = "/opt/work/python/sign"

def get_tmp_path():
    return tempfile.gettempdir()

def get_temp_conf_file():
    """ 获取用来保存不重要信息的配置文件路径 """

    return os.path.join(tempfile.gettempdir(), "__sign.conf")

def save_tmp_config(section, key, value):
    """ 设置一些不需要长久保存的配置 """

    cf = configparser.ConfigParser()
    cf.read(get_temp_conf_file())

    if not cf.has_section(section):
        cf.add_section(section)

    cf.set(section, key, value)
    cf.write(open(get_temp_conf_file(), 'r+'))

    return True

def get_tmp_config(section, key):
    """ 获取不需要长久保存的配置 """

    if not os.path.exists(get_temp_conf_file()):
        with open(get_temp_conf_file(), 'w') as f:
            print("create file %s" % get_temp_conf_file())
        return ""

    cf = configparser.ConfigParser()
    cf.read(get_temp_conf_file())

    if cf.has_section(section) and cf.has_option(section, key):
        return cf.get(section, key)

    return ""

def test():
    path = get_tmp_config("global", "save_path")
    print("get path=%s" % path)

    save_tmp_config("global", "save_path", "/opt/work/exchange_dir/")
    save_tmp_config("data", "a", "1")
    save_tmp_config("data", "a", "2")
    save_tmp_config("data", "a", "3")

    path = get_tmp_config("global", "save_path")
    print("after save get path=%s" % path)
    path = get_tmp_config("bbbb", "b")
    print("after save get bbbb.b=%s" % path)
    path = get_tmp_config("data", "a")
    print("after save get data.a=%s" % path)
    path = get_tmp_config("data", "b")
    print("after save get data.b=%s" % path)

if __name__ == '__main__':
    test()
