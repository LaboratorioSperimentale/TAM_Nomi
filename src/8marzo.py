import glob
import pos_maps as pmaps
import os
import csv
import collections

counts = {}
noun_semantics = {}

with open("../pulizia/nomi.sorted") as fin:
    for line in fin:
        print(line)
        word, sem = line.strip().split("\t")
        if not word in noun_semantics:
            noun_semantics[word] = set()

        print(pmaps.categories_map.values())

        if sem in pmaps.categories_map.values():
            noun_semantics[word].add(sem)
        else:
            noun_semantics[word].add(pmaps.categories_map[sem])

# input_counts_ngrams = "../output_final/ngram_ctx/COUNTS"
# with open(input_counts_ngrams) as fin:
#     fin.readline()

#     for line in fin:
#         line = line.strip().split("\t")

#         coll, sem, n_itwac, n_repubblica, n_wiki, _ = line

#         if not coll in counts:
#             counts[coll] = {"sketch":0,
#                             "prefix": {"ITWAC":0, "REPUBBLICA":0, "WIKICONLL":0},
#                             "adverb": {"ITWAC":0, "REPUBBLICA":0, "WIKICONLL":0}}

#         counts[coll]["adverb"]["ITWAC"] = n_itwac
#         counts[coll]["adverb"]["REPUBBLICA"] = n_repubblica
#         counts[coll]["adverb"]["WIKICONLL"] = n_wiki

#         if not coll in noun_semantics:
#             noun_semantics[coll] = []

#         noun_semantics[coll] += sem.split("#")


# input_counts_ntratt = "../output_final/trattino_ctx/COUNTS"
# with open(input_counts_ntratt) as fin:
#     fin.readline()

#     for line in fin:
#         line = line.strip().split("\t")

#         coll, sem, n_itwac, n_repubblica, n_wiki, _ = line

#         if not coll in counts:
#             counts[coll] = {"sketch":0,
#                             "prefix": {"ITWAC":0, "REPUBBLICA":0, "WIKICONLL":0},
#                             "adverb": {"ITWAC":0, "REPUBBLICA":0, "WIKICONLL":0}}

#         counts[coll]["prefix"]["ITWAC"] = n_itwac
#         counts[coll]["prefix"]["REPUBBLICA"] = n_repubblica
#         counts[coll]["prefix"]["WIKICONLL"] = n_wiki

#         if not coll in noun_semantics:
#             noun_semantics[coll] = []

#         noun_semantics[coll] += sem.split("#")

# for noun in noun_semantics:
#     noun_semantics[noun] = set(noun_semantics[noun])


############################
#    PROCESSING PREFISSI   #
############################


prefissi = ["ex", "neo", "quasi", "pre", "post", "non"]

for prefisso in prefissi:

    print(f"PROCESSING {prefisso}")

    collected_information = {}

    all_corpora = {x.strip():False for x in open(f"../output_final/trattino_ctx/{prefisso}.uniq").readlines()}
    all_sketch = {}
    freqs_sketch = {}

    with open(f"../annotati/prefissi/{prefisso}-N.csv", encoding="utf-8") as csvfin:
        reader = csv.reader(csvfin)
        for row in reader:
            word = row[0].strip()
            if word.startswith(f"{prefisso}-"):
                word = word[len(f"{prefisso}-"):]
                freq = int(row[1])

                all_sketch[word] = False
                freqs_sketch[word] = freq
                # print(freqs_sketch)
                # input()


    with open(f"../annotati/prefissi/{prefisso}_sketch.tsv") as fin:
        for line in fin:
            linesplit = line.strip().split("\t")
            # print(linesplit)

            word, *_ = linesplit
            projected_semantics = "?"

            if word in noun_semantics:
                projected_semantics = "#".join(noun_semantics[word])

            all_sketch[word] = True


            collected_information[word] = {"freq_sketch":freqs_sketch[word],
                                        "projected_semantics": projected_semantics,
                                        "annotated_semantics": "?",
                                        "selected": True,
                                        "f-pref_itwac":0,
                                        "f-adv_itwac":"-",
                                        "f-pref_repubblica":0,
                                        "f-adv_repubblica":"-",
                                        "f-pref_wikiconll":0,
                                        "f-adv_wikiconll":"-",
                                        "word":word
                                        }


    with open(f"../annotati/prefissi/{prefisso}_corpora.tsv") as fin:
        fin.readline()
        for line in fin:
            line = line.split("\t")
            if not line[0].strip() == "":
                # print(line)
                word, semantics, *_ = line
                word = word.split("-", 1)[1]
                semantics = semantics.strip()
                if len(semantics) == 0:
                    semantics = "-"

                if word in all_corpora:
                    all_corpora[word] = True


                n_itwac = 0
                n_repubblica = 0
                n_wiki = 0

                annotated_semantics = pmaps.categories_map[semantics]
                projected_semantics = annotated_semantics

                if word in noun_semantics:
                    projected_semantics = "#".join(noun_semantics[word])


                # print(word, annotated_semantics, projected_semantics)

                file_occurrences = f"../output_final/trattino_ctx/split/{word}.txt"
                file_examples = f"../8marzo/{prefisso}_pref/extraction_corpora/{word}.tsv"
                os.makedirs(os.path.dirname(file_examples), exist_ok=True)

                if os.path.exists(file_occurrences):

                    with open(file_occurrences) as focc, open(file_examples, "w") as fout_occ:
                        examples = {"ITWAC":[], "REPUBBLICA":[], "WIKICONLL":[]}
                        for lineocc in focc:
                            lineocc = lineocc.strip().split("\t")
                            # print(lineocc)
                            postctx = ""
                            if len(lineocc) == 5:
                                _, _, source, prectx, compound = lineocc
                            elif len(lineocc) == 6:
                                _, _, source, prectx, compound, postctx = lineocc
                            if compound.startswith(f"{prefisso}-"):
                                example = f"{prectx}\t{compound}\t{postctx}"
                                if not example in examples[source]:
                                    examples[source].append(example)

                        n_itwac = len(examples["ITWAC"])
                        n_wiki = len(examples["WIKICONLL"])
                        n_repubblica = len(examples["REPUBBLICA"])

                        if word in collected_information:
                            collected_information[word]["annotated_semantics"] = annotated_semantics
                            collected_information[word]["f-pref_itwac"] = n_itwac
                            collected_information[word]["f-pref_repubblica"] = n_repubblica
                            collected_information[word]["f-pref_wikiconll"] = n_wiki
                        else:
                            collected_information[word] = {"freq_sketch":0,
                                                            "projected_semantics": projected_semantics,
                                                            "annotated_semantics": annotated_semantics,
                                                            "selected": True,
                                                            "f-pref_itwac":n_itwac,
                                                            "f-adv_itwac":"-",
                                                            "f-pref_repubblica":n_repubblica,
                                                            "f-adv_repubblica":"-",
                                                            "f-pref_wikiconll":n_wiki,
                                                            "f-adv_wikiconll":"-",
                                                            "word":word
                                                            }

                        for source in examples:
                            for example in examples[source]:
                                print(f"{source}\t{example}", file=fout_occ)
                            print("", file=fout_occ)

    for word in all_corpora:
        if not all_corpora[word]:

            if not word in collected_information:
                collected_information[word] = {"freq_sketch":0,
                                                "projected_semantics": "?",
                                                "annotated_semantics": "?",
                                                "selected": False,
                                                "f-pref_itwac":0,
                                                "f-adv_itwac":"-",
                                                "f-pref_repubblica":0,
                                                "f-adv_repubblica":"-",
                                                "f-pref_wikiconll":0,
                                                "f-adv_wikiconll":"-",
                                                "word":word
                                                }

                if word in noun_semantics:
                    collected_information[word]["projected_semantics"] = "#".join(noun_semantics[word])


            file_occurrences = f"../output_final/trattino_ctx/split/{word}.txt"
            file_examples = f"../8marzo/{prefisso}_pref/extraction_corpora/{word}.tsv"

            os.makedirs(os.path.dirname(file_examples), exist_ok=True)

            if os.path.exists(file_occurrences):
                with open(file_occurrences) as focc:#, open(file_examples, "w") as fout_occ:
                    examples = {"ITWAC":[], "REPUBBLICA":[], "WIKICONLL":[]}
                    for lineocc in focc:
                        lineocc = lineocc.strip().split("\t")
                        # print(lineocc)
                        postctx = ""
                        if len(lineocc) == 5:
                            _, _, source, prectx, compound = lineocc
                        elif len(lineocc) == 6:
                            _, _, source, prectx, compound, postctx = lineocc
                        if compound.startswith(f"{prefisso}-"):
                            example = f"{prectx}\t{compound}\t{postctx}"
                            if not example in examples[source]:
                                examples[source].append(example)

                    n_itwac = len(examples["ITWAC"])
                    n_wiki = len(examples["WIKICONLL"])
                    n_repubblica = len(examples["REPUBBLICA"])

                    collected_information[word]["f-pref_itwac"] = n_itwac
                    collected_information[word]["f-pref_repubblica"] = n_repubblica
                    collected_information[word]["f-pref_wikiconll"] = n_wiki

                if n_itwac+n_wiki+n_repubblica > 4:
                    with open(file_examples, "w") as fout_occ:
                        for source in examples:
                            for example in examples[source]:
                                print(f"{source}\t{example}", file=fout_occ)
                            print("", file=fout_occ)

    for word in all_sketch:
        if not all_sketch[word]:
            if not word in collected_information:
                collected_information[word] = {"freq_sketch":0,
                                                "projected_semantics": "?",
                                                "annotated_semantics": "?",
                                                "selected": False,
                                                "f-pref_itwac":0,
                                                "f-adv_itwac":"-",
                                                "f-pref_repubblica":0,
                                                "f-adv_repubblica":"-",
                                                "f-pref_wikiconll":0,
                                                "f-adv_wikiconll":"-",
                                                "word":word
                                                }
                if word in noun_semantics:
                    collected_information[word]["projected_semantics"] = "#".join(noun_semantics[word])

            collected_information[word]["freq_sketch"] = freqs_sketch[word]


    with open(f"../8marzo/{prefisso}.pref.collected_information.csv", "w") as fout:
        fieldnames = ["word", "selected", "annotated_semantics", "projected_semantics",
                    "freq_sketch", "f-pref_itwac", "f-pref_repubblica", "f-pref_wikiconll",
                    "f-adv_itwac", "f-adv_repubblica", "f-adv_wikiconll"]

        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for word in collected_information:
            writer.writerow(collected_information[word])





############################
#    PROCESSING ADVERBS   #
############################

adverbs = ["allora", "ancora", "già", "nonpiù", "ormai", "quasi", "non", "appena", "forse"]
# adverbs = ["appena"]

for adverb in adverbs:

    print(f"PROCESSING {adverb}")

    collected_information = {}

    all_corpora = {x.strip():False for x in open(f"../output_final/ngram_ctx/{adverb}.uniq").readlines()}
    # print(all_corpora)
    all_sketch = {}
    freqs_sketch = collections.defaultdict(int)

    path_to_open = f"../annotati/ngrams/{adverb}-N.csv"
    if adverb == "nonpiù":
        path_to_open = f"../annotati/prefissi/non-N.csv"

    with open(path_to_open, encoding="utf-8") as csvfin:
        reader = csv.reader(csvfin)
        for row in reader:
            word = row[0].strip()

            adv_prefix = adverb
            if adverb == "nonancora":
                adv_prefix = "non-ancora"
            if adverb == "nonpiù":
                adv_prefix = "non-più"

            if word.startswith(f"{adv_prefix}-"):
                word = word[len(f"{adv_prefix}-"):]
                freq = int(row[1])

                all_sketch[word] = False
                freqs_sketch[word] = freq
                # print(freqs_sketch)
                # input()


    with open(f"../annotati/ngrams/{adverb}_sketch.tsv") as fin:
        for line in fin:
            linesplit = line.strip().split("\t")
            # print(linesplit)

            word, *_ = linesplit
            projected_semantics = "?"

            if word in noun_semantics:
                projected_semantics = "#".join(noun_semantics[word])

            all_sketch[word] = True


            collected_information[word] = {"freq_sketch":freqs_sketch[word],
                                        "projected_semantics": projected_semantics,
                                        "annotated_semantics": "?",
                                        "selected": True,
                                        "f-pref_itwac":"-",
                                        "f-adv_itwac":0,
                                        "f-pref_repubblica":"-",
                                        "f-adv_repubblica":0,
                                        "f-pref_wikiconll":"-",
                                        "f-adv_wikiconll":0,
                                        "word":word
                                        }

    if os.path.exists(f"../annotati/ngrams/{adverb}_corpora.tsv"):

        # print("FILE ESISTE")
        # input()
        with open(f"../annotati/ngrams/{adverb}_corpora.tsv") as fin:
            fin.readline()
            for line in fin:
                line = line.split("\t")
                if not line[0].strip() == "":

                    if len(line)>=2:
                        word, semantics, *_ = line
                    else:
                        word = line[0].strip()
                        semantics = "-"

                    if adverb in ["nonancora", "nonpiù"]:
                        word = word.split(" ", 2)[2]
                    else:
                        word = word.split(" ", 1)[1]

                    # print(line)
                    # print(word)
                    # input()
                    semantics = semantics.strip()
                    if len(semantics) == 0:
                        semantics = "-"

                    if word in all_corpora:
                        all_corpora[word] = True


                    n_itwac = 0
                    n_repubblica = 0
                    n_wiki = 0

                    if semantics in pmaps.categories_map:
                        annotated_semantics = pmaps.categories_map[semantics]
                    else:
                        annotated_semantics = "?"
                    projected_semantics = annotated_semantics

                    if word in noun_semantics:
                        projected_semantics = "#".join(noun_semantics[word])


                    # print(word, annotated_semantics, projected_semantics)

                    file_occurrences = f"../output_final/ngram_ctx/split/{word}.txt"
                    file_examples = f"../8marzo/{adverb}_adv/extraction_corpora/{word}.tsv"
                    os.makedirs(os.path.dirname(file_examples), exist_ok=True)

                    if os.path.exists(file_occurrences):

                        with open(file_occurrences) as focc:#, open(file_examples, "w") as fout_occ:
                            examples = {"ITWAC":[], "REPUBBLICA":[], "WIKICONLL":[]}
                            for lineocc in focc:
                                lineocc = lineocc.strip().split("\t")
                                # print(lineocc)
                                postctx = ""
                                if len(lineocc) == 5:
                                    _, _, source, prectx, compound = lineocc
                                elif len(lineocc) == 6:
                                    _, _, source, prectx, compound, postctx = lineocc


                                adv_prefix = adverb
                                if adverb == "nonancora":
                                    adv_prefix = "non ancora"
                                if adverb == "nonpiù":
                                    adv_prefix = "non più"

                                if f"{adv_prefix}" in compound:
                                    example = f"{prectx}\t{compound}\t{postctx}"
                                    if not example in examples[source]:
                                        examples[source].append(example)

                            n_itwac = len(examples["ITWAC"])
                            n_wiki = len(examples["WIKICONLL"])
                            n_repubblica = len(examples["REPUBBLICA"])

                            if word in collected_information:
                                collected_information[word]["annotated_semantics"] = annotated_semantics
                                collected_information[word]["f-adv_itwac"] = n_itwac
                                collected_information[word]["f-adv_repubblica"] = n_repubblica
                                collected_information[word]["f-adv_wikiconll"] = n_wiki
                            else:
                                collected_information[word] = {"freq_sketch":0,
                                                                "projected_semantics": projected_semantics,
                                                                "annotated_semantics": annotated_semantics,
                                                                "selected": True,
                                                                "f-pref_itwac":"-",
                                                                "f-adv_itwac":n_itwac,
                                                                "f-pref_repubblica":"-",
                                                                "f-adv_repubblica":n_repubblica,
                                                                "f-pref_wikiconll":"-",
                                                                "f-adv_wikiconll":n_wiki,
                                                                "word":word
                                                                }

                        # if n_itwac + n_repubblica + n_wiki > 4:
                        if n_repubblica + n_wiki > 4:
                            with open(file_examples, "w") as fout_occ:
                                for source in examples:
                                    for example in examples[source]:
                                        print(f"{source}\t{example}", file=fout_occ)
                                    print("", file=fout_occ)

    for word in all_corpora:

        if not all_corpora[word]:

            if not word in collected_information:

                collected_information[word] = {"freq_sketch":0,
                                                "projected_semantics": "?",
                                                "annotated_semantics": "?",
                                                "selected": False,
                                                "f-pref_itwac":"-",
                                                "f-adv_itwac":0,
                                                "f-pref_repubblica":"-",
                                                "f-adv_repubblica":0,
                                                "f-pref_wikiconll":"-",
                                                "f-adv_wikiconll":0,
                                                "word":word
                                                }



            if word in noun_semantics:
                collected_information[word]["projected_semantics"] = "#".join(noun_semantics[word])


            file_occurrences = f"../output_final/ngram_ctx/split/{word}.txt"
            file_examples = f"../8marzo/{adverb}_adv/extraction_corpora/{word}.tsv"

            os.makedirs(os.path.dirname(file_examples), exist_ok=True)


            if os.path.exists(file_occurrences):
                # print(file_occurrences)
                # input()
                with open(file_occurrences) as focc, open(file_examples, "w") as fout_occ:
                    examples = {"ITWAC":[], "REPUBBLICA":[], "WIKICONLL":[]}
                    for lineocc in focc:
                        lineocc = lineocc.strip().split("\t")
                        # print(lineocc)
                        postctx = ""
                        if len(lineocc) == 5:
                            _, _, source, prectx, compound = lineocc
                        elif len(lineocc) == 6:
                            _, _, source, prectx, compound, postctx = lineocc

                        adv_prefix = adverb
                        if adverb == "nonancora":
                            adv_prefix = "non ancora"
                        if adverb == "nonpiù":
                            adv_prefix = "non più"
                        if adv_prefix in compound:
                            example = f"{prectx}\t{compound}\t{postctx}"
                            if not example in examples[source]:
                                examples[source].append(example)

                    n_itwac = len(examples["ITWAC"])
                    n_wiki = len(examples["WIKICONLL"])
                    n_repubblica = len(examples["REPUBBLICA"])

                    collected_information[word]["f-adv_itwac"] = n_itwac
                    collected_information[word]["f-adv_repubblica"] = n_repubblica
                    collected_information[word]["f-adv_wikiconll"] = n_wiki

                    for source in examples:
                        for example in examples[source]:
                            print(f"{source}\t{example}", file=fout_occ)
                        print("", file=fout_occ)

    for word in all_sketch:
        if not all_sketch[word]:
            if not word in collected_information:
                collected_information[word] = {"freq_sketch":0,
                                                "projected_semantics": "?",
                                                "annotated_semantics": "?",
                                                "selected": False,
                                                "f-pref_itwac":"-",
                                                "f-adv_itwac":0,
                                                "f-pref_repubblica":"-",
                                                "f-adv_repubblica":0,
                                                "f-pref_wikiconll":"-",
                                                "f-adv_wikiconll":0,
                                                "word":word
                                                }
                if word in noun_semantics:
                    collected_information[word]["projected_semantics"] = "#".join(noun_semantics[word])

            collected_information[word]["freq_sketch"] = freqs_sketch[word]


    with open(f"../8marzo/{adverb}.adv.collected_information.csv", "w") as fout:
        fieldnames = ["word", "selected", "annotated_semantics", "projected_semantics",
                    "freq_sketch", "f-pref_itwac", "f-pref_repubblica", "f-pref_wikiconll",
                    "f-adv_itwac", "f-adv_repubblica", "f-adv_wikiconll"]

        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for word in collected_information:
            writer.writerow(collected_information[word])