from enum import Enum


class TypeQCM(Enum):
    """Small class to represent the type of a QCM without strings"""
    QUESTION = 1
    QUESTION_MULT = 2


def type_from_str(string):
    """Allows the conversion of the QCM type from LaTeX"""
    if string == "question":
        return TypeQCM.QUESTION
    elif string == "questionmult":
        return TypeQCM.QUESTION_MULT


def str_from_type(type_qcm):
    """Brings the QCM type back to LaTeX"""
    if type_qcm == TypeQCM.QUESTION:
        return "question"
    elif type_qcm == TypeQCM.QUESTION_MULT:
        return "questionmult"


class Reponse:
    """Class representing an answer"""

    def __init__(self, est_correcte, enonce):
        self.est_correcte = est_correcte
        self.enonce = enonce

    def __str__(self):
        if self.est_correcte:
            return "bonne : " + self.enonce
        else:
            return "mauvaise : " + self.enonce

    def to_latex(self):
        if self.est_correcte:
            return "\\bonne{" + self.enonce + "}"
        else:
            return "\\mauvaise{" + self.enonce + "}"


class Question:
    """Class representing a full QCM"""

    def __init__(self, type_qcm, nom, enonce, reponses=None, tags=None):
        if tags is None:
            tags = []
        if reponses is None:
            reponses = []
        self.type = type_qcm
        self.nom = nom
        self.enonce = enonce.strip()
        self.reponses = reponses
        self.tags = tags

    def __str__(self):
        """Returns a string for displaying"""
        res = self.nom + "\n"
        res += str(self.type) + "\n"
        res += self.enonce + "\n"
        for r in self.reponses:
            res += "  " + str(r) + "\n"
        res += "tags = " + str(self.tags)
        return res

    def to_dict(self):
        """creates a dictionnary representing the object
        all the fields correspond to a key in the resulting dictionnary
        this function is used for the JSON dump
        """
        res = {
            "type": str_from_type(self.type),
            "nom": self.nom,
            "enonce": self.enonce,
            "reponses": [rep.__dict__ for rep in self.reponses],
            "tags": self.tags
        }
        return res

    def to_latex(self):
        res = "\\begin{" + str_from_type(self.type) + "}{" + self.nom + "}\n"
        res += "  " + self.enonce.replace("\n", "\n  ") + "\n"
        res += "  \\begin{reponses}\n"
        for reponse in self.reponses:
            res += "    " + reponse.to_latex() + "\n"
        res += "  \\end{reponses}\n"
        res += "\\end{" + str_from_type(self.type) + "}"
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

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)




