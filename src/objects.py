class Token:
    def __init__(self, form:str, lemma:str, pos:str) -> None:
        self.form = form
        self.lemma = lemma
        self.pos = pos


class Sentence:
    def __init__(self, source:str) -> None:
        self.sentence = []
        self.source = source

    def add_token(self, token:Token) -> None:
        self.sentence.append(token)

    def empty(self):
        if len(self.sentence) > 0:
            return False
        return True

    def __repr__(self) -> str:
        return " ".join(x.form for x in self.sentence)