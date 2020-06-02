import DB
import Parser
import os


# This module is the core of the GestionQCM app. every major can and should be done from this module
# All other modules should refrain from using modules other than Gestion as mush as possible
# To use this module, simply import it and execute the init() function
# Almost none of the function in this module handle exceptions and it is the responsability
# of the caller to handle exceptions (such as IndexError)


sel = []
buffer = []
db = None


#
# Basic functions for setting up the system
#


def init():
    """
    initializes a database with the default name and location
    if a database already exists, it is charged, if not it is created
    """
    global db
    location = os.path.dirname(os.path.realpath(__file__))
    base_path = location + "/db.json"
    try:
        db = DB.Base(base_path)
        print("Fichier db.json trouvé, base chargée")
    except FileNotFoundError:
        with open(base_path, "w") as file:
            file.write("{}")
        db = DB.Base(base_path)
        print("Fichier db.json non trouvé, création d'une base vierge, base chargée")


def get_buffer():
    """
    get the reference for the buffer list
    this reference should remain valid after each operation on the list
    :return: the reference
    """
    global buffer
    return buffer


def get_sel():
    """
    get the reference for the selection list
    this reference should remain valid after each operation on the selection
    :return: the reference
    """
    global sel
    return sel


#
# Functions for parsing and exporting
#


def export_sel_latex(filename):
    """
    exports the selection list to a file as LaTeX source code
    uses the AMC LaTeX package
    :param filename: the path to the file
    """
    global sel
    try:
        with open(filename, 'w') as file:
            for index, question in sel:
                file.write(question.to_latex())
    except FileNotFoundError:
        with open(filename, "x") as file:
            for index, question in sel:
                file.write(question.to_latex())


def export_sel_moodle(filename):
    """
    exports the selection list to a file as LaTeX source code
    uses the Moodle LaTeX package
    :param filename: the path to the file
    """
    global sel
    try:
        with open(filename, 'w') as file:
            for index, question in sel:
                file.write(question.to_moodle_latex())
    except FileNotFoundError:
        with open(filename, "x") as file:
            for index, question in sel:
                file.write(question.to_moodle_latex())


def export_buffer_latex(filename):
    """
    exports the buffer list to a file as LaTeX source code
    uses the AMC LaTeX package
    :param filename: the path to the file
    """
    global buffer
    try:
        with open(filename, 'w') as file:
            for question in buffer:
                file.write(question.to_latex())
    except FileNotFoundError:
        with open(filename, "x") as file:
            for question in buffer:
                file.write(question.to_latex())


def export_buffer_moodle(filename):
    """
    exports the selection list to a file as LaTeX source code
    uses the Moodle LaTeX package
    :param filename: the path to the file
    """
    global buffer
    try:
        with open(filename, 'w') as file:
            for question in buffer:
                file.write(question.to_moodle_latex())
    except FileNotFoundError:
        with open(filename, "x") as file:
            for question in buffer:
                file.write(question.to_moodle_latex())


def get_latex_str(index):
    """
    returns a LaTeX string for the question in the specified index of the selection
    :param index: th index of the selection list
    :return: the string
    """
    global sel
    return sel[index][1].to_latex()


def get_moodle_str(index):
    """
    returns a moodle LaTeX string for the question in the specified index of the selection
    :param index: th index of the selection list
    :return: the string
    """
    global sel
    return sel[index][1].to_moodle_latex()


def get_buffer_latex_str(index):
    """
    returns a LaTeX string for the question in the specified index of the selection
    :param index: th index of the selection list
    :return: the string
    """
    global buffer
    return buffer[index].to_latex()


def get_buffer_moodle_str(index):
    """
    returns a moodle LaTeX string for the question in the specified index of the selection
    :param index: th index of the selection list
    :return: the string
    """
    global buffer
    return buffer[index].to_moodle_latex()


def get_all_latex_str():
    """
    return all the LaTeX string for each question in the selction
    :return: a list containing all the string
    """
    global sel
    res = []
    for index, question in sel:
        res.append(question.to_latex())
    return res


def get_all_moodle_str():
    """
    return all the moodle LaTeX string for each question in the selction
    :return: a list containing all the string
    """
    global sel
    res = []
    for index, question in sel:
        res.append(question.to_moodle_latex())
    return res


def get_all_buffer_latex_str():
    """
    return all the LaTeX string for each question in the selction
    :return: a list containing all the string
    """
    global buffer
    res = []
    for question in buffer:
        res.append(question.to_latex())
    return res


def get_all_buffer_moodle_str():
    """
    return all the moodle LaTeX string for each question in the selction
    :return: a list containing all the string
    """
    global buffer
    res = []
    for question in buffer:
        res.append(question.to_moodle_latex())
    return res


def parse_file(filename):
    """
    parses a latex file and stores the result in the buffer list
    :param filename: the path to a latex source code
    :returns the number of questions found
    """
    global buffer
    n = len(buffer)
    with open(filename, 'r') as file:
        buffer += Parser.parse_latex(file)
    return len(buffer) - n


#
# Functions for basic manipulation of the selction, buffer an db
#


def save_bufer():
    """
    saves the content of the buffer in the database
    """
    global buffer
    db.add_multiple(buffer)


def clear_buffer():
    """
    clears the buffer
    """
    global buffer
    buffer.clear()


def save_sel():
    """
    saves the modifications done to the questions in the selection in the database
    """
    global sel
    global db
    for index, question in sel:
        db.update_question(index, question)


def clear_sel():
    """
    clears the selection
    """
    global sel
    sel.clear()


def remove_duplicates():
    """
    removes duplicate entry in the selection
    this function should be called after every addition to the selection
    as it relies on the unicity of the index in the db,
    any modification to this property may break the function
    """
    global sel
    seen = []
    for i in range(len(sel)):
        if sel[i][0] in seen:
            sel.pop(i)
        else:
            seen.append(sel[i][0])


def persist_db():
    """
    forces the database to write data to disk
    """
    db.persist()


#
# Functions for manipulation the questions in the selection and buffer
#


def apply_tag(index, tag):
    """
    adds the given tag to a question in the selection
    :param index: the index of the question in the selection list
    :param tag: the tag to apply (must be a string for the database to work properly)
    """
    global sel
    sel[index][1].add_tag(tag)


def apply_tag_all(tag):
    """
    adds the given tag to all the questions in the selection
    :param tag: the tag to add
    """
    global sel
    for index, question in sel:
        question.add_tag(tag)


def apply_tag_buffer(index, tag):
    """
    adds the given tag to a question in the buffer
    :param index: the index of the question in the buffer list
    :param tag: the tag to apply (must be a string for the database to work properly)
    """
    global buffer
    buffer[index].add_tag(tag)


def apply_tag_all_buffer(tag):
    """
    adds the given tag to all the questions in the buffer
    :param tag: the tag to add
    """
    global buffer
    for question in buffer:
        question.add_tag(tag)


def get_sel_str(index):
    """
    returns the string corresponding to the specified question in the selection
    :param index: the index of the question in the selection
    :return: the desired string
    """
    global sel
    return str(sel[index][1])


def get_short_sel_str(index):
    """
    returns a short string corresponding to the specified question in the selection
    :param index: the index of the question in the selection
    :return: the desired string
    """
    global sel
    return sel[index][1].short_str()


def get_buffer_str(index):
    """
    returns the string corresponding to the specified question in the selection
    :param index: the index of the question in the selection
    :return: the desired string
    """
    global buffer
    return str(buffer[index])


def get_short_buffer_str(index):
    """
    returns a short string corresponding to the specified question in the selection
    :param index: the index of the question in the selection
    :return: the desired string
    """
    global buffer
    return buffer[index].short_str()


def get_all_sel_str():
    """
    returns all the str(questions) for the questions in the selection
    :return: a list of the desired strings
    """
    global sel
    res = []
    for index, question in sel:
        res.append(str(question))
    return res


def get_all_short_sel_str():
    """
    returns a short string for every question in the selection
    :return: a list of the desired strings
    """
    global sel
    res = []
    for index, question in sel:
        res.append(question.short_str())
    return res


def get_all_buffer_str():
    """
    returns all the str(questions) for the questions in the bufer
    :return: a list of the desired strings
    """
    global buffer
    res = []
    for question in buffer:
        res.append(str(question))
    return res


def get_all_short_buffer_str():
    """
    returns a short string for every question in the buffer
    :return: a list of the desired strings
    """
    global buffer
    res = []
    for question in buffer:
        res.append(question.short_str())
    return res


#
# functions for selecting questions from the db to the selection
#


def select_name(name):
    """
    appends the questions with the specified name to the selection list
    :param name: the name to search
    """
    global db
    global sel
    for question in db.select_question_by_name(name):
        sel.append(question)
    remove_duplicates()


def select_tags(tags):
    """
    appends the questions with the specified tags to the selection list
    :param tags: the tags to search
    """
    global db
    global sel
    for question in db.select_question_by_tag(tags):
        sel.append(question)
    remove_duplicates()


def select_keywords(keywords):
    """
    appends the questions with the specified keywords to the selection list
    note : the keywords are only searched for in the text of the questions
    (not the name nor the answers)
    :param keywords: the keywords to search
    """
    global db
    global sel
    for question in db.select_question_by_keyword(keywords):
        sel.append(question)
    remove_duplicates()


def select_all():
    """
    puts all the questions in the selection list
    clears the selection beforehand so that there is no need to call remove_duplicates()
    """
    global db
    global sel
    clear_sel()
    for question in db.select_all_questions():
        sel.append(question)
