"""
    跨语言数据预处理

    数据来源：

        跨语言属性三元组数据 [xx_att_triples]
"""
from printProcess import show
import time
import datetime

# 一、定义源文件路径
base = "./sourceData/"
path1 = base + "en_att_triples"
path2 = base + "zh_att_triples"

# 二、定义输出文件路径
output1 = base + "en_att_triples_proccessed"
output2 = base + "zh_att_triples_proccessed"

# 三、处理源文件
"""
以下是源文件中的一行
<http://zh.dbpedia.org/resource/日本國家足球隊> <http://zh.dbpedia.org/property/age> "1989-11-12"^^<http://www.w3.org/2001/XMLSchema#date> .
经处理后得到：日本國家足球隊  age 1989-11-12  date

注：
    1. 每行格式：实体的title    属性名    属性值  属性类型
    2. 每行中的内容以制表符\t分隔
    3. 如果这一行的属性值为字符串类型，则丢弃。比如以@en、@zh结尾的
"""


def splitFile(input_file, output_file, entity_prefix, string_mark, split_char):
    """
        处理att文件
    :param input_file:  输入文件地址
    :param output_file:     输出文件地址
    :param entity_prefix:   实体前缀
    :param string_mark:     字符类型属性值的标志
    :param split_char:  每行分隔符
    :return:
    """
    print('Start to process {} ......'.format(input_file))

    output = open(output_file, 'w', encoding='utf-8')
    output.write('title\t\t属性名\t\t属性值\t\t属性类型\n')

    with open(file=input_file, mode='r', encoding='utf-8') as f:
        start = datetime.datetime.now()
        lines = f.readlines()
        total = len(lines)
        c = 0
        for line in lines:
            c += 1
            show(c, total, interval=datetime.datetime.now() - start, DoneInfo='Process {} finished.'.format(input_file))
            line = line.strip()
            if line == '':
                continue

            info = line.split(sep=split_char, maxsplit=2)

            # if c >= 2493:
            #     print("breakpoint")
            raw_value_temp = info[2].strip()[::-1].split('. ', maxsplit=1)
            if len(raw_value_temp) < 2:
                raw_value_temp = raw_value_temp[0].split('.', maxsplit=1)
            raw_value = raw_value_temp[1][::-1].strip()
            if raw_value.endswith(string_mark):
                continue

            raw_title = info[0]
            raw_property = info[1]

            title_processed = raw_title.strip().split(entity_prefix)[1].split('>')[0].strip()
            property_processed = raw_property[::-1].split('/', maxsplit=1)[0].split('>')[1][::-1]
            temp = raw_value.split('"', maxsplit=2)
            if len(temp) == 1:
                continue
            value_processed = temp[1]
            property_type = temp[2]

            # output.write(
            #     title_processed + '\t\t' + property_processed + '\t\t' + value_processed + '\t\t' + property_type + '\n')
            output.write(title_processed+'\t\t'+property_processed+'\t\t'+value_processed+'\n')

    output.close()


if __name__ == '__main__':
    # en
    splitFile(input_file=path1, output_file=output1, entity_prefix='<http://dbpedia.org/resource/', string_mark='@en',
              split_char=' ')
    # zh
    splitFile(input_file=path2, output_file=output2, entity_prefix='<http://zh.dbpedia.org/resource/',
              string_mark='@zh',
              split_char=' ')
