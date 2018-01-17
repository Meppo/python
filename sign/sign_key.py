#!/usr/bin/python3

#
# 所有产品(型号,插件中心)的秘钥管理功能 实现
#   增: add_new_key(model, app_center, key_path):
#   删: del_key(model, app_center):
#   获取指定秘钥: get_key_path(model, app_center):
#   获取现有秘钥s: get_all_keys():
#
# 1. 秘钥信息主要通过 DATA/SIGN_KEY.DATA 文件记录
#    秘钥保存在 KEY/ 目录下
# 2. 添加秘钥后修改秘钥的名字便于识别:
#    秘钥名字格式:  [model].[app_center].key
#

import os
import copy
import shutil

# 自定义模块
import config

DATA_FILE = os.path.join(config.INSTALL_PATH, 'DATA', "SIGN_KEY.DATA")
SEPERATE = "|"
ITEM_MEMBER_NUM=3
OLD_KEY_PATH = "/opt/work/N360/N360_Power4S/user/nossdk/sign_tools_all/KEY"
NEW_KEY_PATH = os.path.join(config.INSTALL_PATH, 'KEY')

all_data = []

def test_show_all_data():
    """ 测试用: 显示数组中所有key条目 """
    index = 0
    for i in all_data:
        print("%d: %s" % (index, str(i)))
        index = index + 1
    print("\n")


def write_all_keys_to_file():
    """ 将当前缓存中所有key条目(all_data)写到DATA_FILE """

    with open(DATA_FILE, 'w') as f:
        for i in all_data:
            line = SEPERATE.join(i)
            f.write(line + "\n")


def get_all_keys():
    """ 读KEY条目文档DATA_FILE 到缓存缓存数组all_data中
        all_data数组每条格式:
         [model, app_center, key_path]
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


def scan_keys():
    """ 扫描KEY目录 更新所有key条目数组all_data
        并重新更新到文件DATA_FILE """

    # clear all_data[]
    for i in all_data[0:]:
        all_data.remove(i)

    # scan all key
    allnames = os.listdir(NEW_KEY_PATH)

    for name in allnames:
        if '.key' != name[-4:]:
            continue
        item = name.split(".")
        if len(item) < 3:
            continue
        new_key_item = []
        new_key_item.append(item[0])
        new_key_item.append(item[1])
        name = os.path.join(NEW_KEY_PATH, name)
        new_key_item.append(name)
        print ("scan key: %s" % str(new_key_item))
        all_data.append(new_key_item)

    # write to file
    write_all_keys_to_file()

    pass


def get_key_path(model, app_center):
    """ 根据model, app_center获取相应的用来生成
        插件签名工具的key文件路径
    """

    if not all_data:
        get_all_keys()

    # 第一次查找,直接在DATA_FILE中记录的条目中查找
    m_retry = 0
    for i in all_data:
        m_model = i[0]
        m_app_center = i[1]
        m_key_path = i[2]
        if m_model == model and m_app_center == app_center:
            print("find key for %s %s: %s" % (model, app_center, m_key_path))

            if not os.path.exists(m_key_path):
                m_retry = 1
                break

            return m_key_path

    # 条目中存在 但实际KEY文件不存在
    # 重新扫描一次key目录
    # 重新查找看是否能找到model,appcenter对应的key文件
    if m_retry:
        scan_keys_to_file()

        for i in all_data:
            m_model = i[0]
            m_app_center = i[1]
            m_key_path = i[2]
            if m_model == model and m_app_center == app_center:
                print("find key for %s %s: %s" % (model, app_center, m_key_path))

                if not os.path.exists(m_key_path):
                    return ""

                return m_key_path

    return ""


def add_new_key(model, app_center, key_path):
    """ 为新的型号/插件中心 添加新的KEY """

    if not os.path.exists(key_path) or not os.path.isfile(key_path):
        print ("key file %s not exist!" % key_path)
        return False

    if not model or not app_center:
        print ("model[%s] app_center[%s] is null!" % (model, app_center))
        return False

    if model.find("|") >= 0 \
            or app_center.find("|") >=0 \
            or key_path.find("|") >=0:
        print ("model[%s] app_center[%s] file_path[%s] contain char '|', invalid!" 
                % (model, app_center, key_path))
        return False

    if not all_data:
        get_all_keys()

    exist = 0
    for i in all_data[0:]:
        m_model = i[0]
        m_app_center = i[1]
        if m_model == model and m_app_center == app_center:
            print("key has exist, replace it.")
            exist = 1
            break

    file_path = os.path.join(NEW_KEY_PATH, model + "." + app_center + ".key")
    if not exist:
        item = []
        item.append(model)
        item.append(app_center)
        item.append(file_path)
        all_data.append(item)

    shutil.copy(key_path, file_path)

    write_all_keys_to_file()

    return True


def del_key(model, app_center):
    """ 删除指定KEY """

    if not all_data:
        get_all_keys()

    result = False
    for i in all_data[0:]:
        m_model = i[0]
        m_app_center = i[1]
        m_key_path = i[2]
        if m_model == model and m_app_center == app_center:
            result = True
            if os.path.exists(m_key_path):
                os.remove(m_key_path)

            all_data.remove(i)
            write_all_keys_to_file()
            break

    return result


def del_all_keys():
    """ 删除所有KEY和文件
        注: 操作前注意key的备份
    """

    if not all_data:
        get_all_keys()

    for i in all_data[0:]:
        m_key_path = i[2]
        if os.path.exists(m_key_path):
            os.remove(m_key_path)

        all_data.remove(i)


# function list_all_keys()
# {
#     C_Info "--------- support list ------------"
#     local model=
#     local key=
#     local res=
#     local author=
# 
#     C_Info "MODEL\tAPP_CENTER\n"
#     for model in `ls $root_dir/KEY`
#     do
#         if [ ! -d "$root_dir/KEY/$model" ];then
#             continue;
#         fi
#         for key in `ls $root_dir/KEY/$model/*_server_private.key`
#         do
#             res=$(echo $(basename $key) | grep -Eo '(netcore|360)')
#             if [ -z "$res" ];then
#                 C_Info "$model\t360"
#             else
#                 C_Info "$model\t$res"
#             fi
#         done
#     done
# 
#     C_Info ""
# }
def old_2_new():
    """ 将老版本KEY目录下的key全部查找按新的
        组织方案移动到新目录
        旧版key存放目录: ../KEY/MODEL/MODEL_APPCENTER_server_private.key
        新版key存放目录: KEY/MODEL_APPCENTER.key
    """

    #  e.g:
    #   old path: ..../P1/P1_360_server_private.key
    #   after parse: model=P1  app_center=360
    #   old path: ..../P0/P0_server_private.key
    #   after parse: model=P1  app_center=360
    all_oldnames = os.listdir(OLD_KEY_PATH)
    for i in all_oldnames:
        old_dir = os.path.join(OLD_KEY_PATH, i)
        if not os.path.isdir(old_dir):
            continue
        m_model = i

        all_model_keys = os.listdir(old_dir)
        for j in all_model_keys:

            # abs path
            old_file = os.path.join(old_dir, j)

            # must be regular file
            if not os.path.isfile(old_file):
                continue

            # end with "_server_private.key"
            index = j.find("_server_private.key")
            if index <= 0:
                continue

            m_app_center = j[len(m_model)+1:index]
            if not m_app_center:
                # default app_center = "360"
                m_app_center = "360"
            m_key_path = old_file
            print ("find old key model:%s app_center:%s" % (m_model, m_app_center))

            add_new_key(m_model, m_app_center, m_key_path)

    #write_all_keys_to_file()
    pass

def test_arr_del():
    print("begin scan keys...")
    scan_keys()

    print("after scans")
    test_show_all_data()

def test():

    print("begin scan keys...")
    scan_keys()

    print("after scans")
    test_show_all_data()


    get_all_keys()
    print("after get all keys:")
    test_show_all_data()


    print("before add:")
    test_show_all_data()

    add_new_key("test_MODEL_1", "test_APPCENTER_1", "test_KEY_1.key")
    add_new_key("test_MODEL_2", "test_APPCENTER_2", "test_KEY_2.key")
    add_new_key("test_MODEL_3", "test_APPCENTER_3", "test_KEY_3.key")

    print("after add:")
    test_show_all_data()

    key_path = get_key_path("test_MODEL_1", "test_APPCENTER_1")
    print("get key path for %s %s : %s" % ("test_MODEL_1", "test_APPCENTER_1", key_path))

    del_key("test_MODEL_2", "test_APPCENTER_1")
    print("after del wrong item:")
    test_show_all_data()

    del_key("test_MODEL_2", "test_APPCENTER_2")
    print("after del test_MODEL_2:")
    test_show_all_data()

    key_path = get_key_path("test_MODEL_2", "test_APPCENTER_2")
    print("get key path for %s %s : %s" % ("test_MODEL_2", "test_APPCENTER_2", key_path))

    del_key("test_MODEL_1", "test_APPCENTER_1")
    del_key("test_MODEL_3", "test_APPCENTER_3")
    print("after del test_MODEL_1 and test_MODEL_3:")
    test_show_all_data()
    
    add_new_key("test_MODEL_1", "test_APPCENTER_1", "test_KEY_1.key")
    add_new_key("test_MODEL_2", "test_APPCENTER_2", "test_KEY_2.key")
    add_new_key("test_MODEL_3", "test_APPCENTER_3", "test_KEY_3.key")

    print("after add:")
    test_show_all_data()

    del_all_keys()
    print("after del all keys:")
    test_show_all_data()

if __name__ == '__main__':
    test_arr_del()
