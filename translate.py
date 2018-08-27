from googletrans import Translator
import goslate
import time
gs = goslate.Goslate(service_urls=['http://translate.google.cn'])

# translator = Translator(service_urls=['translate.google.cn'],timeout=30)


def translate(source, src_lan, tgt_lan='en'):
    # text = translator.translate(source, src=src_lan, dest=tgt_lan).text
    text = gs.translate(source,tgt_lan,src_lan)
    time.sleep(3)
    return text

def split(word):
    return str(word).replace('_',' ')


def process_align(src, tgt, prefix, lan):
    with open(file=src, mode='r', encoding='utf-8') as f:
        with open(file=tgt, mode='w', encoding='utf-8') as output:
            lines = f.readlines()
            for line in lines:
                info = line.strip().split('\t')
                title = split(info[0].strip().split(prefix)[1].strip())
                rs = translate(title, lan)
                print("{}-->{}".format(title, rs))
                output.write("{}{}\t{}\n".format(prefix, rs, info[1]))

    print('Process {} ---> {} Finished.'.format(src, tgt))


def process_rel(src, tgt, prefix, prefix_pred, lan):
    with open(file=src, mode='r', encoding='utf-8') as f:
        with open(file=tgt, mode='w', encoding='utf-8') as output:
            lines = f.readlines()
            for line in lines:
                info = line.strip().split('\t')
                sub = info[0].strip()
                title = split(sub.split(prefix)[1].strip())
                rs = translate(title, lan)
                sub = "{}{}".format(prefix, rs)
                print("{}-->{}".format(title, rs))

                pred = info[1].strip()
                predicate = split(pred.split(prefix_pred)[1].strip())
                rs = translate(predicate, lan)
                pred = "{}{}".format(prefix_pred, rs)
                print("{}-->{}".format(predicate, rs))

                obj = info[2].strip()
                o_bject = split(obj.split(prefix)[1].strip())
                rs = translate(o_bject, lan)
                obj = "{}{}".format(prefix, rs)
                print("{}-->{}".format(o_bject, rs))

                output.write("{}\t{}\t{}\n".format(sub, pred, obj))

    print('Process {} ---> {} Finished.'.format(src, tgt))


if __name__ == '__main__':
    print(translate("United States Army", 'fr'))

    '''
    process_align('fr/ent_ILLs', 'fr/translated/ent_ILLs', 'http://fr.dbpedia.org/resource/', 'fr')
    process_rel('fr/fr_rel_triples', 'fr/translated/fr_rel_triples', 'http://fr.dbpedia.org/resource/',
                'http://fr.dbpedia.org/property/' 'fr')
    process_align('ja/ent_ILLs', 'ja/translated/ent_ILLs', 'http://ja.dbpedia.org/resource/', 'ja')
    process_rel('ja/ja_rel_triples', 'ja/translated/ja_rel_triples', 'http://ja.dbpedia.org/resource/',
                'http://ja.dbpedia.org/property/' 'ja')
    '''


