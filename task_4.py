# 识别出该命令是RPM软件包自己带的还是操作系统的，例如/bin目录下的命令就是操作系统自带的，不是软件包的（30%）
import re

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
            command_task4.append(os_commond.strip())
            # print(os_commond)
    # print(sys_command)
    command_task3 = []
    for dir in sys_command:
        for command in sys_command[dir]:
            command_task3.append(re.findall(r'[(](.*?)[)]', command))
    ans = []
    other = []
    print("The commands that come with the operating system include:")
    for i in range(len(command_task3)):
        temp = command_task3[i]
        if not temp:
            continue
        command_string = temp[0]
        if "\"" in command_string:
            # print(command_string)
            word_list = command_string.split(" ")
            if word_list[0].endswith("\""):
                word_list[0] = eval(word_list[0])

            else:
                word_list[0] = eval(word_list[0] + "\"")
            # print(word_list)
            if "|" not in word_list and word_list[0] in command_task4:
                ans.append(" ".join(word_list).strip('(').strip('(,)'))
            if "|" in word_list:
                if word_list[0] in command_task4:
                    ans.append(" ".join(word_list[:word_list.index("|")]).strip('(,)'))
                if word_list[word_list.index("|") + 1] in command_task4:
                    ans.append(" ".join(word_list[word_list.index("|") + 1:]).strip('(,)'))
            if word_list[0] not in command_task4:
                other.append(" ".join(word_list).strip('(').strip('(,)'))
        # print(command_string)
    for a in ans:
        while a[-1] in ' (,\\%':
            a = a[:-1]
        if a.count('(') == a.count(')') + 1:
            a = a + ')'
        if a.count('"') % 2 == 1:
            a = a.replace('"','')
        if a.count("'") % 2 == 1:
            a = a.replace("'",'')
        print(a)
    print("The commands that do not come with the operating system include:")
    for b in other:
        while b[-1] in ' (,\\%':
            b = b[:-1]
        if b.count('(') == b.count(')') + 1:
            b = b + ')'
        if b.count('"') % 2 == 1:
            b = b.replace('"','')
        if b.count("'") % 2 == 1:
            b = b.replace("'",'')
        print(b)
    return ans, other

