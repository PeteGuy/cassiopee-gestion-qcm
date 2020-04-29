import DB
import QCM
import Parser
import os


sel = []
buffer = []
db = None


def main():
    """reads the data from db.json or creates it if missing
    then prompts the user for a command which is then executed
    """

    global db
    global buffer
    global sel
    location = os.path.dirname(os.path.realpath(__file__))
    base_path = location + "\\db.json"
    try:
        db = DB.Base(base_path)
        print("Fichier db.json trouvé, base chargée")
    except FileNotFoundError:
        with open(base_path, "w") as file:
            file.write("{}")
        db = DB.Base(base_path)
        print("Fichier db.json non trouvé, création d'une base vierge, base chargée")

    line = input("GestionQCM >> ")
    command_and_args = line.split()
    command = command_and_args[0]
    args = command_and_args[1:]

    while command != "exit":

        if command == "parsef":
            parse_file(args)

        if command == "printb":
            print_buffer(args)

        if command == "latexb":
            print_latex_buffer(args)

        if command == "clearb":
            buffer = []
            print("Buffer cleared")

        if command == "tagb":
            tag_buffer(args)
            print("Tag applied!")

        if command == "saveb":
            db.add_multiple(buffer)
            print("Buffer saved!")

        if command == "clear":
            sel = []
            print("Selection cleared!")

        if command == "selectbyname":
            select_name(args)

        if command == "selectbytag":
            select_tag(args)

        if command == "print":
            print_selection(args)

        if command == "latex":
            print_latex(args)

        line = input("GestionQCM >> ")
        command_and_args = line.split()
        command = command_and_args[0]
        args = command_and_args[1:]

    db.close()


def parse(arg):
    global buffer
    questions = Parser.parse_latex(arg)
    buffer += questions


def parse_file(args):
    global buffer
    n = len(buffer)
    if len(args) == 0:
        print("Pas de fichier spécifié")
    else:
        for filename in args:
            with open(filename) as file:
                buffer += Parser.parse_latex(file)
        n = len(buffer) - n
        print(str(len(args)) + " fichier(s) parsé(s), " + str(n) + " questions trouvées")
        print(str(len(buffer)) + " questions non sauvegardées")


def print_buffer(args):
    global buffer
    if len(args) == 0:
        for question in buffer:
            print(question)
    else:
        for index in args:
            try:
                print(buffer[int(index)])
            except IndexError:
                print("Index invalide")


def print_latex_buffer(args):
    global buffer
    if len(args) == 0:
        for question in buffer:
            print(question.to_latex())
    else:
        for index in args:
            try:
                print(buffer[int(index)].to_latex())
            except IndexError:
                print("Index invalide")


def tag_buffer(args):
    global buffer
    for tag in args:
        for question in buffer:
            question.add_tag(tag)


def select_name(args):
    global sel
    global db
    nsel = []
    replace = True
    if "-a" in args:
        args.remove("-a")
        replace = False
    for name in args:
        nsel += db.select_question_by_name(name)
    if replace:
        sel = nsel
    else:
        sel += nsel


def select_tag(args):
    global sel
    global db
    replace = True
    if "-a" in args:
        args.remove("-a")
        replace = False
    nsel = db.select_question_by_tag(args)
    if replace:
        sel = nsel
    else:
        sel += nsel


def print_selection(args):
    global sel
    if len(args) == 0:
        for index, question in sel:
            print(question)
    else:
        for index in args:
            try:
                print(sel[int(index)][1])
            except IndexError:
                print("Index invalide")


def print_latex(args):
    global sel
    if len(args) == 0:
        for index, question in sel:
            print(question.to_latex())
    else:
        for index in args:
            try:
                print(sel[int(index)][1].to_latex())
            except IndexError:
                print("Index invalide")


if __name__ == "__main__":
    main()