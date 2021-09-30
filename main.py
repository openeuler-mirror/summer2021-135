from task_1 import Task_1
from task_2 import Task_2
from task_3 import Task_3
from task_4 import Task_4
from task_difference import difference
def main():
    # print('请输入文件夹下你想要分析的rpm包名，(包含.rpm)')
    # file = input()
    file = 'oec-hardware-1.0.0-2.x86_64.rpm'
    abs_file = Task_1(file)
    start_command, restart_command, stop_command = Task_2(abs_file)
    sys_command = Task_3(abs_file)
    ans, other = Task_4(sys_command)
    # generate_pdf(file, abs_file, start_command, restart_command, stop_command, sys_command, ans)
    file2 = 'oec-hardware-1.0.0-2.aarch64.rpm'
    abs_file2 = Task_1(file2)
    start_command2, restart_command2, stop_command2 = Task_2(abs_file2)
    sys_command2 = Task_3(abs_file2)
    ans2, other2 = Task_4(sys_command2)
    difference(start_command, start_command2, restart_command, restart_command2, stop_command, stop_command2, sys_command, sys_command2, ans, ans2, other, other2)
if __name__ == '__main__':
    main()
