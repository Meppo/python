#!/usr/bin/python3

#
# 插件签名 功能实现
#   sign_opk(var_list)
#      参数: var_list: [model, app_center, app_sign, expire_time, opk_path]
#      返回: [status, msg]
#           status : 0 成功   !=0 错误码
#
# 注: 签名工具的查找功能实现在 sign_tool 包中
#

import os
import subprocess
import tarfile
import shutil
import time

# 自定义模块
import sign_tool
import config

def sign_opk(var_list):
    """ 插件签名实现函数
        var_list: [model, app_center, app_sign, expire_time, opk_path]
        根据型号, 插件中心，插件名，到期时间找到签名工具 对opk_path进行签名
    """

    model = var_list[0]
    app_center = var_list[1]
    app_sign = var_list[2]
    expire_time = var_list[3]
    opk_path = var_list[4]

    if not model or not app_center or not app_sign\
            or not expire_time or not opk_path:
        msg = "error argus, model:%s app_center:%s app_sign:%s expire_time:%s opk_path:%s" % \
                (model, app_center, app_sign, expire_time, opk_path)
        print(msg)
        return [-1, msg]

    if not os.path.exists(opk_path):
        msg = "opk not exist:%s" % opk_path
        print(msg)
        return [-1, msg]

    tool_path = sign_tool.get_tool_path(model, app_center, app_sign, expire_time)
    if not tool_path:
        msg = "can't find the tool for %s %s %s %s" % (model, app_center, app_sign, expire_time)
        print(msg)
        return [-2, msg]

    try:
        target_path = os.path.join(config.get_tmp_path(), "_tmp_sign_tool")
        shutil.rmtree(target_path, ignore_errors=True)
        os.mkdir(target_path)

        tar = tarfile.open(tool_path, "r:*")
        for i in tar.getmembers():
            if i.isfile():
                name = os.path.basename(i.name)
                if name == "make_sign.sh":
                    script_dir = os.path.join(target_path, os.path.dirname(i.name))

            tar.extract(i, target_path)
        tar.close()
    except:
        if target_path and os.path.exists(target_path):
            shutil.rmtree(target_path) 

        msg = "extract tool %s failed!" % tool_path
        print(msg)
        return [-3, msg]

    # 执行脚本进行签名
    cmd = "cd %s && chmod +x make_sign.sh && ./make_sign.sh %s" % (script_dir, opk_path)
    output = "执行时间:\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n"
    output = output + "执行命令:\n" + cmd + "\n\n"
    process = os.popen(cmd) # return file
    while True:
        tmp = process.read()
        if not tmp:
            break
        output = output + "执行结果:\n" + tmp + "\n\n"
    process.close()

    shutil.rmtree(target_path) 

    if not output:
        return [0, "no output.."]

    return [0, output]

def test():
    var_list = []
    var_list.append("P0")
    var_list.append("360")
    var_list.append("airlink_app")
    var_list.append("2018-02-28")
    var_list.append("/opt/work/exchange_dir/tcpdump_tool_P1_sign.opk")
    status, output = sign_opk(var_list)
    print("st=%d output=%s" % (status, output))

    return True

if __name__ == '__main__':
    test()
