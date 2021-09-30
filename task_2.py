# 识别出脚本中带有启动，关闭，重启操作的系统服务（10%）
from collections import defaultdict
import re
from utils import match


def Task_2(abs_file):
    print("--" * 100)
    print("Task 2:")
    start_command = defaultdict(list)
    restart_command = defaultdict(list)
    stop_command = defaultdict(list)
    for i in range(len(abs_file)):
        with open(abs_file[i], 'r') as f:
            lines = f.readlines()
            pass_num = 0    # 利用pass_num去处理出现注释的问题。
            for index in range(len(lines)):
                if pass_num > 0:
                    pass_num = pass_num - 1
                    continue
                line = lines[index]
                string = line.strip()
                if string.endswith("%"):
                    string = string + " " + lines[index + 1].strip()
                    pass_num = pass_num + 1
                while string.endswith("\\"):
                    string = string.replace("\\", "") + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                while not match(string):
                    string = string + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                if "systemctl start" in line or "systemctl enable" in line:
                    pattern1 = re.compile('"(.*)"')
                    str_rel1 = pattern1.findall(string)
                    pattern2 = re.compile("'(.*)'")
                    str_rel2 = pattern2.findall(string)
                    if str_rel1 != [] and str_rel2 == []:
                        start_command[abs_file[i]].append(str_rel1[0])
                    if str_rel2 != [] and str_rel1 == []:
                        start_command[abs_file[i]].append(str_rel2[0])
                if "systemctl restart" in line:
                    pattern1 = re.compile('"(.*)"')
                    str_rel1 = pattern1.findall(string)
                    pattern2 = re.compile("'(.*)'")
                    str_rel2 = pattern2.findall(string)
                    if str_rel1 != [] and str_rel2 == []:
                        restart_command[abs_file[i]].append(str_rel1[0])
                    if str_rel2 != [] and str_rel1 == []:
                        restart_command[abs_file[i]].append(str_rel2[0])
                if "systemctl stop" in line or "systemctl disable" in line:
                    pattern1 = re.compile('"(.*)"')
                    str_rel1 = pattern1.findall(string)
                    pattern2 = re.compile("'(.*)'")
                    str_rel2 = pattern2.findall(string)
                    if str_rel1 != [] and str_rel2 == []:
                        stop_command[abs_file[i]].append(str_rel1[0])
                    if str_rel2 != [] and str_rel1 == []:
                        stop_command[abs_file[i]].append(str_rel2[0])
    if start_command:
        print("The system services with startup operations in the script include:")
        for dir in start_command:
            for command in start_command[dir]:
                print(command + "----->>>>>>>" + dir)
    else:
        print("No system services related to startup operations were found in all scripts.")
    print()
    if restart_command:
        print("The system services with restart operations in the script include:")
        for dir in restart_command:
            for command in restart_command[dir]:
                print(command + "----->>>>>>>" + dir)
    else:
        print("No system services related to restart operations were found in all scripts")
    print()
    if stop_command:
        print("The system services with shutdown operations in the script include:")
        for dir in stop_command:
            for command in stop_command[dir]:
                print(command + "----->>>>>>>" + dir)
    else:
        print("No system services related to shutdown operations were found in all scripts")

    return start_command, restart_command, stop_command

