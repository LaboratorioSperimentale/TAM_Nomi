import objects as objs
import pos_maps as pmaps


def read_wikiconll(fname):
    sentence = objs.Sentence(source="wikiCoNLL")

    with open(fname, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            # print(line)
            if line.startswith("<doc"):
                if not sentence.empty():
                    yield sentence

                sentence = objs.Sentence(source="wikiCoNLL")

            elif len(line) == 0:
                if not sentence.empty():
                    yield sentence

                sentence = objs.Sentence(source="wikiCoNLL")

            elif line.startswith("</doc"):
                pass

            else:
                line = line.strip().split("\t")

                form = line[1]
                lemma = line[2]
                pos = line[3]

                if pos in pmaps.wikiCoNLL_map:
                    pos = pmaps.wikiCoNLL_map[pos]
                else:
                    pass
                    #TODO add log

                token = objs.Token(form, lemma, pos)
                sentence.add_token(token)
        if not sentence.empty():
            yield sentence



def read_xlime(fname):
    sentence = objs.Sentence(source="xlime")

    with open(fname, encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if line == "":
                if not sentence.empty():
                    yield sentence
                sentence = objs.Sentence(source="xlime")
            else:
                line = line.split()
                form = line[0]
                lemma = line[0]
                pos = line[1]

                if pos in pmaps.xlime_map:
                    pos = pmaps.xlime_map[pos]
                else:
                    pass
                    #TODO add log
                # print(line)
                token = objs.Token(form, lemma, pos)
                sentence.add_token(token)

        if not sentence.empty():
            yield sentence



def read_UDT(fname, subcorpus):
    sentence = objs.Sentence(source=subcorpus)

    with open(fname, encoding="utf-8") as fin:
        for line in fin:
            if line.startswith("#"):
                if not sentence.empty():
                    yield sentence

                sentence = objs.Sentence(source=subcorpus)
            elif line.strip() == "":
                pass
            else:
                line = line.strip().split("\t")

                token = objs.Token(line[1], line[2], line[4])
                sentence.add_token(token)


        if not sentence.empty():
            yield sentence


def read_repubblica(fname):
    sentence = objs.Sentence(source="repubblica")

    with open(fname, encoding="utf-8") as fin:
        for line in fin:
            if line.startswith("<s"):
                if not sentence.empty():
                    yield sentence

                sentence = objs.Sentence(source="repubblica")

            elif line.startswith("<"):
                pass

            else:
                line = line.strip().split("\t")

                form = line[1]
                lemma = line[2]
                pos = line[4]

                if pos in pmaps.repubblica_map:
                    pos = pmaps.repubblica_map[pos]
                elif pos[0] in pmaps.repubblica_map:
                    pos = pmaps.repubblica_map[pos[0]]
                else:
                    pass
                    #TODO add log

                token = objs.Token(form, lemma, pos)
                sentence.add_token(token)
        if not sentence.empty():
            yield sentence



def read_parseme(fname):
    sentence = objs.Sentence(source="parseme")

    with open(fname, encoding="utf-8") as fin:
        for line in fin:
            if line.startswith("#"):
                if not sentence.empty():
                    yield sentence

                sentence = objs.Sentence(source="parseme")
            elif line.strip() == "":
                pass
            else:
                line = line.strip().split("\t")

                token = objs.Token(line[1], line[2], line[3])
                sentence.add_token(token)


        if not sentence.empty():
            yield sentence


def read_itwac(fname):

    sentence = objs.Sentence(source="itwac")

    with open(fname, encoding="iso-8859-1") as fin:

        for line in fin:
            if line.startswith("<s"):
                if not sentence.empty():
                    yield sentence

                sentence = objs.Sentence(source="itwac")

            elif line.startswith("<"):
                pass

            else:
                line = line.strip().split("\t")
                if len(line) == 3:

                    form = line[0]
                    lemma = line[2]
                    pos = line[1].split(":")[0]
                    if pos in pmaps.itwac_map:
                        pos = pmaps.itwac_map[pos]
                    else:
                        pass
                        #TODO add log

                    token = objs.Token(form, lemma, pos)
                    sentence.add_token(token)
                else:
                    pass
                    #TODO add log

        if not sentence.empty():
            yield sentence


def read(filename, source):

    if source == "ITWAC":
        return read_itwac(filename)
    elif source == "PARSEME":
        return read_parseme(filename)
    elif source == "REPUBBLICA":
        return read_repubblica(filename)
    elif source == "XLIME":
        return read_xlime(filename)
    elif source == "WIKICONLL":
        return read_wikiconll(filename)
    else:
        return read_UDT(filename, source)


if __name__ == "__main__":
    # for sentence in read_itwac("/home/ludovica/Documents/CORPORA/ITWAC/ITWAC-1.xml"):
    #     print(sentence)
    #     input()

    # for sentence in read_parseme("/home/ludovica/Documents/CORPORA/PARSEME-IT/train.cupt"):
    #     print(sentence)
    #     input()

    # for sentence in read_repubblica("/home/ludovica/Documents/CORPORA/REPUBBLICA/repubblica.parsed.utf8.xml"):
    #     print(sentence)
    #     # input()

    # for sentence in read_UDT("/home/ludovica/Documents/CORPORA/UD_Italian-ISDT/it_isdt-ud-train.conllu", "ISDT"):
    #     print(sentence)
    #     input()

    # for sentence in read_xlime("/home/ludovica/Documents/CORPORA/xlime_twitter_corpus-master/corpus_task/italian_pos.txt"):
    #     print(sentence)
    #     # input()

    for sentence in read_wikiconll("/home/ludovica/Documents/CORPORA/WIKICONLL/wikiCoNLL"):
        print(sentence)
        # input()