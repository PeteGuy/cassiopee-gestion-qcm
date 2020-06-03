import json
import QCM


# this module iplements a simple databse based on a json file
# this databse is extremely rudimentary but in exchange, the json file
# can be reused easily with any other tool


#
# Utilitary functions
#


def tag_check(tags, required):
    """
    Checks if the required tags are present in a list of tags
    :param tags: the list of tags to chack
    :param required: the list of required tags
    :return: the answer
    """
    for tag in required:
        if tag not in tags:
            return False
    return True


def keyword_check(text, keywords):
    """
    Check if a text contains all the required keywords
    :param text: the text to check
    :param keywords: the list of keywords
    :return: the answer
    """
    for keyword in keywords:
        if keyword not in text:
            return False
    return True


def reponse_from_dict(rdict):
    """
    creates a QCM.Reponse object from a dict
    :param rdict: the dict from the database
    :return: the QCM.Reponse object
    """
    return QCM.Reponse(rdict["est_correcte"], rdict["enonce"])


def question_from_dict(qdict):
    """
    creates a QCM.Question object from a dict
    :param qdict: the dict from the database
    :return: the QCM.Question object
    """
    reponses = [reponse_from_dict(rdict) for rdict in qdict["reponses"]]
    return QCM.Question(QCM.type_from_str(qdict["type"]),
                        qdict["nom"],
                        qdict["amc_options"],
                        qdict["enonce"],
                        reponses,
                        qdict["tags"])


#
# Database definition
#


class Base:
    """
    Class that creates creates a dictionnary object from a JSON file
    allows for various operation on the dictionnary before writing it back to the file
    """

    def __init__(self, input_file):
        """
        open a .json file as a database and extract the data to create a Base object
        :param input_file: the database .json file
        """
        self.filename = input_file
        with open(input_file, "r") as file:
            self.data = json.load(file)
        self.nextindex = 1
        # We search for the next valid unused index value in the database
        while str(self.nextindex) in self.data:
            self.nextindex += 1

    def persist(self):
        """write the database back to the disk"""
        with open(self.filename, "w") as file:
            json.dump(self.data, file)

    def add_question(self, question):
        """
        adds a question to the database
        :param question: the QCM.Question object to add
        """
        # We search for the next valid unused index value in the database
        while str(self.nextindex) in self.data:
            self.nextindex += 1
        # json objects are like python dictionnaries so we convert our object into one
        # the keys of a json object must be strings so our unique indexes are converted to strings
        self.data[str(self.nextindex)] = question.to_dict()

    def add_multiple(self, questions):
        """
        adds multiple questions
        :param questions: a list of QCM.Question objects
        """
        for question in questions:
            self.add_question(question)

    def del_question(self, index):
        """
        deletes a question from the database
        :param index: the string index of the question to remove
        """
        self.data.pop(index)

    def get_question(self, index):
        """
        returns the QCM.Question object at the given index
        this method does not handle exceptions
        :param index: the index wanted
        :return: the QCm.Question object
        """
        return question_from_dict(self.data[index])

    def update_question(self, index, question):
        """
        replaces the question at the given index in the database with the one
        given as an argument
        NOTE : if the index does not exist, the question is simply added
        :param index: the index at which to replace
        :param question: the new question object to put at the given index
        """
        self.data[index] = question.to_dict()

    def question_by_name(self, name):
        """
        return the questions in the database that match the given name
        :param name: the name string to search for
        :return: a list of matching questions and their indexes
        """
        sel = []
        for index in self.data:
            if self.data[index]["nom"] == name:
                sel.append((index, question_from_dict(self.data[index])))
        return sel

    def question_by_tag(self, tags):
        """
        returns the questions in the database that match the given tags
        NOTE : to be returned by this method a question must have ALL the given tags
        :param tags: the list of required tags to search for
        :return: a list of matching questions and their indexes
        """
        sel = []
        for index in self.data:
            if tag_check(self.data[index]["tags"], tags):
                sel.append((index, question_from_dict(self.data[index])))
        return sel

    def question_by_keyword(self, keywords):
        """
        returns the questions in the database that match the given keywords
        NOTE : each question must contain ALL given keywords in its enonce to be returned
        :param keywords: the list of required keywords to search for
        :return: a list of matching questions and their indexes
        """
        sel = []
        for index in self.data:
            if keyword_check(self.data[index]["enonce"], keywords):
                sel.append((index, question_from_dict(self.data[index])))
        return sel

    def all_questions(self):
        """
        returns all the questions in the database
        :return: a liste of tuples (index, question) containing every questions
        """
        sel = []
        for index in self.data:
            sel.append((index, question_from_dict(self.data[index])))
        return sel
