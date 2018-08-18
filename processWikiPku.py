import mysql.connector
from printProcess import show
import datetime

def process(cursor, sql, output):
    cursor.execute(sql)
    a = cursor.fetchall()
    start = datetime.datetime.now()
    output_dict = {}
    total = len(a) - 1
    c = 0
    for property_name, objectType, value in a:
        # print("{}\t{}\t{}".format(property_name, objectType,value))
        c+=1
        show(c, total, interval=datetime.datetime.now() - start,
             DoneInfo='Process finished.')
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
    '''
    wiki_conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='icstwip',
                                        database='JWPL_zh_050602')
    wiki_cursor = wiki_conn.cursor()
    process(wiki_cursor, ' select predicate, objectType, value from tripleValue ',
            'results/wiki_result')
    wiki_conn.close()
    wiki_cursor.close()
    '''

    pku_conn = mysql.connector.connect(host='59.108.48.35', port='3306', user='root', password='icstwip',
                                       database='knowledgeGift')
    pku_cursor = pku_conn.cursor()
    # pku_cursor.execute(' select predicate, objectType, value from tripleValue ', 'results/pku_result ')
    # a = pku_cursor.fetchall()
    process(pku_cursor, ' select predicate, objectType, value from tripleValue ', 'results/pku_result')
    pku_conn.close()
    pku_cursor.close()
