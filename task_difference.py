from collections import defaultdict
def difference(start_command, start_command2, restart_command, restart_command2, stop_command, stop_command2, sys_command, sys_command2, ans, ans2, other, other2):
    start_command_list = []
    start_command2_list = []
    restart_command_list = []
    restart_command2_list = []
    stop_command_list = []
    stop_command2_list = []
    sys_command_list = []
    sys_command2_list = []
    for dir in start_command:
        start_command_list = start_command_list + start_command[dir]
    for dir in start_command2:
        start_command2_list = start_command2_list + start_command2[dir]
    for dir in restart_command:
        restart_command_list = restart_command_list + restart_command[dir]
    for dir in restart_command2:
        restart_command2_list = restart_command2_list + restart_command2[dir]
    for dir in stop_command:
        stop_command_list = stop_command_list + stop_command[dir]
    for dir in stop_command2:
        stop_command2_list = stop_command2_list + stop_command2[dir]
    for dir in sys_command:
        sys_command_list = sys_command_list + sys_command[dir]
    for dir in sys_command2:
        sys_command2_list = sys_command2_list + sys_command2[dir]
    start_command_set = set(start_command_list)
    start_command2_set = set(start_command2_list)
    restart_command_set = set(restart_command_list)
    restart_command2_set = set(restart_command2_list)
    stop_command_set = set(stop_command_list)
    stop_command2_set = set(stop_command2_list)
    sys_command_set = set(sys_command_list)
    sys_command2_set = set(sys_command2_list)
    ans_set = set(ans)
    ans2_set = set(ans2)
    other_set = set(other)
    other2_set = set(other2)
    start_set = start_command_set & start_command2_set
    restart_set = restart_command_set & restart_command2_set
    stop_set = stop_command_set & stop_command2_set
    sys_set = sys_command_set & sys_command2_set
    ans_same_set = ans_set & ans2_set
    other_same_set = other_set & other2_set
    start_diff_set = start_command_set - start_set
    start_diff_set2 = start_command2_set - start_set
    restart_diff_set = restart_command_set - restart_set
    restart_diff_set2 = restart_command2_set - restart_set
    stop_diff_set = stop_command_set - stop_set
    stop_diff_set2 = stop_command2_set - stop_set
    sys_diff_set = sys_command_set - sys_set
    sys_diff_set2 = sys_command2_set - sys_set
    ans_diff_set = ans_set - ans_same_set
    ans_diff_set2 = ans2_set - ans_same_set
    other_diff_set = other_set - other_same_set
    other_diff_set2 = other2_set - other_same_set
    with open("diff.txt", 'w') as f:
        f.write("\n------This is the same start command------\n")
        f.write('\n'.join(str(e) for e in list(start_set)))
        f.write("\n------This is the different start command in rpm1------\n")
        f.write('\n'.join(str(e) for e in list(start_diff_set)))
        f.write("\n------This is the different start command in rpm2------\n")
        f.write('\n'.join(str(e) for e in list(start_diff_set2)))

        f.write("\n------This is the same restart command------\n")
        f.write('\n'.join(str(e) for e in list(restart_set)))
        f.write("\n------This is the different restart command in rpm1------\n")
        f.write('\n'.join(str(e) for e in list(restart_diff_set)))
        f.write("\n------This is the different restart command in rpm2------\n")
        f.write('\n'.join(str(e) for e in list(restart_diff_set2)))

        f.write("\n------This is the same stop command------\n")
        f.write('\n'.join(str(e) for e in list(stop_set)))
        f.write("\n------This is the different stop command in rpm1------\n")
        f.write('\n'.join(str(e) for e in list(stop_diff_set)))
        f.write("\n------This is the different stop command in rpm2------\n")
        f.write('\n'.join(str(e) for e in list(stop_diff_set2)))

        f.write("\n------This is the same all system command------\n")
        f.write('\n'.join(str(e) for e in list(sys_set)))
        f.write("\n------This is the different all system command in rpm1------\n")
        f.write('\n'.join(str(e) for e in list(sys_diff_set)))
        f.write("\n------This is the different all system command in rpm2------\n")
        f.write('\n'.join(str(e) for e in list(sys_diff_set2)))

        f.write("\n------This is the same os system command------\n")
        f.write('\n'.join(str(e) for e in list(ans_same_set)))
        f.write("\n------This is the different os system command in rpm1------\n")
        f.write('\n'.join(str(e) for e in list(ans_diff_set)))
        f.write("\n------This is the different os system command in rpm2------\n")
        f.write('\n'.join(str(e) for e in list(ans_diff_set2)))

        f.write("\n------This is the same rpm system command------\n")
        f.write('\n'.join(str(e) for e in list(other_same_set)))
        f.write("\n------This is the different rpm system command in rpm1------\n")
        f.write('\n'.join(str(e) for e in list(other_diff_set)))
        f.write("\n------This is the different rpm system command in rpm2------\n")
        f.write('\n'.join(str(e) for e in list(other_diff_set2)))

        f.close()

