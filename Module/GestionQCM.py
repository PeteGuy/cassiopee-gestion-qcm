from enum import Enum


class TypeQCM(Enum):
    QUESTION = 1
    QUESTION_MULT = 2


class Reponse:

    def __init__(self, est_correcte, enonce):
        self.est_correcte = est_correcte
        self.enonce = enonce


class Question:

    def __init__(self, type_qcm, enonce, reponses):
        self.type = type_qcm
        self.enonce = enonce
        self.reponses = reponses

    def get_answers(self):
        return self.reponses

    def get_right_answers(self):
        res = []
        for reponse in self.reponses :
            if reponse.est_correcte:
                res.append(reponse)
        return res

    def get_wrong_answers(self):
        res =[]
        for reponse in self.reponses :
            if not reponse.est_correcte:
                res.append(reponse)
        return res
