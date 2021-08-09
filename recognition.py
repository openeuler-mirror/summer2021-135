import os
import sys

# (1) Given an RPM package, identify all Python scripts in the RPM package
def unzip(file_dir):
    for file in os.listdir(file_dir):
        # print(file)
        if file.endswith(".rpm"):
            # os.system('rpm2cpio nginx-1.12.2-1.el7_4.ngx.x86_64.rpm | cpio -div')
            os.system('rpm2cpio {} | cpio -div'.format(file))
            # print(file)
python_file = []
def sub_file(file_dir):
    # path, subdir, subfile
    for _, _, files in os.walk(file_dir):
        # print(root)
        # print(dirs)
        # print(files)
        for file in files:
            if file.endswith(".py") and file != os.path.basename(sys.argv[0]):
                python_file.append(file)
# unzip(os.getcwd())
sub_file(os.getcwd())
if not python_file:
    print("There is no python file in the rpm package")
else:
    print(' '.join(file for file in python_file))
