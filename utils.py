import os

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

def unzip(file):
    # for file in os.listdir(file_dir):
    #     # print(file)
    #     if file.endswith(".rpm"):
    #         # os.system('rpm2cpio nginx-1.12.2-1.el7_4.ngx.x86_64.rpm | cpio -div')
    #         os.system('rpm2cpio {} | cpio -div'.format(file))
    #         # print(file)
    os.system('mkdir {}'.format(file.replace('.rpm', "")))
    os.system('cp {} {}'.format(file, file.replace('.rpm', "")))
    os.chdir(file.replace('.rpm', ""))
    os.system('rpm2cpio {} | cpio -div'.format(file))
    os.chdir('../')