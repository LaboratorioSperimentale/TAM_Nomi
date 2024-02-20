import random

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

if __name__ == "__main__":
    sample("../output_ctxs", "../data/selected_non_sample.txt", 50, 1673)