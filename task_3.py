# 识别出脚本调用的系统命令，例如/bin目录下的命令（20%）
import re
from collections import defaultdict
from utils import match
import inspect
def Task_3(abs_file):
    print("--" * 100)
    print("Task 3:")
    sys_command = defaultdict(list)                             # 包含目标系统调用命令的指定行
    sys_command_dir = []
    not_command = []    # 去除一些类里面的调用，并不是真正的系统命令
    extra_command = []  # 可能存在一些类里面使用固定的系统命令进行调用
    # 用于记录extra_command
    for i in range(len(abs_file)):                              # abs_file为所有文件的绝对路径
        with open(abs_file[i], 'r') as f:
            lines = f.readlines()                               # lines为文件中所有行的内容
            pass_num = 0                                        # 通过pass_num解决文本中一条代码跨行的问题
            for index in range(len(lines)):
                if pass_num > 0:
                    pass_num = pass_num - 1
                    continue
                line = lines[index].strip()                     # line为文件中每一行的内容
                if line.startswith('import'):
                    continue
                if line.endswith("%"):
                    line = line + " " + lines[index + 1].strip()
                    pass_num = pass_num + 1
                while line.endswith("\\"):
                    line = line.replace("\\", "") + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                while not match(line):
                    line = line + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                p2 = re.compile(r'[(](.*)[)]', re.S)    # 正则表达式去除最外侧的括号
                if "subprocess" in line:
                    # print(1)
                    not_command.append(line)
                    if line.find("#") == -1 or line.find('#') != -1 and line.find('subprocess') != -1 and \
                            line.index('#') > line.index("subprocess"):
                        # print(2)
                        if "self." in re.findall(p2, line.strip())[0] and \
                                "subprocess" in re.findall(p2, line.strip())[0]:
                            # print(3)
                            for class_index in range(index, -1, -1):
                                if "class " in lines[class_index]:
                                    # print(lines[class_index].strip().split())
                                    # print(lines[class_index].strip().split()[1].strip(":"))
                                    if lines[class_index].strip().split()[1].strip(":") not in extra_command:
                                        extra_command.append(lines[class_index].strip().split()[1].strip(":"))
    # print('1' * 100)
    # print(not_command)

    # print(extra_command)
    # 获得extra_command
    continue_flag = 0
    for i in range(len(abs_file)):  # abs_file为所有文件的绝对路径
        with open(abs_file[i], 'r') as f:
            lines = f.readlines()  # lines为文件中所有行的内容
            pass_num = 0  # 通过pass_num解决文本中一条代码跨行的问题
            for index in range(len(lines)):
                index_record = index
                if continue_flag == 1:
                    continue
                if pass_num > 0:
                    pass_num = pass_num - 1
                    continue
                line = lines[index].strip()  # line为文件中每一行的内容
                if line.startswith('"""'):
                    continue_flag = 1
                    if line.endswith('"""'):
                        continue_flag = 0
                    continue
                if line.endswith('"""'):
                    continue_flag = 0
                    continue
                if line.startswith('from'):
                    continue
                if line.startswith('class'):
                    continue
                if line.startswith('import'):
                    continue
                if line.endswith("%"):
                    line = line + " " + lines[index + 1].strip()
                    pass_num = pass_num + 1
                while line.endswith("\\"):
                    line = line.replace("\\", "") + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                while not match(line):
                    line = line + lines[index + 1].strip()
                    index = index + 1
                    pass_num = pass_num + 1
                if line not in not_command:
                    if not extra_command:
                        if "os.system" in line or "os.popen" in line or "commands" in line or "subprocess" in line:
                            if line.find("#") == -1 or (
                                    line.find('#') != -1 and line.find('os.system') != -1 and line.index(
                                '#') > line.index("os.system")) \
                                    or (line.find('#') != -1 and line.find('os.popen') != -1 and line.index(
                                '#') > line.index("os.popen")) \
                                    or (line.find('#') != -1 and line.find('commands') != -1 and line.index(
                                '#') > line.index("commands")) \
                                    or (line.find('#') != -1 and line.find('subprocess') != -1 and line.index(
                                '#') > line.index("subprocess")):
                                if "%" in line.strip():
                                    command_list = []  # 将command按空格分开，去除多余的字符，存储到command_list中
                                    commands = line.strip().split()
                                    for index in range(len(commands)):
                                        command_list.append(
                                            commands[index].strip(')').strip('(').strip("'").strip('"'))
                                    # print(extra)
                                    # if extra in line:
                                    #     print(line.index(extra))
                                    # print(command_list)
                                    variable_num = 0  # 记录command_list中所包含的格式化字符串的数量
                                    variable = []  # 记录需要寻找的变量
                                    format_list = ['%c', '%r', '%s', '%d', '%i', '%u', '%o', '%x', '%X', '%e', '%E',
                                                   '%f', '%F', '%g', '%G']
                                    for target in command_list:
                                        for format in format_list:
                                            variable_num = variable_num + target.count(format)
                                    for index in range(len(command_list)):
                                        if command_list[index] == '%':
                                            while variable_num != 0:
                                                variable_num = variable_num - 1
                                                index = index + 1
                                                # 判断变量中是否有可能是通过两个加号连接
                                                if index + 2 <= len(command_list) - 1 and command_list[
                                                    index + 1] == '+':
                                                    # x = ''.join(filter(lambda i: i in ['#'] or i.isalnum(), x))
                                                    # 去除variable
                                                    # print('2' * 200)
                                                    variable.append(
                                                        command_list[index] + ' + ' + command_list[index + 2])
                                                else:
                                                    variable.append(command_list[index])
                                                    # ''.join(filter(lambda i: i in ['_'] or i.isalnum(),
                                            break
                                    # print(abs_file[i])
                                    # print(line.strip())
                                    # 处理变量中有可能存在括回的情况
                                    # print(variable)
                                    for variable_index in range(len(variable)):
                                        for var_index in range(len(variable[variable_index])):
                                            # print(variable_index)
                                            # print(var_index)
                                            # print(variable[variable_index][var_index])

                                            if ')' in variable[variable_index]:
                                                if '(' not in variable[variable_index] or variable[
                                                    variable_index].index('(') > variable[variable_index].index(')'):
                                                    if variable[variable_index][var_index] == ')':
                                                        variable[variable_index] = variable[variable_index][:var_index]
                                                        break
                                    # 去除可能存在的逗号
                                    for index in range(len(variable)):
                                        if '+' not in variable[index]:
                                            variable[index] = ''.join(
                                                filter(lambda i: i in ['_', '.'] or i.isalnum(), variable[index]))
                                    # print(variable)
                                    # print(index_record)
                                    # print(sys_command[abs_file[i]].index(line.strip()))

                                    for v in variable:
                                        # 能够找到变量
                                        for v_index in range(index_record - 1, -1, -1):
                                            # 判断没有空格的情况
                                            if v + '=' in lines[v_index] and v + '==' not in lines[v_index] and (
                                                    lines[v_index].index(v + '=') == 0 or lines[v_index].index(
                                                    v + '=') != 0 and lines[v_index][
                                                        lines[v_index].index(v + '=') - 1] == ' '):
                                                # print('2' * 200)
                                                # print(lines[v_index])
                                                # print(lines[v_index][lines[v_index].index(v + '=') + 1:])
                                                line = line.replace(v, lines[v_index][
                                                                       lines[v_index].index(v + '=') + len(
                                                                           v + '='):].strip())
                                                break
                                            # 判断可能出现空格的情况
                                            if v + ' =' in lines[v_index] and v + ' ==' not in lines[v_index] and (
                                                    lines[v_index].index(v + ' =') == 0 or lines[v_index].index(
                                                    v + ' =') != 0 and lines[v_index][
                                                        lines[v_index].index(v + ' =') - 1] == ' '):
                                                # print(lines[v_index].split())

                                                var_space = lines[v_index]
                                                # print(var_space)
                                                if var_space.strip().endswith('\\'):
                                                    var_space = var_space.strip() + lines[v_index + 1]
                                                var_space = var_space.split()
                                                # print(var_space.index("="))
                                                # print(' '.join(var_space[var_space.index("=") + 1:]))
                                                # print(variable.index(v) + 1)
                                                special_index = 0

                                                for j in range(line.index(v) - 1, -1, -1):
                                                    if (line[j] == '%'):
                                                        line = line[:j] + line[j + 1:]
                                                        break
                                                line = line.replace(v, '')

                                                break

                                    line = line.replace('{', '@$')
                                    line = line.replace('}', '$@')
                                    for format in format_list:
                                        if line.find(format):
                                            line = line.replace(format, '{}')
                                    # print('3' * 100)
                                    # print(line)
                                    line = line.format(*variable)
                                    line = line.replace('@$', '{')
                                    line = line.replace('$@', '}')
                                    # print(line)
                                    # print()

                                sys_command[abs_file[i]].append(line.strip())
                    else:
                        for extra in extra_command:

                            if "os.system" in line or "os.popen" in line or "commands" in line or "subprocess" in line\
                                    or extra == line or extra in line and\
                                    (line.index(extra) == 0 and
                                     line[line.index(extra) + len(extra)].isalpha() == False \
or len(line) == line.index(extra) + len(extra) and line[line.index(extra) - 1].isalpha() == False \
or line[line.index(extra) - 1].isalpha() == False and line[line.index(extra) + len(extra)].isalpha() == False):
                                if line.find("#") == -1 or (
                                        line.find('#') != -1 and line.find('os.system') != -1 and line.index(
                                        '#') > line.index("os.system")) \
                                        or (line.find('#') != -1 and line.find('os.popen') != -1 and line.index(
                                    '#') > line.index("os.popen")) \
                                        or (line.find('#') != -1 and line.find('commands') != -1 and line.index(
                                    '#') > line.index("commands")) \
                                        or (line.find('#') != -1 and line.find(extra) != -1 and line.index(
                                    '#') > line.index(extra)) \
                                        or (line.find('#') != -1 and line.find('subprocess') != -1 and line.index(
                                    '#') > line.index("subprocess")):
                                    if "%" in line.strip():
                                        command_list = []  # 将command按空格分开，去除多余的字符，存储到command_list中
                                        commands = line.strip().split()
                                        for index in range(len(commands)):
                                            command_list.append(
                                                commands[index].strip(')').strip('(').strip("'").strip('"'))
                                        # print(extra)
                                        # if extra in line:
                                        #     print(line.index(extra))
                                        # print(command_list)
                                        variable_num = 0  # 记录command_list中所包含的格式化字符串的数量
                                        variable = []  # 记录需要寻找的变量
                                        format_list = ['%c', '%r', '%s', '%d', '%i', '%u', '%o', '%x', '%X', '%e', '%E',
                                                       '%f', '%F', '%g', '%G']
                                        for target in command_list:
                                            for format in format_list:
                                                variable_num = variable_num + target.count(format)
                                        for index in range(len(command_list)):
                                            if command_list[index] == '%':
                                                while variable_num != 0:
                                                    variable_num = variable_num - 1
                                                    index = index + 1
                                                    # 判断变量中是否有可能是通过两个加号连接
                                                    if index + 2 <= len(command_list) - 1 and command_list[
                                                        index + 1] == '+':
                                                        # x = ''.join(filter(lambda i: i in ['#'] or i.isalnum(), x))
                                                        # 去除variable
                                                        # print('2' * 200)
                                                        variable.append(command_list[index] + ' + '
                                                                        + command_list[index + 2])
                                                    else:
                                                        variable.append(command_list[index])
                                                        # ''.join(filter(lambda i: i in ['_'] or i.isalnum(),
                                                break
                                        # print(abs_file[i])
                                        # print(line.strip())
                                        # 处理变量中有可能存在括回的情况
                                        # print(variable)
                                        for variable_index in range(len(variable)):
                                            for var_index in range(len(variable[variable_index])):
                                                # print(variable_index)
                                                # print(var_index)
                                                # print(variable[variable_index][var_index])

                                                if ')' in variable[variable_index]:
                                                    if '(' not in variable[variable_index] or\
                                                            variable[variable_index].index('(') > \
                                                            variable[variable_index].index(')'):
                                                        if variable[variable_index][var_index] == ')':
                                                            variable[variable_index] = \
                                                                variable[variable_index][:var_index]
                                                            break
                                        # 去除可能存在的逗号
                                        for index in range(len(variable)):
                                            if '+' not in variable[index]:
                                                variable[index] = ''.join\
                                                    (filter(lambda i: i in ['_','.'] or i.isalnum(), variable[index]))
                                        # print(variable)
                                        # print(index_record)
                                        # print(sys_command[abs_file[i]].index(line.strip()))

                                        for v in variable:
                                            # 能够找到变量
                                            for v_index in range(index_record - 1, -1, -1):
                                                # 判断没有空格的情况
                                                if v + '=' in lines[v_index] \
                                                        and v + '==' not in lines[v_index] \
                                                        and (lines[v_index].index(v + '=') == 0
                                                             or lines[v_index].index(v + '=') != 0
                                                             and lines[v_index][lines[v_index].
                                                                                        index(v + '=') - 1] == ' '):
                                                    # print('2' * 200)
                                                    # print(lines[v_index])
                                                    # print(lines[v_index][lines[v_index].index(v + '=') + 1:])
                                                    line = line.replace(v, lines[v_index][lines[v_index].
                                                                        index(v + '=') + len(v+'='):].strip())
                                                    break
                                                # 判断可能出现空格的情况
                                                if v + ' =' in lines[v_index] and\
                                                        v + ' ==' not in lines[v_index] and\
                                                        (lines[v_index].index(v + ' =') == 0 or
                                                         lines[v_index].index(v + ' =') != 0 and
                                                         lines[v_index][lines[v_index].index(v + ' =') - 1] == ' '):
                                                    # print(lines[v_index].split())

                                                    var_space = lines[v_index]
                                                    # print(var_space)
                                                    if var_space.strip().endswith('\\'):
                                                        var_space = var_space.strip() + lines[v_index + 1]
                                                    var_space = var_space.split()
                                                    #print(var_space.index("="))
                                                    #print(' '.join(var_space[var_space.index("=") + 1:]))
                                                    #print(variable.index(v) + 1)
                                                    special_index = 0

                                                    for j in range(line.index(v) - 1, -1, -1):
                                                        if(line[j] == '%'):
                                                            line = line[:j] + line[j + 1:]
                                                            break
                                                    line = line.replace(v, '')

                                                    break

                                        line = line.replace('{', '@$')
                                        line = line.replace('}', '$@')
                                        for format in format_list:
                                            if line.find(format):
                                                line = line.replace(format, '{}')
                                        # print('3' * 100)
                                        # print(line)
                                        line = line.format(*variable)
                                        line = line.replace('@$', '{')
                                        line = line.replace('$@', '}')
                                        # print(line)
                                        # print()


                                    sys_command[abs_file[i]].append(line.strip())
                        # print("yes")
                            # print(re.findall(p2, line.strip())[0])




    # 通过匹配粗略的得到了代码中包含指定命令的行存在了sys_command中
    if sys_command == []:
        print("No system commands called were found in all scripts")
    else:
        # for dir in sys_command:                 # dir为每个command所在的路径
        #     for command in sys_command[dir]:    # command为dir中的命令
        #          if '%' in command:             # 筛选出那些会因为存在变量而导致命令完不完整的情况
        #             command_list = []           # 将command按空格分开，去除多余的字符，存储到command_list中
        #             commands = command.split()
        #             for index in range(len(commands)):
        #                 command_list.append(commands[index].strip(')').strip('(').strip("'").strip('"'))
        #             print(command_list)
        #             variable_num = 0            # 记录command_list中所包含的格式化字符串的数量
        #             variable = []               # 记录需要寻找的变量
        #             for target in command_list:
        #                 for format in format_list:
        #                     variable_num = variable_num + target.count(format)
        #             for index in range(len(command_list)):
        #                 if command_list[index] == '%':
        #                     while variable_num != 0:
        #                         variable_num = variable_num - 1
        #                         index = index + 1
        #                         # 判断变量中是否有可能是通过两个加号连接
        #                         if index + 2 <= len(command_list) - 1 and command_list[index + 1] == '+':
        #                             variable.append(command_list[index] + ' + ' + command_list[index + 2])
        #                         else:
        #                             variable.append(command_list[index])
        #                     break
        #             print(dir)
        #             print(command)
        #             # 处理变量中有可能存在括回的情况
        #             # print(variable)
        #             for variable_index in range(len(variable)):
        #                 for var_index in range(len(variable[variable_index])):
        #                     # print(variable_index)
        #                     # print(var_index)
        #                     # print(variable[variable_index][var_index])
        #                     if variable[variable_index][var_index] == ')':
        #                         variable[variable_index] = variable[variable_index][:var_index]
        #                         break
        #
        #             print(variable)
        #             print(sys_command[dir].index(command))
        #             print()
        #
        #             for v in variable:
        #                 pass
        #                 # for v_index in range(sys_command[dir].index(command) - 1)
        # print('--' * 100)
        print("The system calls in the script include:")
        for dir in sys_command:
            for command in sys_command[dir]:
                new_command = command.split()
                command = " ".join(new_command)
                print(command + "----->>>>>>>" + dir)

    return sys_command
