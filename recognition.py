import os
import sys

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
start_dic = {}
restart_dic = {}
stop_dic = {}
for i in range(len(python_file)):
    with open(python_root[i] + '/' + python_file[i], 'r') as f:
        lines = f.readlines()
        for line in lines:
            # if "systemctl" in line:
            #     print(python_file[i] + '--------' + line)
            if "systemctl restart" in line:
                restart_dic[python_root[i] + '/' + python_file[i]] = line.strip()
            if "systemctl stop" in line or "systemctl disable" in line:
                stop_dic[python_root[i] + '/' + python_file[i]] = line.strip()
            if "systemctl start" in line or "systemctl enable" in line:
                start_dic[python_root[i] + '/' + python_file[i]] = line.strip()
if bool(start_dic):
    print("The system services with startup operations in the script include:")
    for key in start_dic:
        print(start_dic[key] + "----->>>>>>>" + key)
else:
    print("No system services related to startup operations were found in all scripts.")
print()
if bool(restart_dic):
    print("The system services with restart operations in the script include:")
    for key in restart_dic:
        print(restart_dic[key] + "----->>>>>>>"  + key)
else:
    print("No system services related to restart operations were found in all scripts")
print()
if bool(stop_dic):
    print("The system services with shutdown operations in the script include:")
    for key in stop_dic:
        print(stop_dic[key] + "----->>>>>>>"  + key)
else:
    print("No system services related to shutdown operations were found in all scripts")
# (3) Identify the system commands called by the script
# (4) Identify whether the command is provided by the RPM software package or the operating system
