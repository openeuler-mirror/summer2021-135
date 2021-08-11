import os
import sys
import re
from collections import defaultdict

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
# unzip(os.getcwd())
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

# (2) Identify system services with startup, shutdown, and restart operations in the script
# for file in python_file:
print("--" * 100)
print("Task 2:")
start_command = defaultdict(list)
# start_command_dir = []
restart_command = defaultdict(list)
# restart_command_dir = []
stop_command = defaultdict(list)
# stop_command_dir = []
def match(line):
    l = []
    parentheses = "()"
    for i in range(len(line)):
        word = line[i]
        if parentheses.find(word) == -1:
            continue
        if word == '(':
            l.append(word)
            continue
        if len(l) == 0:
            return False
        p = l.pop()
        if p == '(' and word == ')':
            continue
        else:
            return False
    if len(l) > 0:
        return False
    return True
for i in range(len(python_file)):
    with open(python_root[i] + '/' + python_file[i], 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # if "systemctl" in line:
            #     print(python_file[i] + '--------' + line)
            string = line.strip()
            if string.endswith("\\"):
                string = string + lines[index + 1].strip()
            if not match(string):
                string = string + lines[index + 1].strip()
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

# (3) Identify the system commands called by the script
print("--" * 100)
print("Task 3:")
sys_command = defaultdict(list)
sys_command_dir = []
for i in range(len(python_file)):
    with open(python_root[i] + '/' + python_file[i], 'r') as f:
        lines = f.readlines()
        for index, lr in enumerate(lines):
            line = lr.strip()
            if line.endswith("\\"):
                line = line + lines[index + 1].strip()
            if not match(line):
                line = line + lines[index + 1].strip()
            if "os.system" in line or "os.popen" in line or "commands" in line or "subprocess" in line:
                if line.find("#") == -1 or (line.find('#') != -1 and line.find('os.system') != -1 and line.index('#') > line.index("os.system"))\
                        or (line.find('#') != -1 and line.find('os.popen') != -1 and line.index('#') > line.index("os.popen"))\
                        or (line.find('#') != -1 and line.find('commands') != -1 and line.index('#') > line.index("commands"))\
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
# (4) Identify whether the command is provided by the RPM software package or the operating system

