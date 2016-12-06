# coding:utf-8

import sqlite3


def load_market_groups():
    file_market_groups = open('MarketGroups.txt', 'r')
    lines_market_groups = file_market_groups.readlines()
    file_market_groups.close()
    return lines_market_groups


def load_fitting_shiptypes():
    file_fitting_shiptypes = open('FittingShipTypes.txt', 'r')
    lines_fitting_shiptypes = file_fitting_shiptypes.readlines()
    file_fitting_shiptypes.close()
    return lines_fitting_shiptypes


def load_items():
    file_items = open('ItemsNonFiltered.txt', 'r')
    lines_items = file_items.readlines()
    file_items.close()
    return lines_items


def get_pairs(line):
    return line.strip('\n\r').split(',')


def translate_market_groups(cursor, lines_market_groups):
    for i in range(len(lines_market_groups)):
        each_pair = get_pairs(lines_market_groups[i])
        sql = "update invmarketgroups set marketGroupName='{0}({1})' where marketGroupName='{0}'".format(
            each_pair[0], each_pair[1])
        cursor.execute(sql)


def translate_fitting_shiptypes(cursor, lines_fitting_shiptypes):
    for i in range(len(lines_fitting_shiptypes)):
        each_pair = get_pairs(lines_fitting_shiptypes[i])
        sql = "update invgroups set groupName='{0}({1})' where groupName='{0}'".format(
            each_pair[0], each_pair[1])
        cursor.execute(sql)


def translate_items(cursor, lines_items):
    for i in range(len(lines_items)):
        each_pair = get_pairs(lines_items[i])
        sql = "update invtypes set typeName='{0}({1})' where typeName='{0}'".format(
            each_pair[0], each_pair[1])
        cursor.execute(sql)


def main():

    # 加载market groups
    lines_market_groups = load_market_groups()

    # 加载fitting ship types
    lines_fitting_shiptypes = load_fitting_shiptypes()

    # 加载items
    lines_items = load_items()

    # 连接数据库
    conn = sqlite3.connect('eve.db')
    cursor = conn.cursor()

    # 翻译数据库中的market group
    translate_market_groups(cursor, lines_market_groups)

    # 翻译数据库中的fitting ship type
    translate_fitting_shiptypes(cursor, lines_fitting_shiptypes)

    # 翻译数据库中的item
    translate_items(cursor, lines_items)

    # 关闭数据库
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
