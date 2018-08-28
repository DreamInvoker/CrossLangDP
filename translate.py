from googletrans import Translator
import goslate
import time
from printProcess import show
import datetime


gs = goslate.Goslate(service_urls=['http://translate.google.cn'])

translator = Translator(service_urls=['translate.google.cn'], timeout=30,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")


def translate(source, src_lan, tgt_lan='en'):
    text = translator.translate(source, src=src_lan, dest=tgt_lan).text
    # text = gs.translate(source,tgt_lan,src_lan)
    time.sleep(1)
    return text


def split(word):
    return str(word).replace('_', ' ')


def process_align(src, tgt, prefix, lan):
    with open(file=src, mode='r', encoding='utf-8') as f:
        with open(file=tgt, mode='w', encoding='utf-8') as output:
            lines = f.readlines()
            start = datetime.datetime.now()
            print("Process {} ---> {} start at {}.".format(src, tgt, start))
            total = len(lines)
            c = 0
            for line in lines:
                c += 1
                show(c, total, interval=datetime.datetime.now() - start,
                     DoneInfo='Process {} ---> {} finished at {}.'.format(src, tgt, datetime.datetime.now()))
                info = line.strip().split('\t')
                title = split(info[0].strip().split(prefix)[1].strip())
                rs = translate(title, lan)
                output.write("{}{}\t{}\n".format(prefix, rs, split(info[1])))

def process_rel(src, tgt, prefix, prefix_pred, lan):
    with open(file=src, mode='r', encoding='utf-8') as f:
        with open(file=tgt, mode='w', encoding='utf-8') as output:
            lines = f.readlines()
            start = datetime.datetime.now()
            print("Process {} ---> {} start at {}.".format(src, tgt, start))
            total = len(lines)
            c = 0
            for line in lines:
                c += 1
                show(c, total, interval=datetime.datetime.now() - start,
                     DoneInfo='Process {} ---> {} finished at {}.'.format(src, tgt, datetime.datetime.now()))
                info = line.strip().split('\t')
                sub = info[0].strip()
                title = split(sub.split(prefix)[1].strip())
                rs = translate(title, lan)
                sub = "{}{}".format(prefix, split(rs))

                pred = info[1].strip()
                predicate = split(pred.split(prefix_pred)[1].strip())
                rs = translate(predicate, lan)
                pred = "{}{}".format(prefix_pred, split(rs))

                obj = info[2].strip()
                o_bject = split(obj.split(prefix)[1].strip())
                rs = translate(o_bject, lan)
                obj = "{}{}".format(prefix, split(rs))

                output.write("{}\t{}\t{}\n".format(sub, pred, obj))


if __name__ == '__main__':
    # print(translate("United States Army", 'fr'))
    # process_align('fr/ent_ILLs', 'fr/translated/ent_ILLs', 'http://fr.dbpedia.org/resource/', 'fr')
    # process_align('ja/ent_ILLs', 'ja/translated/ent_ILLs', 'http://ja.dbpedia.org/resource/', 'ja')

    process_align('zh/ent_ILLs', 'zh/translated/ent_ILLs', 'http://zh.dbpedia.org/resource/', 'zh-cn')
    process_rel('zh/zh_rel_triples', 'zh/translated/zh_rel_triples', 'http://zh.dbpedia.org/resource/',
                'http://zh.dbpedia.org/property/', 'zh-cn')
    process_rel('fr/fr_rel_triples', 'fr/translated/fr_rel_triples', 'http://fr.dbpedia.org/resource/',
                'http://fr.dbpedia.org/property/', 'fr')
    process_rel('ja/ja_rel_triples', 'ja/translated/ja_rel_triples', 'http://ja.dbpedia.org/resource/',
                'http://ja.dbpedia.org/property/', 'ja')
