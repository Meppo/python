#!/usr/bin/python3

#
# 生成签名工具 功能实现
#   build_sign_tool(var_list)
#      参数: var_list: [MODEL, APP_CENTER, APP_SIGN, AUTHOR, SIGN_AUTHOR]
#      返回: [status, tool_path, msg]
#
# 注: 秘钥的匹配查找功能实现在 sign_key 包中
#

import os
import subprocess
import sign_key
import time

BUILD_SH = "/opt/work/N360/N360_Power4S/user/nossdk/sign_tools_all/sign_tool/build_sign_tool.sh"

def build_sign_tool(var_list):
    """ 生成插件工具实现函数
        参数: var_list: [MODEL, APP_CENTER, APP_SIGN, AUTHOR, SIGN_AUTHOR]
        返回: [status, tool_path, msg]
    """

    if len(var_list) < 5:
        print("too few argus")
        return [-1, "","too few argus: build_sign_tool([MODEL, APP_CENTER, APP_SIGN, AUTHOR, SIGN_AUTHOR])"]

    model = var_list[0]
    app_center = var_list[1]
    app_sign = var_list[2]
    author = var_list[3]
    sign_author = var_list[4]

    key_path = sign_key.get_key_path(model, app_center)
    if not key_path:
        print("can't find the key for %s %s" % (model, app_center))
        return [-2, "", "can't find the key for %s %s" % (model, app_center)]

    cmd = "%s %s %s %s %s %s %s" % (BUILD_SH, key_path, model, app_sign, app_center, author, sign_author)
    output = "执行时间:\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n"
    output = output + "执行命令:\n" + cmd + "\n\n"
    process = os.popen(cmd) # return file
    while True:
        tmp = process.read()
        if not tmp:
            break
        output = output + "执行结果:\n" + tmp + "\n\n"
    process.close()

    if not output:
        return [0, "", "no output.."]

    # find target name from output
    #  ...find "=> [app_sign]_[model]_[app_center]_[time].tar.gz"
    target_name = ""
    end = output.find(".tar.gz")
    if end > 0:
        start = output.rfind("=> ", 0, end)
        if start > 0:
            target_name = output[start+3:end+7]
            print("last sign tool name: %s" % target_name)

    return [0, target_name, output]


def test():
    items = sign_key.get_all_keys()
    index = 0

    if len(items) <= 0:
        print ("no key to build sign tool!")
        return False

    for i in items:
        print("%d: %s" % (index, i))
        var = [i[0], i[1], "airlink_app", "xxx", "0"]
        state,output = build_sign_tool(var)
        print ("%d output=%s" % (state, output))
        index = index+1
        break

    return True

if __name__ == '__main__':
    test()
