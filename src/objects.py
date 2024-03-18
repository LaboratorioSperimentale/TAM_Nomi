class Token:
    def __init__(self, id:int, form:str, lemma:str, pos:str,
                 head: int, deprel:str) -> None:
        self.id = id
        self.form = form
        self.lemma = lemma
        self.pos = pos
        self.head = head
        self.deprel = deprel


    def __repr__(self) -> str:
        return f"{self.form}/{self.pos}/{self.deprel}:{self.head}"


class Sentence:
    def __init__(self, source:str) -> None:
        self.sentence = []
        self.source = source
        self.sentence_map = {}

    def add_token(self, token:Token) -> None:
        self.sentence.append(token)
        self.sentence_map[token.id] = token

    def empty(self):
        if len(self.sentence) > 0:
            return False
        return True

    def get_token(self, id:int) -> Token:
        return self.sentence_map[id]


    def __repr__(self) -> str:
        return " ".join(x.form for x in self.sentence)