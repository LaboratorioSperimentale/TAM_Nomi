import csv
import collections

all_info = {}

parameter = "non"

with open(f"../8marzo/{parameter}.all.collected_information.csv") as csvfile:

    reader = csv.reader(csvfile)

    header = reader.__next__()
    print(header)

    for row in reader:
        info = dict(zip(header, row))
        # print(info)
        # input()

        if info["word"] not in all_info:
            all_info[info["word"]] = collections.defaultdict(int)

        all_info[info["word"]]["word"] = info["word"]
        all_info[info["word"]]["selected"] = info["selected"]
        all_info[info["word"]]["annotated_semantics"] = info["annotated_semantics"]
        all_info[info["word"]]["projected_semantics"] = info["projected_semantics"]
        all_info[info["word"]]["freq_sketch"] = info["freq_sketch"]
        all_info[info["word"]]["freq_sketch"] = info["freq_sketch"]

        for f_pref in ['f-pref_itwac', 'f-pref_repubblica', 'f-pref_wikiconll']:
            if not info[f_pref] == "-":
                freq = int(info[f_pref])
                all_info[info["word"]][f_pref] = freq

        for f_adv in ['f-adv_itwac', 'f-adv_repubblica', 'f-adv_wikiconll']:
            if not info[f_adv] == "-":
                freq = int(info[f_adv])
                all_info[info["word"]][f_adv] = freq



with open(f"../8marzo/{parameter}.sorted.collected_infomation.csv", "w") as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=header)

    writer.writeheader()

    for element in all_info:
        writer.writerow(all_info[element])