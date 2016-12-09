# coding:utf-8

import sqlite3


def ship_types_extractor(cursor, categoryid=6):
    sql = ("select groupid,groupname from invgroups "
           "where categoryID = {0} "
           "order by groupname").format(categoryid)
    cursor.execute(sql)
    list_types = cursor.fetchall()
    return list_types


def items_dict_load(items_file_path):
    file_to_read = open(items_file_path, 'r')
    lines = file_to_read.readlines()
    file_to_read.close()
    dict_items = {}
    for each_line in lines:
        each_pair = each_line.strip('\n\r').split(',')
        dict_items[each_pair[0].replace("''", "'")] = each_pair[1]
    return dict_items


def items_execute(cursor, exec_file_path, list_types, dict_items):

    file_tmp = open(exec_file_path, 'w')

    for each_group in list_types:
        sql = ("select typeName from invtypes "
               "where groupID = {0} "
               "order by raceID,typeName").format(each_group[0])
        cursor.execute(sql)
        list_items_each_group = cursor.fetchall()
        if len(list_items_each_group) > 0:
            print >> file_tmp, "**********{0}**********".format(each_group[1])
            for each_item in list_items_each_group:
                if dict_items.has_key(each_item[0]):
                    print >> file_tmp, "{0},{1}".format(
                        each_item[0].encode('utf-8').replace("'", "''"), dict_items[each_item[0]])
                else:
                    print >> file_tmp, "{0},{1}".format(
                        each_item[0].encode('utf-8').replace("'", "''"), "")

    file_tmp.flush()
    file_tmp.close()


def main():

    # 连接数据库
    conn = sqlite3.connect('eve.db')
    cursor = conn.cursor()

    # 获取categoryID为6(name为ship)的group list
    list_types = ship_types_extractor(cursor)


    # 加载汉化物品字典
    dict_items = items_dict_load("locate/po/ItemsNonFiltered.tmp")

    # 分组输出items的name和namecn
    items_execute(cursor, 'locate/po/ShipsTypeby.tmp',
                  list_types, dict_items)

    # 关闭数据库
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
