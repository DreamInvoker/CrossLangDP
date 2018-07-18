from printProcess import show
import datetime

base = "./sourceData/"
path1 = base + "en_att_triples_proccessed"
path2 = base + "zh_att_triples_proccessed"

res_base = "./results/"
output1 = res_base + "en_att_triples_results"
output2 = res_base + "zh_att_triples_results"
output_type1 = res_base + "en_att_triples_type"
output_type2 = res_base + "zh_att_triples_type"


def process(input_file, output_file, output_type_file, spli_char):
    output_dict = {}
    output_type_dict = {}
    with open(file=input_file, mode='r', encoding='utf-8') as f:
        start = datetime.datetime.now()
        lines = f.readlines()
        total = len(lines) - 1
        c = 0
        for line in lines:
            if c == 0:
                c += 1
                continue
            c += 1
            show(c - 1, total, interval=datetime.datetime.now() - start,
                 DoneInfo='Process {} finished.'.format(input_file))
            info = line.split(spli_char)
            if len(info) == 0:
                continue

            entity = info[0]
            property_name = info[1]
            value = info[2]
            type = info[3]
            property_value_list = []
            property_type_list = []
            if property_name in output_dict:
                property_value_list = list(output_dict[property_name])
                property_type_list = list(output_type_dict[property_name])

                property_value_list.append(value)
                property_type_list.append(type)
            else:
                property_value_list.append(value)
                property_type_list.append(type)

            output_dict[property_name] = property_value_list
            output_type_dict[property_name] = property_type_list

    with open(file=output_file, mode='w', encoding='utf-8') as f:
        with open(file=output_type_file, mode='w', encoding='utf-8') as ftype:
            for key, value in output_dict.items():
                f.write(key + "\t\t" + "\t".join(str(i) for i in list(value))+"\n")
            for key, value in output_type_dict.items():
                ftype.write(key + "\t\t" + "\t".join(str(i) for i in list(value))+"\n")


if __name__ == '__main__':
    # en
    process(input_file=path1, output_file=output1, output_type_file=output_type1, spli_char='\t\t')
    # zh
    process(input_file=path2, output_file=output2, output_type_file=output_type2, spli_char='\t\t')
