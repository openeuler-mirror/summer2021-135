import os
import sys
import re
from collections import defaultdict

# match the (
def match(line):
    brackets_num = 0
    quotation_num = 0
    for l in line:
        if l == "\"":
            quotation_num = quotation_num + 1
        if l == "(" and quotation_num % 2 == 0:
            brackets_num = brackets_num + 1
        if l == ")" and quotation_num % 2 == 0:
            brackets_num = brackets_num - 1
    if brackets_num == 0:
        return True
    else:
        return False

# print(match("print(\"Can not find pr)oper test-type for %s.\" % device.get_name())"))
def Task_1():
    # (1) Given an RPM package, identify all Python scripts in the RPM package
    print("Task 1:")
    def unzip(file_dir):
        for file in os.listdir(file_dir):
            # print(file)
            if file.endswith(".rpm"):
                # os.system('rpm2cpio nginx-1.12.2-1.el7_4.ngx.x86_64.rpm | cpio -div')
                os.system('rpm2cpio {} | cpio -div'.format(file))
                # print(file)
    python_file = []
    python_root = []
    python_dirs = []
    def sub_file(file_dir):
        # path, subdir, subfile
        for root, dirs, files in os.walk(file_dir):
            # print(root)
            # print(dirs)
            # print(files)
            for file in files:
                if file.endswith(".py") and file != os.path.basename(sys.argv[0]):
                    python_file.append(file)
                    python_root.append(root)
                    python_dirs.append(dirs)
    #unzip(os.getcwd())
    sub_file(os.getcwd())
    if not python_file:
        print("There is no python file in the rpm package")
    else:
        print("The scripts in the RPM package are:")
        for i in range(len(python_file)):
            if i % 5 == 4 or i == len(python_file) - 1:
                print(python_file[i])
            else:
                print(python_file[i], end=" ")
    return python_root, python_file


def Task_2(python_root, python_file):
    # (2) Identify system servi`ces with startup, shutdown, and restart operations in the script
    # for file in python_file:
    print("--" * 100)
    print("Task 2:")
    start_command = defaultdict(list)
    # start_command_dir = []
    restart_command = defaultdict(list)
    # restart_command_dir = []
    stop_command = defaultdict(list)
    # stop_command_dir = []
    for i in range(len(python_file)):
        with open(python_root[i] + '/' + python_file[i], 'r') as f:
            lines = f.readlines()
            # lines = iter(lines)
            pass_num = 0
            for index in range(len(lines)):
                if pass_num > 0:
                    pass_num = pass_num - 1
                    continue
                # if "systemctl" in line:
                #     print(python_file[i] + '--------' + line)
                line = lines[index]
                string = line.strip()
                # print(i, index)
                # if i == 18 and index == 75:
                    # continue
                if string.endswith("%"):
                    string = string + lines[index + 1].strip()
                    pass_num = pass_num + 1
                while string.endswith("\\"):
                    string = string.replace("\\", "") + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                while not match(string):
                    string = string + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                pattern = re.compile('"(.*)"')
                str_rel = pattern.findall(string)
                if "systemctl restart" in line:
                    restart_command[python_root[i] + '/' + python_file[i]].append(str_rel[0])
                    # restart_command.append(line.strip())
                    # restart_command_dir.append(python_root[i] + '/' + python_file[i])
                     # restart_dic[python_root[i] + '/' + python_file[i]] = line.strip()
                if "systemctl stop" in line or "systemctl disable" in line:
                    stop_command[python_root[i] + '/' + python_file[i]].append(str_rel[0])
                    # stop_command.append(line.strip())
                    # stop_command_dir.append(python_root[i] + '/' + python_file[i])
                    # stop_dic[python_root[i] + '/' + python_file[i]] = line.strip()
                if "systemctl start" in line or "systemctl enable" in line:
                    start_command[python_root[i] + '/' + python_file[i]].append(str_rel[0])
                    # start_command.append(line.strip())
                    # start_command_dir.append(python_root[i] + '/' + python_file[i])
                    # start_dic[python_root[i] + '/' + python_file[i]] = line.strip()
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


def Task_3(python_root, python_file):
    # (3) Identify the system commands called by the script
    print("--" * 100)
    print("Task 3:")
    sys_command = defaultdict(list)
    sys_command_dir = []
    for i in range(len(python_file)):
        with open(python_root[i] + '/' + python_file[i], 'r') as f:
            lines = f.readlines()
            pass_num = 0
            for index in range(len(lines)):
                if pass_num > 0:
                    pass_num = pass_num - 1
                    continue
                line = lines[index].strip()
                if line.startswith('import'):
                    continue
                if line.endswith("%"):
                    line = line + lines[index + 1].strip()
                    pass_num = pass_num + 1
                while line.endswith("\\"):
                    line = line.replace("\\", "") + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                while not match(line):
                    line = line + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                if "os.system" in line or "os.popen" in line or "commands" in line or "subprocess" in line:
                    if line.find("#") == -1 or (line.find('#') != -1 and line.find('os.system') != -1 and line.index('#') > line.index("os.system"))\
                            or (line.find('#') != -1 and line.find('os.popen') != -1 and line.index('#') > line.index("os.popen"))\
                            or (line.find('#') != -1 and line.find('commands') != -1 and line.index('#') > line.index("commands")) \
                            or (line.find('#') != -1 and line.find('subprocess') != -1 and line.index('#') > line.index("subprocess")):
                        # print(python_root[i] + '/' + python_file[i] + "        " + line.strip())
                        # sys_command[python_root[i] + '/' + python_file[i]] = line.strip()
                        sys_command[python_root[i] + '/' + python_file[i]].append(line.strip())
                        # sys_command.append(line.strip())
                        # sys_command_dir.append(python_root[i] + '/' + python_file[i])
    if sys_command:
        print("The system calls in the script include:")
        for dir in sys_command:
            for command in sys_command[dir]:
                print(command + "----->>>>>>>" + dir)
            # print(dir[0])
            # for command in dir:
            #     print(command)
        # for i in range(len(sys_command)):
        #     print(sys_command[i] + "----->>>>>>>" + sys_command_dir[i])

    else:
        print("No system commands called were found in all scripts")
    return sys_command


def Task_4(sys_command):
    # (4) Identify whether the command is provided by the RPM software package or the operating system
    print("--" * 100)
    print("Task 4:")
    # from os import listdir
    # filenames1 = listdir("/bin")
    # filenames2 = listdir("/sbin")
    # filenames = filenames1 + filenames2
    # #print(filenames)
    # with open("os.txt", "w") as file:
    #     for str in filenames:
    #         file.write(str + "\n")
    command_task4 = []
    with open("os.txt", 'r') as file:
        os_commonds = file.readlines()
        # print(os_commond)
        # if 'memtester\n' in os_commond:
        #     print("yes")
        for os_commond in os_commonds:
            os_commond = os_commond.replace('\n', '')
            command_task4.append(os_commond)
            # print(os_commond)
    # print(sys_command)
    command_task3 = []
    for dir in sys_command:
        for command in sys_command[dir]:
            command_task3.append(re.findall(r'[(](.*?)[)]', command))

    print("The commands that come with the operating system include:")
    for i in range(len(command_task3)):
        command_string = command_task3[i][0]
        if "\"" in command_string:
            # print(command_string)
            word_list = command_string.split(" ")
            if word_list[0].endswith("\""):
                word_list[0] = eval(word_list[0])
            else:
                word_list[0] = eval(word_list[0] + "\"")
            # print(word_list)
            if "|" not in word_list and word_list[0] in command_task4:
                print(" ".join(word_list))
            if "|" in word_list:
                if word_list[0] in command_task4:
                    print(" ".join(word_list[:word_list.index("|")]))
                if word_list[word_list.index("|") + 1] in command_task4:
                    print(" ".join(word_list[word_list.index("|") + 1:]))
        # print(command_string)



if __name__ == '__main__':
    python_root, python_file = Task_1()
    Task_2(python_root, python_file)
    sys_command = Task_3(python_root, python_file)
    Task_4(sys_command)
