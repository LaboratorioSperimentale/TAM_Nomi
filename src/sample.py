import random
import glob
import os

import pos_maps as pmaps

def sample(contexts_folder:str, word_list: str, n_ctxs:int, seed:int):
    random.seed(seed)

    with open(word_list, encoding="utf-8") as fin:
        files_to_open = []
        for line in fin:
            line = line.strip()
            files_to_open.append(line+".txt")


    with open(f"{contexts_folder}/CTXS_NON.tsv", "w", encoding="utf-8") as fout:

        for filename in files_to_open:
            print(filename[:-4], file=fout)
            with open(f"{contexts_folder}/{filename}", encoding="utf-8") as fin:
                contexts = fin.readlines()

                sample_list = contexts
                if len(contexts) > n_ctxs:
                    sample_list = random.sample(contexts, n_ctxs)

                for ctx in sample_list:
                    print(ctx.strip(), file=fout)

            print("", file=fout)


def sample_2(contexts_folder:str, prefix_folder:str, output_folder: str, n_ctxs:int, seed:int):

    random.seed(seed)

    to_search_for = {}

    for filename in glob.glob(prefix_folder+"/*"):

        prefix = filename.split("/")[-1][:-4]
        to_search_for[prefix] = {}
        # print(prefix)
        # input()

        # fout = open(f"{output_folder}/{prefix}.txt", "w")

        with open(filename) as fin:
            header = fin.readline().strip().split("\t")
            print(header)
            for line in fin:
                line = line.strip().split("\t")
                line = line +  [""]*(len(header) - len(line))
                if len(line) == 1:
                    print(f"EMPTY: {line}")
                else:
                    d = dict(zip(header, line))
                    # print(d)
                    if not d["ERR"] == "x":
                        if not d["semantica nome"] == "-":
                            to_search_for[prefix][d["ADV-N"]] = d
                        else:
                            to_search_for[prefix][d["ADV-N"]] = d
                            # print(f"DIVERSA SEMANTICA: {d['ADV-N']}")
                    else:
                        print(f"ERROR: {d['ADV-N']}")

    # print([(x, len(to_search_for[x])) for x in to_search_for])
    # input()

    for prefix in to_search_for:
        with open(f"{output_folder}/{prefix}.txt", "w") as fout:
            print("ITWAC\tREPUBBLICA\tWIKICONLL\tADV-N\tsemantica nome\tserve contesto\tvalore prefisso\tcontesto", file=fout)

            for element_name, element_content in to_search_for[prefix].items():

                print(f"{element_content['ITWAC']}\t{element_content['REPUBBLICA']}\t{element_content['WIKICONLL']}\t{element_name}\t{element_content['semantica nome']}\t{element_content['serve contesto']}\t{element_content['valore prefisso']}", file=fout)

                # ADV-N	ERR	semantica nome	serve contesto	animato	valore prefisso

                path = f"{contexts_folder}/{element_name}.txt"

                if not os.path.exists(path):
                    print(f"FILE ISSUE: {element_content['ADV-N']}")

                else:
                    repubblica = []
                    n_repubblica = 0
                    wikiconll = []
                    n_wikiconll = 0
                    itwac = []
                    n_itwac = 0
                    TOT = 0

                    with open(path) as fin:
                        for line in fin:
                            linesplit = line.strip().split("\t")
                            if linesplit[0] == "ITWAC":
                                if not line in itwac:
                                    itwac.append(line)
                                    n_itwac += 1
                            elif linesplit[0] == "REPUBBLICA":
                                if not line in repubblica:
                                    repubblica.append(line)
                                    n_repubblica += 1
                            else:
                                if not line in wikiconll:
                                    wikiconll.append(line)
                                    n_wikiconll += 1
                            TOT += 1

                    if TOT > n_repubblica+n_wikiconll+n_itwac:
                        print(f"file {path} contains {TOT- (n_repubblica+n_wikiconll+n_itwac)} repetitions")

                    perc_repubblica = int(n_repubblica*n_ctxs/TOT)
                    perc_itwac = int(n_itwac*n_ctxs/TOT)
                    perc_wikiconll = int(n_wikiconll*n_ctxs/TOT)
                    # print(perc_itwac, perc_repubblica, perc_wikiconll)
                    # input()

                    if n_repubblica > perc_repubblica:
                        sample_repubblica = random.sample(repubblica, perc_repubblica)
                    else:
                        sample_repubblica = repubblica

                    if n_itwac > perc_itwac:
                        sample_itwac = random.sample(itwac, perc_itwac)
                    else:
                        sample_itwac = itwac

                    if n_wikiconll > perc_wikiconll:
                        sample_wikiconll = random.sample(wikiconll, perc_wikiconll)
                    else:
                        sample_wikiconll = wikiconll

                    prefisso_tab = "\t"*7
                    for ctx in sample_itwac:
                        print(prefisso_tab+ctx.strip(), file=fout)
                    for ctx in sample_repubblica:
                        print(prefisso_tab+ctx.strip(), file=fout)
                    for ctx in sample_wikiconll:
                        print(prefisso_tab+ctx.strip(), file=fout)

                    print("", file=fout)


def sample_2_ngrams(contexts_folder:str, output_folder: str, n_ctxs:int, seed:int):

    random.seed(seed)

    for filename in glob.glob(contexts_folder+"/*"):
        # print(filename)
        adv_name = filename.split("/")[-1].split(".")[-2]
        fout = open(f"{output_folder}/{adv_name}.txt", "w")

        print("ITWAC\tREPUBBLICA\tWIKICONLL\tNGRAM\tsemantica nome\tvalore adv\tngram pattern\tsource\tcontesto", file=fout)

        with open(filename) as fin:
            prev_word = ""
            repubblica = []
            n_repubblica = 0
            wikiconll = []
            n_wikiconll = 0
            itwac = []
            n_itwac = 0
            TOT = 0

            for line in fin:
                linesplit = line.strip().split("\t")
                cur_word = linesplit[0]
                cur_source = linesplit[2]

                if not cur_word == prev_word:

                    if len(prev_word)>1:
                        dump(prev_word,
                            repubblica, n_repubblica,
                            wikiconll, n_wikiconll,
                            itwac, n_itwac,
                            TOT, n_ctxs, fout)
                    prev_word = cur_word
                    repubblica = []
                    n_repubblica = 0
                    wikiconll = []
                    n_wikiconll = 0
                    itwac = []
                    n_itwac = 0
                    TOT = 0


                if cur_source == "ITWAC":
                    if not line in itwac:
                        itwac.append(line)
                        n_itwac += 1
                elif cur_source == "REPUBBLICA":
                    if not line in repubblica:
                        repubblica.append(line)
                        n_repubblica += 1
                else:
                    if not line in wikiconll:
                        wikiconll.append(line)
                        n_wikiconll += 1
                TOT += 1

            if len(prev_word)>1:
                dump(prev_word,
                    repubblica, n_repubblica,
                    wikiconll, n_wikiconll,
                    itwac, n_itwac,
                    TOT, n_ctxs, fout)



def dump(prev_word,
        repubblica, n_repubblica,
        wikiconll, n_wikiconll,
        itwac, n_itwac,
        TOT, n_ctxs, fout):

    # print(n_repubblica, n_wikiconll, n_itwac)
    # input()

    print(f"{n_itwac}\t{n_repubblica}\t{n_wikiconll}\t{prev_word}", file=fout)


    if TOT > n_repubblica+n_wikiconll+n_itwac:
        print(f"{prev_word} contains {TOT- (n_repubblica+n_wikiconll+n_itwac)} repetitions")

    perc_repubblica = int(n_repubblica*n_ctxs/TOT)
    perc_itwac = int(n_itwac*n_ctxs/TOT)
    perc_wikiconll = int(n_wikiconll*n_ctxs/TOT)


    if n_repubblica > perc_repubblica:
        sample_repubblica = random.sample(repubblica, perc_repubblica)
    else:
        sample_repubblica = repubblica

    if n_itwac > perc_itwac:
        sample_itwac = random.sample(itwac, perc_itwac)
    else:
        sample_itwac = itwac

    if n_wikiconll > perc_wikiconll:
        sample_wikiconll = random.sample(wikiconll, perc_wikiconll)
    else:
        sample_wikiconll = wikiconll


    prefisso_tab = "\t"*6
    for ctx in sample_itwac:
        ctx = ctx.strip().split("\t")
        context = '\t'.join(ctx[3:])
        print(f"{prefisso_tab}{ctx[1]}\t{ctx[2]}\t{context}", file=fout)
    for ctx in sample_repubblica:
        ctx = ctx.strip().split("\t")
        context = '\t'.join(ctx[3:])
        print(f"{prefisso_tab}{ctx[1]}\t{ctx[2]}\t{context}", file=fout)
    for ctx in sample_wikiconll:
        ctx = ctx.strip().split("\t")
        context = '\t'.join(ctx[3:])
        print(f"{prefisso_tab}{ctx[1]}\t{ctx[2]}\t{context}", file=fout)

    print("", file=fout)


def split_files(input_folder, output_folder):



    semantics_map = {}
    with open("../pulizia/nomi.sorted") as fin:
        for line in fin:
            linesplit = line.strip().split("\t")
            noun, sem = linesplit
            if not noun in semantics_map:
                semantics_map[noun] = []


            if sem in pmaps.categories_map.values():
                semantics_map[noun].append(sem)
            else:
                semantics_map[noun].append(pmaps.categories_map[sem])

    output_files = {}

    files = glob.glob(input_folder+"/*.txt")

    for file in files:
        counts = {}
        with open(file) as fin:
            for line in fin:
                linesplit = line.strip().split("\t")
                collocation = linesplit[0]
                # print(file, line)
                corpus = linesplit[2]

                if not collocation in output_files:
                    output_files[collocation] = open(f"{output_folder}/{collocation}.txt", "w")

                print(line.strip(), file=output_files[collocation])

                if not collocation in counts:
                    counts[collocation] = {"ITWAC":0, "REPUBBLICA":0, "WIKICONLL":0}

                # print(file, line)
                counts[collocation][corpus] += 1

        # with open(f"{input_folder}/COUNTS", "w") as fout:
        #     print(f"COLLOCATION\tSEM\tITWAC\tREPUBBLICA\tWIKICONLL\tTOT", file=fout)
        #     for collocation in counts:
        #         n_semantics = "?"
        #         if collocation in semantics_map:
        #             n_semantics = "#".join(semantics_map[collocation])
        #         itwac_n = counts[collocation]['ITWAC']
        #         repubblica_n = counts[collocation]['REPUBBLICA']
        #         wikiconll_n = counts[collocation]['WIKICONLL']
        #         TOT = itwac_n+repubblica_n+wikiconll_n
        #         print(f"{collocation}\t{n_semantics}\t{itwac_n}\t{repubblica_n}\t{wikiconll_n}\t{TOT}", file=fout)





if __name__ == "__main__":
    # sample("../output_ctxs", "../data/selected_non_sample.txt", 50, 1673)

    # sample_2("../output_ctxs", "../data/prefissi", "../data_samples/", 30, 1673)

    # sample_2_ngrams("../output_ctxs_ngrams/sorted/", "../data_samples_ngrams/", 30, 865)

    split_files("../output_final/ngram_ctx/", "../output_final/ngram_ctx/split/")
    # split_files("../output_final/trattino_ctx/", "../output_final/trattino_ctx/split/")