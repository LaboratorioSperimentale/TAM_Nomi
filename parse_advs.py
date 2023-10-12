fout_tam = open("data/TAM.advs", "w")
fout_other = open("data/other.advs", "w")

for filename in ["data/adv_annotati.post", "data/adv_annotati.pre"]:

    with open(filename) as fin:
        
        for line in fin:
            line = line.strip().split("\t")
            
            if len(line) == 2:
                
                if line[1] == "-":
                    print(f"{line[0]}\t{line[1]}", file=fout_other)
                else:
                    print(f"{line[0]}\t{line[1]}", file=fout_tam)


            elif len(line) == 3:
                print(f"{line[0]}\t{line[1]}/{line[2]}", file=fout_tam)

            else:
                print("ERRORE", line)
        