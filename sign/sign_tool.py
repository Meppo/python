#!/usr/bin/python3

#
# 所有插件签名工具管理功能 实现
#   增: add_new_tool(model, app_center, app_sign, expire_time, tool_path):
#   删: del_tool(model, app_center, app_sign, expire_time):
#   获取指定签名工具: get_tool_path(model, app_center, app_sign, expire_time):
#   获取现有签名工具s: get_all_tools():
#
# 1. 签名工具信息主要通过 DATA/SIGN_TOOL.DATA 文件记录
#    签名工具保存在 TOOL/ 目录下
# 2. 添加签名工具后修改名字便于识别:
#    签名工具名字格式:  [model].[app_center].[app_sign].[expire_time].tgz
#

import os
import copy
import shutil
import time

DATA_FILE = os.path.join(os.getcwd(), 'DATA', "SIGN_TOOL.DATA")
SEPERATE = "|"
ITEM_MEMBER_NUM=5
NEW_TOOL_PATH = os.path.join(os.getcwd(), 'TOOL')

all_data = []

def test_show_all_data():
    """ 测试用: 显示数组中所有tool条目 """
    index = 0
    for i in all_data:
        print("%d: %s" % (index, str(i)))
        index = index + 1
    print("\n")


def write_all_tools_to_file():
    """ 将当前缓存中所有tool条目(all_data)写到DATA_FILE """

    with open(DATA_FILE, 'w') as f:
        for i in all_data:
            line = SEPERATE.join(i)
            f.write(line + "\n")


def get_all_tools():
    """ 读TOOL条目文档DATA_FILE 到缓存缓存数组all_data中
        all_data数组每条格式:
         [model, app_center, app_sign, expire_time, tool_path]
    """

    # clear all_data[]
    for i in all_data[0:]:
        all_data.remove(i)

    if not os.path.exists(DATA_FILE):
        print ("%s not exist!" % DATA_FILE)
        return copy.deepcopy(all_data)

    with open(DATA_FILE, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n')
            tmp_data = line.split(SEPERATE)
            if len(tmp_data) != ITEM_MEMBER_NUM:
                continue
            all_data.append(tmp_data)

    return copy.deepcopy(all_data)


def scan_tools():
    """ 扫描TOOL目录 更新所有tool条目数组all_data
        并重新更新到文件DATA_FILE """

    # clear all_data[]
    for i in all_data[0:]:
        all_data.remove(i)

    # scan all tool
    allnames = os.listdir(NEW_TOOL_PATH)

    for name in allnames:
        if '.tgz' != name[-4:]:
            print("skip file:%s" % name)
            continue
        item = name.split(".")
        if len(item) != 5:
            print("skip file:%s" % name)
            continue
        new_tool_item = []
        new_tool_item.append(item[0])
        new_tool_item.append(item[1])
        new_tool_item.append(item[2])

        # 检查时间格式是否正确
        try:
            timeArray = time.strptime(item[3], "%Y-%m-%d")
        except:
            print("expire_time format error: %s" % item[3])
            continue
        new_tool_item.append(item[3])
        name = os.path.join(NEW_TOOL_PATH, name)
        new_tool_item.append(name)
        print ("scan tool: %s" % str(new_tool_item))
        all_data.append(new_tool_item)

    # write to file
    write_all_tools_to_file()

    pass


def get_tool_path(model, app_center, app_sign, expire_time):
    """ 根据model, app_center, app_sign, expire_time获取相应的
        插件签名工具路径
    """

    if not all_data:
        get_all_tools()

    # 第一次查找,直接在DATA_FILE中记录的条目中查找
    m_retry = 0
    for i in all_data:
        m_model = i[0]
        m_app_center = i[1]
        m_app_sign = i[2]
        m_expire_time = i[3]
        m_tool_path = i[4]
        if m_model == model and m_app_center == app_center \
                and m_app_sign == app_sign and m_expire_time == expire_time:

            print("find tool for %s %s %s %s:%s" % (model, app_center, app_sign, expire_time, m_tool_path))

            if not os.path.exists(m_tool_path):
                m_retry = 1
                break

            return m_tool_path

    # 条目中存在 但实际tool文件不存在
    # 重新扫描一次tool目录
    # 重新查找看是否能找到model,appcenter对应的tool文件
    if m_retry:
        scan_tools()

        m_model = i[0]
        m_app_center = i[1]
        m_app_sign = i[2]
        m_expire_time = i[3]
        m_tool_path = i[4]
        if m_model == model and m_app_center == app_center \
                and m_app_sign == app_sign and m_expire_time == expire_time:

            print("find tool for %s %s %s %s:%s" % (model, app_center, app_sign, expire_time, m_tool_path))

            if not os.path.exists(m_tool_path):
                return ""

            return m_tool_path

    return ""


def add_new_tool(model, app_center, app_sign, expire_time, tool_path):
    """ 为新的型号/插件中心 添加新的tool 
        时间格式固定为: year-mon-day  例如: 2018-01-02
    """

    if not os.path.exists(tool_path) or not os.path.isfile(tool_path):
        print ("tool file %s not exist!" % tool_path)
        return False

    if not model or not app_center or not app_sign or not expire_time:
        print ("model[%s] app_center[%s] app_sign[%s] expire_time[%s] is null!" 
                % (model, app_center, app_sign, expire_time))
        return False

    # 检测时间格式
    try:
        timeArray = time.strptime(expire_time, "%Y-%m-%d")
    except:
        print("expire_time format error: %s" % expire_time)
        return False

    if model.find("|") >= 0 \
            or app_center.find("|") >=0 \
            or app_sign.find("|") >=0 \
            or expire_time.find("|") >=0 \
            or tool_path.find("|") >=0:
        print ("model[%s] app_center[%s] app_sign[%s] expire_time[%s] file_path[%s] contain char '|', invalid!" 
                % (model, app_center, app_sign, expire_time, tool_path))
        return False

    if not all_data:
        get_all_tools()

    exist = 0
    for i in all_data[0:]:
        m_model = i[0]
        m_app_center = i[1]
        m_app_sign = i[2]
        m_expire_time = i[3]
        if m_model == model and m_app_center == app_center \
                and m_app_sign == app_sign and m_expire_time == expire_time:
            print("tool has exist, replace it.")
            exist = 1
            break

    file_path = os.path.join(NEW_TOOL_PATH, model + "." + app_center +  
                             "." + app_sign +  "." + expire_time + ".tgz")
    if not exist:
        item = []
        item.append(model)
        item.append(app_center)
        item.append(app_sign)
        item.append(expire_time)
        item.append(file_path)
        all_data.append(item)

    shutil.copy(tool_path, file_path)

    write_all_tools_to_file()

    return True


def del_tool(model, app_center, app_sign, expire_time):
    """ 删除指定tool """

    if not all_data:
        get_all_tools()

    result = False
    for i in all_data[0:]:
        m_model = i[0]
        m_app_center = i[1]
        m_app_sign = i[2]
        m_expire_time = i[3]
        m_tool_path = i[4]
        if m_model == model and m_app_center == app_center \
                and m_app_sign == app_sign and m_expire_time == expire_time:
            result = True
            if os.path.exists(m_tool_path):
                os.remove(m_tool_path)

            all_data.remove(i)
            write_all_tools_to_file()
            break

    return result


def del_all_tools():
    """ 删除所有tool和文件
        注: 操作前注意tool的备份
    """

    if not all_data:
        get_all_tools()

    for i in all_data[0:]:
        m_tool_path = i[4]
        if os.path.exists(m_tool_path):
            ret = os.remove(m_tool_path)
            print("del tool: %s ret: %s" % (m_tool_path, str(ret)))

        all_data.remove(i)


def test_scan():
    print("begin scan tools...")
    scan_tools()

    add_new_tool("P0", "360", "airlink_app", "2018-02-28", "tcpdump_tool_P1_360_TempSign_2018-02-31.tar.gz")
    add_new_tool("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-01", "test_tool_1.tool")
    add_new_tool("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-02", "test_tool_2.tool")
    add_new_tool("test_MODEL_3", "test_APPCENTER_3", "test_APPSIGN_3", "2018-02-03", "test_tool_3.tool")
    add_new_tool("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-04", "test_tool_4.tool")


    print("after scans")
    test_show_all_data()


def test():

    print("begin scan tools...")
    scan_tools()

    print("after scans")
    test_show_all_data()


    get_all_tools()
    print("after get all tools:")
    test_show_all_data()


    print("before add:")
    test_show_all_data()

    add_new_tool("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-01", "test_tool_1.tool")
    add_new_tool("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-02", "test_tool_2.tool")
    add_new_tool("test_MODEL_3", "test_APPCENTER_3", "test_APPSIGN_3", "2018-02-03", "test_tool_3.tool")
    add_new_tool("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-04", "test_tool_4.tool")

    print("after add:")
    test_show_all_data()

    tool_path = get_tool_path("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-01")
    print("get tool path for %s %s %s %s: %s" % ("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-04", tool_path))

    del_tool("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-05")
    print("after del wrong item:")
    test_show_all_data()

    del_tool("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-02")
    print("after del test_MODEL_2:")
    test_show_all_data()

    tool_path = get_tool_path("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-02")
    print("get tool path for %s %s %s %s: %s" % ("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-02", tool_path))

    del_tool("test_MODEL_3", "test_APPCENTER_3", "test_APPSIGN_3", "2018-02-03")
    del_tool("test_MODEL_1", "test_APPCENTER_1", "test_APPSIGN_1", "2018-02-01")
    print("after del test_MODEL_1 and test_MODEL_3:")
    test_show_all_data()
    
    add_new_tool("test_MODEL_2", "test_APPCENTER_2", "test_APPSIGN_2", "2018-02-02", "test_tool_2.tool")
    add_new_tool("test_MODEL_3", "test_APPCENTER_3", "test_APPSIGN_3", "2018-02-03", "test_tool_3.tool")

    print("after add:")
    test_show_all_data()

    del_all_tools()
    print("after del all tools:")
    test_show_all_data()

if __name__ == '__main__':
    # test()
    test_scan()

