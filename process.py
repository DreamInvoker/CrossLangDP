from printProcess import show
import datetime

base = "./sourceData/"
path1 = base + "en_att_triples_proccessed"
path2 = base + "zh_att_triples_proccessed"
path_fr_en = base + "fr_en_att_triples_proccessed"
path_fr = base + "fr_att_triples_proccessed"
path_ja_en = base + "ja_en_att_triples_proccessed"
path_ja = base + "ja_att_triples_proccessed"

res_base = "./results/"
output1 = res_base + "en_att_triples_results"
output2 = res_base + "zh_att_triples_results"
# output_type1 = res_base + "en_att_triples_type"
# output_type2 = res_base + "zh_att_triples_type"
output_fr_en = res_base + "fr_en_att_triples_results"
output_fr = res_base + "fr_att_triples_results"

output_ja_en = res_base + "ja_en_att_triples_results"
output_ja = res_base + "ja_att_triples_results"

def process(input_file, output_file, spli_char):
    output_dict = {}
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
            info = line.strip().split(spli_char)
            if len(info) == 0:
                continue

            entity = info[0]
            property_name = info[1]
            value = info[2]
            property_value_list = []
            if property_name in output_dict:
                property_value_list = list(output_dict[property_name])

                property_value_list.append(value)
            else:
                property_value_list.append(value)

            output_dict[property_name] = property_value_list

    with open(file=output_file, mode='w', encoding='utf-8') as f:
        for key, value in output_dict.items():
            f.write(key + "\t\t" + "\t".join(str(i) for i in list(value))+"\n")


if __name__ == '__main__':
    '''
    # en
    process(input_file=path1, output_file=output1, spli_char='\t\t')
    # zh
    process(input_file=path2, output_file=output2, spli_char='\t\t')
    '''
    # fr_en
    process(input_file=path_fr_en, output_file=output_fr_en, spli_char='\t\t')
    # fr
    process(input_file=path_fr, output_file=output_fr, spli_char='\t\t')

    # ja_en
    process(input_file=path_ja_en, output_file=output_ja_en, spli_char='\t\t')
    # ja
    process(input_file=path_ja, output_file=output_ja, spli_char='\t\t')