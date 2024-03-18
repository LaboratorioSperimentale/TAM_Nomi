with open("POST", "w") as fout:

    with open("post-noun.txt") as fin:
        for line in fin:
            print(line)
            name, fname = line.strip().split("\t")


            contexts = open(fname).readlines()
            for ctx in contexts:
                ctx = ctx.strip()
                print(f"{name}\t{ctx}", file=fout)
            print("", file=fout)