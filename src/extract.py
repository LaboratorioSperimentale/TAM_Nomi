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

    ctx = 20

    for sentence in tqdm.tqdm(utils.read(filename, source)):
        candidates = set()
        for token_n, token in enumerate(sentence.sentence):

            if token.form in adj_files:
                candidates.add(token_n)


        for candidate in candidates:
            sentence_portion_left = sentence.sentence[max(0, candidate-ctx):candidate]
            sentence_portion_right = sentence.sentence[candidate+1:min(len(sentence.sentence), candidate+ctx+1)]

            ctx_left = " ".join([token.form for token in sentence_portion_left])
            candidate_str = sentence.sentence[candidate].form
            ctx_right = " ".join([token.form for token in sentence_portion_right])

            print(f"{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=adj_files[candidate_str])


def extract_advN_ctx_FINAL(filename, source, pref_files):

    ctx = 20

    for sentence in tqdm.tqdm(utils.read(filename, source)):
        candidates = set()
        for token_n, token in enumerate(sentence.sentence):
            if "-" in token.form and token.pos == "NOUN":

                pref, suff = token.form.split("-", 1)

                if pref in pref_files:
                    candidates.add((token_n, pref))


        for candidate in candidates:
            candidate, pref = candidate
            sentence_portion_left = sentence.sentence[max(0, candidate-ctx):candidate]
            sentence_portion_right = sentence.sentence[candidate+1:min(len(sentence.sentence), candidate+ctx+1)]

            ctx_left = " ".join([token.form for token in sentence_portion_left])
            candidate_str = sentence.sentence[candidate].form
            ctx_right = " ".join([token.form for token in sentence_portion_right])

            print(f"{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=pref_files[pref])



def extract_detADVN_ctx(filename, source, file_id, accepted_avs, adv_files):

    ctx = 20

    for sentence in tqdm.tqdm(utils.read(filename, source)):
        # check_print=False

        candidates = set()
        for tok_id, token in enumerate(sentence.sentence):
            if token.pos == "ADV" and token.form in accepted_avs and \
                tok_id > 2 and \
                    tok_id < len(sentence.sentence)-2:
                candidates.add(tok_id)
                # pos = [x.pos for x in sentence.sentence]
                # pos = ":".join(pos)
                # if "DET:ADV:NOUN" in pos:
                #     print([(x.form, x.pos) for x in sentence.sentence])
                #     print(candidates)
                #     check_print = True
                #     # input()


        for c_id in candidates:


            adv = sentence.sentence[c_id].form
            adv_str = adv
            to_print = False



            if sentence.sentence[c_id-1].pos == "DET":
                sentence_portion_left = sentence.sentence[max(0, c_id-1-ctx):c_id-1]

                if sentence.sentence[c_id+1].pos == "NOUN":
                    sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+2+ctx+1)]
                    occurrence = sentence.sentence[c_id-1:c_id+2]
                    noun = sentence.sentence[c_id+1].form
                    ngramtype = "DET ADV NOUN"

                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun ):
                        to_print = True

                    # else:
                    #     print(adv, noun)
                        # input()

                if sentence.sentence[c_id+1].pos == "ADJ" and sentence.sentence[c_id+2].pos == "NOUN":
                    sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
                    occurrence = sentence.sentence[c_id-1:c_id+3]
                    noun = sentence.sentence[c_id+2].form
                    ngramtype = "DET ADV ADJ NOUN"
                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun):
                        to_print = True
                    # else:
                    #     print(adv, noun)
                        # input()

                if sentence.sentence[c_id+1].pos == "ADV" and sentence.sentence[c_id+2].pos == "NOUN":
                    sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
                    occurrence = sentence.sentence[c_id-1:c_id+3]
                    noun = sentence.sentence[c_id+2].form
                    adv = adv + " " + sentence.sentence[c_id+1].form
                    adv_str = adv_str + "_" + sentence.sentence[c_id+1].form
                    ngramtype = "DET ADV NOUN"
                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun) and all(c.isalpha() or c in [" ", "-", "."] for c in adv):
                        to_print = True
                    # else:
                    #     print(adv, noun)
                        # input()


            if sentence.sentence[c_id-2].pos == "DET":
                sentence_portion_left = sentence.sentence[max(0, c_id-2-ctx):c_id-2]

                if sentence.sentence[c_id-1].pos == "ADJ" and sentence.sentence[c_id+1].pos == "NOUN":
                    sentence_portion_right = sentence.sentence[c_id+1:min(len(sentence.sentence), c_id+1+ctx+1)]
                    occurrence = sentence.sentence[c_id-2:c_id+2]
                    noun =sentence.sentence[c_id+1].form
                    ngramtype = "DET ADJ ADV NOUN"
                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun):
                        to_print = True
                    # else:
                    #     print(adv, noun)
                        # input()


            if to_print and adv in accepted_avs:


                # if not f"{adv}" in adv_files:
                #     adv_files[f"{adv}"] = open(f"{output_folder}/{adv_str}.txt", "w")


                ctx_left = " ".join([token.form for token in sentence_portion_left])
                candidate_str = " ".join([token.form for token in occurrence])
                ctx_right = " ".join([token.form for token in sentence_portion_right])
                # if check_print:
                #     print(sentence.sentence[c_id-1].form, adv, sentence.sentence[c_id+1].form)

                #     print(f"{adv} {noun}\t{ngramtype}\t{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}")
                #     input()

                print(f"{adv} {noun}\t{ngramtype}\t{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=adv_files[f"{adv}"])


def extract_detADVN_ctx_FINAL(filename, source, adv_files):

    ctx = 20

    for sentence in tqdm.tqdm(utils.read(filename, source)):

        candidates = set()
        for tok_id, token in enumerate(sentence.sentence):

            if token.pos == "ADV" and token.form in adv_files and \
                tok_id > 2 and \
                    tok_id < len(sentence.sentence)-2:
                candidates.add(tok_id)

        for c_id in candidates:
            adverb_object = sentence.sentence[c_id]
            pprevious_object = sentence.sentence[c_id-2]
            previous_object = sentence.sentence[c_id-1]
            next_object = sentence.sentence[c_id+1]
            nnext_object = sentence.sentence[c_id+2]


            adv = sentence.sentence[c_id].form
            adv_str = adv
            to_print = False



            if previous_object.pos == "DET":

                determiner = previous_object

                sentence_portion_left = sentence.sentence[max(0, c_id-1-ctx):c_id-1]


                if (
                    next_object.pos == "NOUN" and
                    (determiner.deprel == "" or determiner.head == adverb_object.id) or
                    (adverb_object.deprel == "" or adverb_object.head == next_object.id)
                ):
                    sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+2+ctx+1)]
                    occurrence = sentence.sentence[c_id-1:c_id+2]
                    noun = next_object.form
                    ngramtype = "DET ADV NOUN"

                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun ):
                        to_print = True


                if (
                    next_object.pos == "ADV" and
                    nnext_object.pos == "NOUN" and
                    (determiner.deprel == "" or determiner.head == nnext_object.id) or
                    (adverb_object.deprel == "" or adverb_object.head == nnext_object.id) or
                    (next_object.deprel == "" or next_object.head == nnext_object.id)
                ):
                    sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
                    occurrence = sentence.sentence[c_id-1:c_id+3]
                    noun = nnext_object.form
                    adv = adv + " " + next_object.form
                    adv_str = adv_str + "_" + next_object.form
                    ngramtype = "DET ADV NOUN"
                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun) and all(c.isalpha() or c in [" ", "-", "."] for c in adv):
                        to_print = True


            if pprevious_object.pos == "DET":
                # print(adv, "---", sentence)
                # input()

                determiner = pprevious_object
                sentence_portion_left = sentence.sentence[max(0, c_id-2-ctx):c_id-2]

                if (
                    previous_object.pos == "ADJ" and
                    next_object.pos == "NOUN" and
                    (determiner.deprel == "" or determiner.head == next_object.id) or
                    (adverb_object.deprel == "" or adverb_object.head == next_object.id)
                ):
                    sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+1+ctx+1)]
                    occurrence = sentence.sentence[c_id-2:c_id+2]
                    noun = next_object.form
                    ngramtype = "DET ADJ ADV NOUN"

                    if all(c.isalpha() or c in [" ", "-", "."] for c in noun):
                        to_print = True


            if to_print and adv in adv_files:

                ctx_left = " ".join([token.form for token in sentence_portion_left])
                candidate_str = " ".join([token.form for token in occurrence])
                ctx_right = " ".join([token.form for token in sentence_portion_right])

                print(f"{adv} {noun}\t{ngramtype}\t{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=adv_files[f"{adv}"])
                # print(f"{adv} {noun}\t{ngramtype}\t{source}\t{ctx_left}\t{candidate_str}\t{ctx_right}")
                # input("STAMPO")



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

    # adj_set = set()
    # with open("../ntrattino.csv") as fin:
    #     reader = csv.reader(fin)
    #     for line in reader:
    #         line = line[0].strip().split("\t")

    #         adj_set.add(line[3])


    # adj_files = {}
    # for adj in adj_set:
    #     adj_files[adj] = open(f"../output_ctxs_advN/{adj}.txt", "w")

    # adv_files = {}
    # accepted_avs = set()
    # with open("../data/ngrams_avverbi.txt") as fin:
    #     for line in fin:
    #         line = line.strip()
    #         accepted_avs.add(line)
    #         adv_files[line] = open(f"../output_ctxs_ngrams/{line}.txt", "w")


    prefixes = ["ex", "neo", "non", "pre", "post", "quasi"]
    adverbs = ["allora", "ancora", "non più", "già", "ormai", "quasi", "non",
               "appena", "forse", "non ancora"]

    # adverbs = ["allora"]

    # pref_files = {x: open(f"../output_final/trattino_ctx/{x}.txt", "w") for x in prefixes}
    adve_files = {x: open(f"../output_final/ngram_ctx/{x}.txt", "w") for x in adverbs}

    for name in files:
        print("Processing", name, "...")
        for file_id, filename in tqdm.tqdm(files[name]):
            # extract_advN(filename, name, file_id)
            # extract_detADVN(filename, name, file_id)
            print("EXTRACTING ADV-N")
            # extract_advN_ctx_FINAL(filename, name, pref_files)

            print("EXTRACTING CONTEXTS")
            extract_detADVN_ctx_FINAL(filename, name, adve_files)





