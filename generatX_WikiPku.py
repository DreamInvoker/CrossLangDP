import json
import mysql.connector
import datetime
from printProcess import show
import os
import sendSMS as sms


def getVectMapping(path):
    with open(file=path, mode='r', encoding='utf-8') as f:
        vect_mapping_dict = json.load(f)
        return vect_mapping_dict


def getPropertyNameList(path):
    with open(file=path, mode='r', encoding='utf-8') as f:
        return json.load(f)


def getTriples(cursor, sql, vect_map_dict, output):
    triple_dict = {}

    if os.path.exists(output):
        with open(output, 'r', encoding='utf-8') as f:
            return json.load(f)

    cursor.execute(sql)
    all_records = cursor.fetchall()
    start = datetime.datetime.now()
    total = len(all_records)
    c = 0
    for id, title, property_name, objectType, value in all_records:
        c += 1
        show(c, total, interval=datetime.datetime.now() - start,
             DoneInfo='Process finished.')
        num = 0.0
        if property_name in vect_map_dict:
            property_dict = dict(vect_map_dict[property_name])
            if value in property_dict:
                num = float(property_dict[value])
            else:
                continue
        else:
            continue
        tri_dict = {}
        props_list = []
        if id in triple_dict:
            tri_dict = dict(triple_dict[id])
            if property_name in tri_dict:
                props_list = list(tri_dict[property_name])
                props_list.append(num)
            else:
                props_list.append(num)
        else:
            props_list.append(num)

        tri_dict[property_name] = props_list
        triple_dict[id] = tri_dict
    if os.path.exists(output):
        os.remove(output)
    with open(file=output, mode='w', encoding='utf-8') as f:
        json.dump(triple_dict, f)
    return triple_dict


def generate(path, total, name_list, tri_dict1, tri_dict2, output):
    result = []
    filecount = 0
    name_list = list(name_list)
    with open(file=path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        start = datetime.datetime.now()
        total_count = len(lines) - 1
        c = 0
        for line in lines:
            filecount += 1
            c += 1
            if filecount == 1:
                continue
            interval = datetime.datetime.now() - start
            show(c - 1, total_count, interval=interval,
                 DoneInfo='Process finished.')
            if c - 1 % 10000 == 0:
                sms.send(msg='婷宝宝，生成X词向量的程序已经跑了{}个实体了～已用时：{}。'.format(c - 1, interval))
            num = 0.0
            array = [0.0] * total
            select_dict = {}

            info = line.strip().split("\t")
            mark = info[0]
            if mark.startswith('wiki'):
                select_dict = tri_dict1
            else:
                select_dict = tri_dict2

            wiki_pku_id = info[1]

            if wiki_pku_id not in select_dict:
                result.append(array)
                continue
            entity_dict = select_dict[wiki_pku_id]

            for key, value in entity_dict.items():
                if key not in name_list:
                    continue
                else:
                    index = name_list.index(key)
                    array[index] = float(sum(list(map(float, value))) / len(list(map(float, value))))

            result.append(array)

    with open(file=output, mode='w', encoding='utf-8') as f:
        f.write(str(filecount - 1))
        for rs in result:
            ls = list(map(str, rs))
            line = " ".join(ls)
            f.write('\n' + str(line))

    sms.send(msg='婷宝宝，生成Wiki--Pku的x.txt的程序已经跑完了～总用时：{}。快去看看吧～'.format(datetime.datetime.now() - start))


if __name__ == '__main__':
    # wiki
    wiki_vector_mapping = getVectMapping("./sourceData/wiki_json_filtered_normtogether_dict_zh.json")

    # pku
    pku_vector_mapping = getVectMapping("./sourceData/pku_json_filtered_normtogether_dict_zh.json")

    property_name_list = getPropertyNameList('./sourceData/repeatedType.json')

    count = len(property_name_list)

    sql = ' select pageId, subject, predicate, objectType, value from tripleValue '
    # wiki
    wiki_conn = mysql.connector.connect(host='59.108.48.35', port='3306', user='root', password='icstwip',
                                        database='JWPL_zh_050602')
    wiki_cursor = wiki_conn.cursor()
    wiki_triple_dict = getTriples(wiki_cursor, sql, wiki_vector_mapping,
                                  './results/wiki_entityTripleDict.json')

    # pku
    pku_conn = mysql.connector.connect(host='59.108.48.35', port='3306', user='root', password='icstwip',
                                       database='knowledgeGift')
    pku_cursor = pku_conn.cursor()
    pku_triple_dict = getTriples(pku_cursor, sql, pku_vector_mapping,
                                 './results/pku_entityTripleDict.json')

    # 可以修改函数，设置默认的短信接收人to
    # 电话号码前要加上+86
    # sms.send(msg='hello wyt!', to="+8618813092702")
    generate('./sourceData/x_test.txt', count, property_name_list, wiki_triple_dict, pku_triple_dict,
             './results/x.txt')
