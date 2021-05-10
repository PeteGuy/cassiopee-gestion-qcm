from enum import Enum
import string


# This module defines the Question class used by the rest of the GestionQCM app
# The class contains all the methods necessary to manipulate and export a question
# Creating a question from a LaTeX source code otherwise requires the use of the Parser module


#
# Class and functions for types of QCM
#


class TypeQCM(Enum):
    """Small class to represent the type of a QCM without strings"""
    QUESTION = 1
    QUESTION_MULT = 2


def type_from_str(string):
    """
    Allows the conversion of the QCM type from LaTeX
    :param string: The LaTeX code of the type
    :returns the corresponding QCM.TypeQCM
    """
    if string == "question":
        return TypeQCM.QUESTION
    elif string == "questionmult":
        return TypeQCM.QUESTION_MULT


def str_from_type(type_qcm):
    """
    Converts TypeQCM back to LaTeX code
    :param type_qcm: the QCM.TypeQCM to convert
    :returns the string of LaTeX code
    """
    if type_qcm == TypeQCM.QUESTION:
        return "question"
    elif type_qcm == TypeQCM.QUESTION_MULT:
        return "questionmult"


def moodle_from_type(type_qcm):
    """
    Converts TypeQCM to moodle LaTeX code
    :param type_qcm: the QCM.TypeQCM to convert
    :returns the string of LaTeX code
    """
    if type_qcm == TypeQCM.QUESTION:
        return "single"
    elif type_qcm == TypeQCM.QUESTION_MULT:
        return "multiple"


#
# Reponse and Question classes
#


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

    def to_moodle_latex(self):
        if self.est_correcte:
            return "\\item* " + self.enonce
        else:
            return "\\item " + self.enonce


class Question:
    """Class representing a full QCM"""

    def __init__(self, type_qcm, nom, options, enonce, reponses=None, tags=None,numberColumn=1):
        if tags is None:
            tags = []
        if reponses is None:
            reponses = []
        self.type = type_qcm
        self.nom = nom
        self.amc_options = options
        self.enonce = enonce.strip()
        self.reponses = reponses
        self.tags = tags   
        self.numberColumn = numberColumn

    def __str__(self):
        res = self.nom + "\n"
        res += str(self.type) + "\n"
        res += self.enonce + "\n"
        for r in self.reponses:
            res += "  " + str(r) + "\n"
        res += "options = " + str(self.amc_options) + "\n"
        res += "tags = " + str(self.tags)
        return res

    def short_str(self):
        """
        Creates a short description that does not contain every field in the object
        :returns a short descriptive string of the question
        """
        return self.nom + " {" + str(self.type)[8:] + "} " + str(self.tags) + "\n" + self.enonce[:100].replace('\n', '').rstrip(string.ascii_letters + string.digits + string.punctuation) + "...\n"

    def to_dict(self, index):
        """
        creates a dictionnary representing the object
        all the fields correspond to a key in the resulting dictionnary
        this function is used for the JSON dump
        :returns a dictionnary object representing the question
        """


        res = {
            "id":   index,
            "type": str_from_type(self.type),
            "nom": self.nom,
            "amc_options": self.amc_options,
            "enonce": self.enonce,
            "reponses": [rep.__dict__ for rep in self.reponses],
            "numberColumn":self.numberColumn,
            "tags": self.tags
        }
        return res

    def to_latex(self):
        """
        Creates LaTeX code to represent the question using the AMC LaTeX package
        :returns a string of LaTeX source code
        """
        
        res = "\\begin{" + str_from_type(self.type) + "}{" + self.nom + "}\n"
        
        for option in self.amc_options:
            res += "  " + option + "\n"
        res += "  " + self.enonce.replace("\n", "\n  ") + "\n"
        
        if self.numberColumn != 1:
            res+="\\begin{multicols}{"+self.numberColumn+"}\n"
        
            
            #print(self.numberColumn)
           
            
            
        res += "  \\begin{reponses}\n"
        for reponse in self.reponses:
            res += "    " + reponse.to_latex() + "\n"
        res += "  \\end{reponses}\n"
        if self.numberColumn != 1:
            res+="\\end{multicols}\n"
        res += "\\end{" + str_from_type(self.type) + "}" + "\n"
        return res

    def to_moodle_latex(self):
        """
        Creates LaTeX code to represent the question using the Moodle LaTeX package
        :returns a string of LaTeX source code
        """
        res = "\\begin{multi}[" + moodle_from_type(self.type) + "]{" + self.nom + "}\n"
        res += "  " + self.enonce.replace("\n", "\n  ") + "\n"
        for reponse in self.reponses:
            res += "  " + reponse.to_moodle_latex() + "\n"
        res += "\\end{multi}" + "\n"
        return res


    def get_name(self):
        """
        :return: The name of the question
        """
        return self.nom

    def get_answers(self):
        """
        :return: The list of all the answers
        """
        return self.reponses

    def get_right_answers(self):
        """
        :return: A list containing the right answers
        """
        return [reponse for reponse in self.reponses if reponse.est_correcte]

    def get_wrong_answers(self):
        """
        :return: A list containing the wrong answers
        """
        return [reponse for reponse in self.reponses if not reponse.est_correcte]

    def add_tag(self, tag):
        """
        adds a tag to the question while avoiding duplicates
        :param tag: the tag to add (preferably a string to avoid conflict when saving to JSON)
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        """
        removes a tag (if the tag is absent nothing is done)
        :param tag: the tag to remove
        """
        self.tags.remove(tag)
