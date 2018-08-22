wiki_pred_list = []
wiki_freq_list = []
with open(file='./sourceData/zh_pred_seq.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    c = 0
    for line in lines:
        if c == 0:
            c += 1
            continue
        info = line.split('\t')
        pred = info[0].strip()
        freq = int(info[1].strip())
        wiki_pred_list.append(pred)
        wiki_freq_list.append(freq)

pku_pred_list = []
pku_freq_list = []
with open(file='./sourceData/en_pred_seq.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    c = 0
    for line in lines:
        if c == 0:
            c += 1
            continue
        info = line.split('\t')
        pred = info[0].strip()
        freq = int(info[1].strip())
        pku_pred_list.append(pred)
        pku_freq_list.append(freq)

repeatedPred = []

for pred in wiki_pred_list:
    if pred in pku_pred_list:
        if pred not in repeatedPred:
            repeatedPred.append(pred)

for pred in pku_pred_list:
    if pred in wiki_pred_list:
        if pred not in repeatedPred:
            repeatedPred.append(pred)

print(len(repeatedPred))
count = 0
final = []
for item in repeatedPred:
    wiki_freq = wiki_freq_list[wiki_pred_list.index(item)]
    pku_freq = pku_freq_list[pku_pred_list.index(item)]
    if wiki_freq >= 100 and pku_freq >= 100:
        print(item,wiki_freq,pku_freq)
        final.append(item)
        count += 1

print(count)

import json
with open(file='./sourceData/repeatedType_100_zh_en.json',mode='w',encoding='utf-8') as f:
    json.dump(final,f)
