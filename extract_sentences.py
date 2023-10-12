import collections
import sys
import tqdm

TAM_pre = set()
TAM_post = set()
other_pre = set()
other_post = set()
discordi_pre = set()
discordi_post = set()


_DICT = collections.defaultdict(lambda: collections.defaultdict(int))
_DICT_composed = collections.defaultdict(int)


with open("data/TAM.concordi.pre") as fin:
    for line in fin:
        line = line.strip().split("\t")
        
        TAM_pre.add(line[0].lower())

with open("data/TAM.concordi.post") as fin:
    for line in fin:
        line = line.strip().split("\t")
        
        TAM_post.add(line[0].lower())
        
with open("data/other.concordi.pre") as fin:
    for line in fin:
        line = line.strip().split("\t")
        
        other_pre.add(line[0].lower())

with open("data/other.concordi.post") as fin:
    for line in fin:
        line = line.strip().split("\t")
        
        other_post.add(line[0].lower())
        
with open("data/discordi.pre") as fin:
    for line in fin:
        line = line.strip().split("\t")
        
        discordi_pre.add(line[0].lower())

with open("data/discordi.post") as fin:
    for line in fin:
        line = line.strip().split("\t")
        
        discordi_post.add(line[0].lower())


        
# with open("data/noun_adverbs.full.synrel") as fin:
#     for line in fin:
#         line = line.strip().split("\t")
        
#         occ = int(line[0])
#         adv_pre = ""
#         adv_post = ""
#         noun = ""
        
#         adv_pre = line[1].lower()
#         noun = line[2].lower()
        
#         if len(line)>3:
#             adv_post = line[3].lower()
        
#         print(occ, adv_pre, noun, adv_post)
#         input()
        
        
def print_linear_sentence(sentence_dict, adv_id, noun_id):
    pos_from = adv_id-5
    pos_to = noun_id+5
    
    linear_sentence = [tok["form"] for tok_id, tok in sentence_dict.items()]
    pos_from = max(pos_from, 0)
    pos_to = min(pos_to, len(linear_sentence))
    
    print("SENTENCE", sentence_dict[adv_id]["form"], "---", sentence_dict[noun_id]["form"], "---", adv_id-noun_id)
    print(linear_sentence[pos_from:pos_to])
    input()
    

        
def extract_adverbs_synrel(sentence, sentence_graph):
    
    for tok_id, token in sentence.items():
        # if token["fpos"] == "V":
        if token["fpos"] == "S":
            # print(token)
            # print(sentence_graph[tok_id])
            dependants = [(t_id, t) for t_id, t in sentence.items() if t_id in sentence_graph[tok_id] and t["pos"] == "B"]
            
            # print(dependants)
            # input()
            
            if len(dependants) > 0:
                
                spre = ' '
                spost = ' '
                
                for d_id, d in dependants:
                    
                    if d["lemma"].lower()+"_b" in TAM_pre:
                        print_linear_sentence(sentence, d_id, tok_id)
                    
                    if d_id < tok_id:
                        spre += d["lemma"]+"_"+d["pos"]+" "
                    if d_id > tok_id:
                        spost += d["lemma"]+"_"+d["pos"]+" "
                
                
                _DICT[token['lemma']+"_"+token["pos"]][(spre, spost)] += 1
                # print(_DICT)
                # input()
                # print(spre, "\t", token['lemma']+"_"+token["pos"], "\t", spost)
                # input()


def process_sentence(sentence):
    
    sentence_dict = {}
    sentence_graph = collections.defaultdict(list)
    for token in sentence:
        id, form, lemma, pos, fpos, morph, head, synrel, *_ = token
        id = int(id)
        try:
            head = int(head)
            
            sentence_dict[id] = {'form':form,
                                'lemma':lemma,
                                'pos':pos,
                                'fpos':fpos,
                                'head':head,
                                'synrel':synrel}
            sentence_graph[head].append(id)
        
        except:
            sentence_dict[id] = {'form':'',
                    'lemma':'',
                    'pos':'',
                    'fpos':'',
                    'head':'',
                    'synrel':''}
            sentence_graph[head].append(id)
        
    return sentence_dict, sentence_graph
        


with open(sys.argv[1]) as fin:
    sentence = []
    for line in tqdm.tqdm(fin):
        line = line.strip().split("\t")
        # print(line)
        
        if len(line) > 1:
            sentence.append(line)
        else:
            if len(sentence) > 0:
                processed_sentence, sentence_graph = process_sentence(sentence)

                # extract_adverbs_range(processed_sentence, 5)
                extract_adverbs_synrel(processed_sentence, sentence_graph)
                # extract_composed_nouns(processed_sentence)
                # input()
            sentence = []



# for token in _DICT:

    # for key, value in _DICT[token].items():
       
        # occ = value
        # spre, spost = key
    
        # print(occ, "\t", spre, "\t", token, "\t", spost)
        
        
for token in _DICT_composed:
    print(_DICT_composed[token], "\t", token)