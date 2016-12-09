# coding:utf-8


def load_po():
    file_po = open('locate/po/pyfa.po', 'r')
    lines_po = file_po.readlines()
    file_po.close()
    return lines_po


def find_first_dataline(lines_po):
    for i in range(len(lines_po)):
        text_line = lines_po[i]
        if 'msgid' in text_line and len(text_line) > 9:
            return i


def get_word(each_line):
    first_num = each_line.find('"')
    return each_line[first_num + 1:].rstrip('"\n')


def main():
    lines_po = load_po()
    start_line_num = find_first_dataline(lines_po)
    file_tmp = open('locate/po/ItemsNonFiltered.tmp','w')
    for i in range(start_line_num, len(lines_po), 3):
        print i
        name_en = get_word(lines_po[i])
        name_cn = get_word(lines_po[i + 1])
        print >> file_tmp,"{0},{1}".format(name_en,name_cn).replace("'","''")
    file_tmp.flush()
    file_tmp.close()
        

if __name__ == '__main__':
    main()
