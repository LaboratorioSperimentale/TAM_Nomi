import collections
import tqdm
import utils

def extract_detADVN(filename, source, file_id):
    freqs = collections.defaultdict(int)


    for sentence in tqdm.tqdm(utils.read(filename, source)):
        candidates = []
        # print(sentence)
        for tok_id, token in enumerate(sentence.sentence):
            if token.pos == "ADV" and \
                tok_id > 2 and \
                    tok_id < len(sentence.sentence)-1:
                candidates.append(tok_id)

        # print(candidates)
        # input()

        for c_id in candidates:

            if sentence.sentence[c_id+1].pos == "NOUN":

                if sentence.sentence[c_id-1].pos == "DET":
                    # freqs[(sentence.sentence[c_id-1].lemma+"_"+sentence.sentence[c_id-1].pos,
                    #        sentence.sentence[c_id].lemma+"_"+sentence.sentence[c_id].pos,
                    #        sentence.sentence[c_id+1].lemma+"_"+sentence.sentence[c_id+1].pos)] += 1
                    freqs[(sentence.sentence[c_id].lemma+"_"+sentence.sentence[c_id].pos,
                           sentence.sentence[c_id+1].lemma+"_"+sentence.sentence[c_id+1].pos)] += 1

                if sentence.sentence[c_id-2].pos == "DET" and sentence.sentence[c_id-1].pos in ["ADV", "ADJ"]:
                    # freqs[(sentence.sentence[c_id-2].lemma+"_"+sentence.sentence[c_id-2].pos,
                    #        sentence.sentence[c_id-1].lemma+"_"+sentence.sentence[c_id-1].pos,
                    #        sentence.sentence[c_id].lemma+"_"+sentence.sentence[c_id].pos,
                    #        sentence.sentence[c_id+1].lemma+"_"+sentence.sentence[c_id+1].pos)] += 1
                    freqs[(sentence.sentence[c_id-1].lemma+"_"+sentence.sentence[c_id-1].pos,
                           sentence.sentence[c_id].lemma+"_"+sentence.sentence[c_id].pos,
                           sentence.sentence[c_id+1].lemma+"_"+sentence.sentence[c_id+1].pos)] += 1

    with open(f"../output/{source}_{file_id}.txt", "w", encoding="utf-8") as fout:
        for key, f in sorted(freqs.items(), key=lambda x: -x[1]):
            if f > 0:
                print(f"{f}\t{' '.join(key)}", file=fout)


def extract_advN(filename, source, file_id):
    freqs = collections.defaultdict(int)

    for sentence in tqdm.tqdm(utils.read(filename, source)):
        for token in sentence.sentence:
            if token.pos == "NOUN" and "-" in token.form:
                freqs[token.form] += 1

    with open(f"../output/{source}_{file_id}.txt", "w", encoding="utf-8") as fout:
        for key, f in sorted(freqs.items()):
            if f > 3:
                print(f"{f}\t{key}", file=fout)


def extract_advN_ctx(filename, source, file_id, adj_files):

    ctx = 10

    for sentence in tqdm.tqdm(utils.read(filename, source)):
        candidates = []
        for token_n, token in enumerate(sentence.sentence):

            if token.form in adj_files:
                candidates.append(token_n)

            # if token.form == "pseudo-vincoli":
            #     print([x.form for x in sentence.sentence])
            #     print(candidates)
            #     input()

        for candidate in candidates:
            sentence_portion_left = sentence.sentence[max(0, candidate-ctx):candidate]
            sentence_portion_right = sentence.sentence[candidate+1:min(len(sentence.sentence), candidate+ctx+1)]

            ctx_left = " ".join([token.form for token in sentence_portion_left])
            candidate_str = sentence.sentence[candidate].form
            ctx_right = " ".join([token.form for token in sentence_portion_right])

            print(f"{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=adj_files[candidate_str])

    # with open(f"../output/{source}_{file_id}.txt", "w", encoding="utf-8") as fout:
    #     for key, f in sorted(freqs.items()):
    #         if f > 3:
    #             print(f"{f}\t{key}", file=fout)




if __name__ == "__main__":
    import tqdm
    import csv

    files = {}
    with open("../data/input_files.txt") as fin:
        for line in fin:

            line = line.strip()
            # print(line)
            if not line == "":
                name, file_id, location = line.split()
                if not name in files:
                    files[name] = []
                files[name].append((file_id, location))

    adj_list = {}
    with open("../ntrattino.csv") as fin:
        reader = csv.reader(fin)
        for line in reader:
            line = line[0].strip().split("\t")

            if len(line) == 8:
                adj_list[line[5]] = "servecontesto"
            else:
                if line[-1] == "-":
                    adj_list[line[5]] = "no"
                else:
                    adj_list[line[5]] = "si"


    adj_files = {}
    for adj in adj_list:
        adj_files[adj] = open(f"../output_ctxs/{adj_list[adj]}/{adj}.txt", "w")

    for name in files:
        print("Processing", name, "...")
        for file_id, filename in tqdm.tqdm(files[name]):
            # extract_advN(filename, name, file_id)
            # extract_detADVN(filename, name, file_id)
            extract_advN_ctx(filename, name, file_id, adj_files)

