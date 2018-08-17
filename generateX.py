import json
import numpy as np
import  math


def getVectMapping(path):
    with open(file=path, mode='r', encoding='utf-8') as f:
        vect_mapping_dict = json.load(f)
        return vect_mapping_dict


def getPropertyNameList(path):
    with open(file=path, mode='r', encoding='utf-8') as f:
         return json.load(f)


def getTriples(path,vect_map_dict,output,split_char='\t\t'):
    triple_dict = {}
    with open(file=path,mode='r',encoding='utf-8') as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            if count == 0:
                count += 1
                continue

            info = line.strip().split(split_char)
            title = info[0].strip()
            property_name = info[1].strip()
            value = info[2].strip()
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
            if title in triple_dict:
                tri_dict = dict(triple_dict[title])
                if property_name in tri_dict:
                    props_list = list(tri_dict[property_name])
                    props_list.append(num)
                else:
                    props_list.append(num)

            else:
                props_list.append(num)

            tri_dict[property_name] = props_list
            triple_dict[title] = tri_dict

    return triple_dict

    # with open(file=output,mode='w',encoding='utf-8') as f:
    #     json.dump(triple_dict,f)


def generate(path,total,name_list, tri_dict1,tri_dict2, entity_prefix1,entity_prefix2,output,start_en=17136):
    result = []
    filecount = 0
    name_list = list(name_list)
    with open(file=path,mode='r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            filecount += 1
            if filecount == 1:
                continue

            array = [0.0] * total
            select_dict = {}
            entity_prefix = ''
            if filecount < start_en:
                select_dict = tri_dict1
                entity_prefix = entity_prefix1
            else:
                select_dict = tri_dict2
                entity_prefix = entity_prefix2

            title = line.strip().split(entity_prefix)[1]

            if title not in select_dict:
                result.append(array)
                continue
            entity_dict = select_dict[title]

            for key,value in entity_dict.items():
                if key not in name_list:
                    continue
                else:
                    index = name_list.index(key)
                    array[index] = float(sum(list(map(float,value)))/len(list(map(float,value))))

            result.append(array)

    with open(file=output,mode='w',encoding='utf-8') as f:
        f.write(str(filecount-1))
        for rs in result:
            ls = list(map(str, rs))
            line = " ".join(ls)
            f.write('\n'+str(line))




if __name__ == '__main__':
    # en
    en_vector_mapping = getVectMapping("./sourceData/en_json_e7_normtogether_dict.json")
    # zh
    zh_vector_mapping = getVectMapping("./sourceData/zh_json_e7_normtogether_dict.json")

    property_name_list = getPropertyNameList('./sourceData/repeatedType_10.json')

    count = len(property_name_list)

    # en
    en_triple_dict = getTriples('./sourceData/en_att_triples_proccessed',en_vector_mapping,'./results/en_entityTripleDict.json')

    # zh
    zh_triple_dict = getTriples('./sourceData/zh_att_triples_proccessed',zh_vector_mapping,'./results/zh_entityTripleDict.json')


    generate('./sourceData/x_20180720.txt',count,property_name_list,zh_triple_dict,en_triple_dict,'http://zh.dbpedia.org/resource/','http://dbpedia.org/resource/','./results/x.txt')


