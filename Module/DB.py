import json


class Base:

    def __init__(self, input_file):
        self.filename = input_file
        with open(input_file, "r") as file:
            self.data = json.load(file)
        self.nextindex = 1
        while self.nextindex in self.data:
            self.nextindex += 1

    def close(self):
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
