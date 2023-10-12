import sys
import collections
import tqdm

_DICT = collections.defaultdict(lambda: collections.defaultdict(int))
_DICT_composed = collections.defaultdict(int)

def extract_adverbs_range(sentence, k):
    
    
    sentence_list = ["_"]+list(sorted(sentence.items()))
    # print(sentence_list)
    for tok_id, token in sentence.items():
        if token["fpos"] == "V":
            left_ctx = sentence_list[max(1, tok_id-k):tok_id]
            right_ctx = sentence_list[tok_id+1:min(len(sentence_list)+1, tok_id+k)]
            
            adverb_found = False
            spre = ''
            for _, ltoken in left_ctx:
                if ltoken["pos"] == "B":
                    adverb_found = True
                spre += ltoken['lemma']+"_"+ltoken['pos']+" "
            
            spost = ''
            for _, rtoken in right_ctx:
                if rtoken["pos"] == "B":
                    adverb_found = True
                spost += rtoken['lemma']+"_"+rtoken['pos']+" "
            
            if adverb_found: 
                print(spre, "\t", token['lemma']+"_"+token["pos"], "\t", spost)
            


def extract_composed_nouns(sentence):
    for tok_id, token in sentence.items():
        if token["fpos"] == "S":
            if "-" in token["lemma"]:
                _DICT_composed[token["lemma"]]+=1
                
    
    
            
def extract_adverbs_synrel(sentence, sentence_graph):
    
    for tok_id, token in sentence.items():
        if token["fpos"] == "V":
        # if token["fpos"] == "S":
            # print(token)
            # print(sentence_graph[tok_id])
            dependants = [(t_id, t) for t_id, t in sentence.items() if t_id in sentence_graph[tok_id] and t["pos"] == "B"]
            if len(dependants) > 0:
                
                spre = ' '
                spost = ' '
                
                for d_id, d in dependants:
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
                # extract_adverbs_synrel(processed_sentence, sentence_graph)
                extract_composed_nouns(processed_sentence)
                # input()
            sentence = []



# for token in _DICT:

    # for key, value in _DICT[token].items():
       
        # occ = value
        # spre, spost = key
    
        # print(occ, "\t", spre, "\t", token, "\t", spost)
        
        
for token in _DICT_composed:
    print(_DICT_composed[token], "\t", token)