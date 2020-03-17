from enum import Enum


class TypeQCM(Enum):
    QUESTION = 1
    QUESTION_MULT = 2


def type_from_str(string):
    if string == "question":
        return TypeQCM.QUESTION
    if string == "questionmult":
        return TypeQCM.QUESTION_MULT


class Reponse:

    def __init__(self, est_correcte, enonce):
        self.est_correcte = est_correcte
        self.enonce = enonce

    def __str__(self):
        if self.est_correcte:
            return "bonne : " + self.enonce
        else:
            return "mauvaise : " + self.enonce


class Question:

    def __init__(self, type_qcm, nom, enonce, reponses):
        self.type = type_qcm
        self.nom = nom
        self.enonce = enonce
        self.reponses = reponses

    def __str__(self):
        res = self.nom + "\n"
        res += "  " + str(self.type) + "\n"
        res += "  " + self.enonce + "\n"
        for r in self.reponses:
            res += "    " + str(r) + "\n"
        return res

    def get_answers(self):
        return self.reponses

    def get_right_answers(self):
        res = []
        for reponse in self.reponses:
            if reponse.est_correcte:
                res.append(reponse)
        return res

    def get_wrong_answers(self):
        res = []
        for reponse in self.reponses:
            if not reponse.est_correcte:
                res.append(reponse)
        return res
