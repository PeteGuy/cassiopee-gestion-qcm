import json
import QCM


def tag_check(tags, required):
    for tag in required:
        if tag not in tags:
            return False
    return True


def reponse_from_dict(rdict):
    return QCM.Reponse(rdict["est_correcte"], rdict["enonce"])


def question_from_dict(qdict):
    reponses = [reponse_from_dict(rdict) for rdict in qdict["reponses"]]
    return QCM.Question(QCM.type_from_str(qdict["type"]),
                        qdict["nom"],
                        qdict["enonce"],
                        reponses,
                        qdict["tags"])


class Base:

    def __init__(self, input_file):
        self.filename = input_file
        with open(input_file, "r") as file:
            self.data = json.load(file)
        self.nextindex = 1
        while self.nextindex in self.data:
            self.nextindex += 1

    def persist(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file)

    def add_question(self, question):
        while self.nextindex in self.data:
            self.nextindex += 1
        self.data[self.nextindex] = question.to_dict()

    def add_multiple(self, questions):
        for question in questions:
            self.add_question(question)

    def del_question(self, index):
        self.data.pop(index)

    def get_question(self, index):
        return self.data[index]

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
