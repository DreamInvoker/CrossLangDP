import mysql.connector


def process(cursor, sql, output):
    cursor.execute(sql)
    output_dict = {}
    for pageId, subject, property_name, objectType, value in cursor:
        print("{}\t{}\t{}\t{}\t{}".format(pageId, subject, property_name, objectType,value))
        property_value_list = []
        if objectType == '_metre':
            value = str(value).split('-')[0]
        if property_name in output_dict:
            property_value_list = list(output_dict[property_name])
            property_value_list.append(value)
        else:
            property_value_list.append(value)

        output_dict[property_name] = property_value_list

    with open(file=output, mode='w', encoding='utf-8') as f:
        for key, value in output_dict.items():
            f.write(key + "\t\t" + "\t".join(str(i) for i in list(value)) + "\n")


if __name__ == '__main__':
    wiki_conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='icstwip',
                                        database='JWPL_zh_050602')
    wiki_cursor = wiki_conn.cursor()
    process(wiki_cursor, ' select pageId, subject, predicate, objectType, value from tripleValue ',
            'results/wiki_result')
    wiki_conn.close()
    wiki_cursor.close()

    pku_conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='icstwip',
                                       database='knowledgeGift')
    pku_cursor = pku_conn.cursor()
    process(pku_cursor, ' select pageId, subject, predicate, objectType, value from tripleValue ', 'results/pku_result')
    pku_conn.close()
    pku_cursor.close()