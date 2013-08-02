#!/usr/bin/python
#coding=utf8
# 自定义函数库

import re # regular expression

def menu():
    print 'Welcome to use `hynmath` package for Python.'
    print 'All functions is listed as follows:'
    print '# get_content -- get content from a MarkDown file'
    print '# get_title -- get title for keyword `topic` from a MarkDown file'

# get_content -- get content from a MarkDown file
def get_content(topic, filename, istitle=True, numdepth=7):
    # 定义行的层级关系:
    # 1  @@      最高级, 用于输出全部目录
    # 2  @       一个文件夹, 一本书
    # 3  #       一篇文章, 一章, 一个 chapter
    # 4  ##      一节, 一个 section
    # 5  ###     一小节, 一个 subsection
    # 6  ####    一个小小节, 一个 subsubsection
    # 7  #####   一个最小词条, 一个段落, 一个 paragraph
    # 8  不带标题  普通内容
    level_arr = ['@@','@','#','##','###','####','#####']
    # 对层级关系序列化
    level_map = {}
    level_idx = 0
    for element in level_arr:
        level_idx += 1
        level_map[element] = level_idx
    pattern = re.compile(r'^(@@|@|#|##|###|####|#####)[^@#]')

    fid = open(filename,'r')
    level_target = 0        # 目标块的标题等级
    flag_sub_target = False # 是否存在子标题
    result = ''             # 结果输出字符串
    for line in fid:
        # 获取当前行的等级
        m = pattern.match(line)
        level_current = m and level_map[m.group(1)] or 8

        # 寻找主题所在的块
        if level_target == 0 and level_current <= 7:
            name = line.split("--")[0]
            if name.upper().find(topic.upper()) >= 0:
                level_target = level_current
                if istitle==True: result+=line
                continue

        # 输出主题下面的内容
        if level_target >= 1 and level_current == 8 and numdepth < 8 and flag_sub_target == False:
            result += line

        # 找到子主题, 只输出子主题的名称
        if level_target >= 1 and level_current <= 7:
            flag_sub_target = True

        if level_target >= 1 and level_current <= numdepth and level_current > level_target:
            result += line

        # 主题内容结束
        if level_target >= 1 and level_current <= level_target:
            break
    fid.close()
    return result

# get_title -- get title for keyword `topic` from a MarkDown file
def get_title(topic, filename):
    level_arr = ['@@','@','#','##','###','####','#####']
    level_map = {}
    level_idx = 0
    for element in level_arr:
        level_idx += 1
        level_map[element] = level_idx
    pattern = re.compile(r'^(@@|@|#|##|###|####|#####)[^@#]')

    fid = open(filename,'r')
    title_target = ""
    result = ''
    for line in fid:
        m = pattern.match(line)
        level_current = m and level_map[m.group(1)] or 8

        if level_current <= 7:
            title_current = line
        if line.upper().find(topic.upper()) >= 0 and title_current != title_target:
            title_target = title_current
            result += title_target
    fid.close()
    return result