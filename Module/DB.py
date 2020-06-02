import json
import QCM


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


class Base:
    """
    Class that creates creates a dictionnary object from a JSON file
    allows for various operation on the dictionnary before writing it back to the file
    """

    def __init__(self, input_file):
        self.filename = input_file
        with open(input_file, "r") as file:
            self.data = json.load(file)
        self.nextindex = 1
        while str(self.nextindex) in self.data:
            self.nextindex += 1

    def persist(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file)

    def add_question(self, question):
        while str(self.nextindex) in self.data:
            self.nextindex += 1
        self.data[str(self.nextindex)] = question.to_dict()

    def add_multiple(self, questions):
        for question in questions:
            self.add_question(question)

    def del_question(self, index):
        self.data.pop(index)

    def get_question(self, index):
        return question_from_dict(self.data[index])

    def update_question(self, index, question):
        self.data[index] = question.to_dict()

    def select_question_by_name(self, name):
        sel = []
        for index in self.data:
            if self.data[index]["nom"] == name:
                sel.append((index, question_from_dict(self.data[index])))
        return sel

    def select_question_by_tag(self, tags):
        sel = []
        for index in self.data:
            if tag_check(self.data[index]["tags"], tags):
                sel.append((index, question_from_dict(self.data[index])))
        return sel

    def select_question_by_keyword(self, keywords):
        sel = []
        for index in self.data:
            if keyword_check(self.data[index]["enonce"], keywords):
                sel.append((index, question_from_dict(self.data[index])))
        return sel

    def select_all_questions(self):
        sel = []
        for index in self.data:
            sel.append((index, question_from_dict(self.data[index])))
        return sel
