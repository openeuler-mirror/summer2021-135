# 给定RPM包，识别RPM包里所有的Python脚本，也有可能没有（10%）
import os
from utils import unzip
def Task_1(file):
    print("Task 1:")
    # 如果没有将rpm包解压，则需要使用utils中的unzip工具，先将其解压。
    # unzip(os.getcwd())
    unzip(file)
    #os.system('rpm2cpio {} | cpio -div'.format(file))
    print('-------------------' * 100)
    # print(os.getcwd())
    python_file = []
    python_root = []
    python_dirs = []
    abs_file = []
    # code_file = ['utils.py', 'task_1.py', 'task_2.py', 'task_3.py', 'task_4.py', 'main.py', 'task_difference.py']
    def sub_file(file_dir):
        # path, subdir, subfile
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                # if file.endswith(".py") and file not in code_file:
                if file.endswith(".py"):
                    python_file.append(file)
                    python_root.append(root)
                    python_dirs.append(dirs)
    sub_file(file.replace('.rpm', ""))
    if not python_file:
        print("There is no python file in the rpm package")
    else:
        print("The scripts in the RPM package are:")
        for i in range(len(python_file)):
            abs_file.append(os.path.join(python_root[i] + "/" + python_file[i]))
            print(abs_file[i])
    return abs_file
