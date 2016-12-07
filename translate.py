# coding:utf-8

import sqlite3
import os

list_table_column = [("invmarketgroups", "marketGroupName"),
                     ("invgroups", "groupName"), ("invtypes", "typeName")]


def load_files_path(locate_path, list_files_path):
    #abs_path = os.path.abspath(locate_path)
    list_three_main = os.walk(locate_path)
    for root, dirs, files in list_three_main:
        for each in files:
            if os.path.splitext(each)[1][1:] == "txt":
                list_files_path.append(os.path.join(root, each))


def get_pairs(line):
    return line.strip('\n\r').split(',')


def load_file(file_path):
    file_to_read = open(file_path, 'r')
    lines = file_to_read.readlines()
    file_to_read.close()
    if len(lines) > 2:
        title_pair = get_pairs(lines[0])
        if title_pair[0] == "flag" and title_pair[1] == "ok":
            table_col = get_pairs(lines[1])
            for table_name,column_name in list_table_column:
                if table_col[0] == table_name and table_col[1] == column_name:
                    return lines
                


def translate_lines(cursor, lines):
    table_col = get_pairs(lines[1])
    table_name = table_col[0]
    column_name = table_col[1]
    for i in range(2, len(lines)):
        if lines[i][0:1] != "#":
            each_pair = get_pairs(lines[i])
            sql = "update {2} set {3}='{0}({1})' where {3}='{0}'".format(
                each_pair[0], each_pair[1], table_name, column_name)
            cursor.execute(sql)


def main():

    # 读取汉化文件路径
    list_files_path = []
    locate_path = 'locate'
    load_files_path(locate_path, list_files_path)

    # 加载数据
    list_lines = []
    for each_file_path in list_files_path:
        data = load_file(each_file_path)
        if data is not None:
            list_lines.append(data)

    # 连接数据库
    conn = sqlite3.connect('eve.db')
    cursor = conn.cursor()

    # 翻译数据库中的market group
    for each_lines in list_lines:
        translate_lines(cursor, each_lines)

    # 关闭数据库
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
