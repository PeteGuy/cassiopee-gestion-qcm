import DB
import QCM
import Parser
import os


sel = []
buffer = []
db = None

help_message_global = """Application de Gestion de QCMs
Pour obtenir plus d'information sur une commande ">>help <commande>"

commande(variante)
<argument> <?argument optionnel> <arguments multiples>...

Liste des commandes :
    - help <commande> : affiche un message d'aide
    - parsef <fichier>... : ouvre le(s) fichier(s) spécifié(s) et recherche les QCM écrites en LaTeX
    - print(printb) <?index>... : affiche les questions de la sélection (du buffer) ou seulement les indexs spécifiés
    - latex(latexb) <?index>... : affiche le code LaTeX des questions sélectionnées (du buffer) spécifiées
    - save(saveb) : enregistre les modifications sur la sélection (enregistre le buffer) dans la base
    - clear(clearb) : Remet à zéro la sélection (le buffer) sans sauvegarder
    - tag(tagb) <tag>... : applique un tag à la sélection (au buffer)
    - selectbytag, selectbyname <arg>... : sélectionne dans la base suivant un critère
    - exit : enregistre la base et ferme l'application
"""


def main():
    """reads the data from db.json or creates it if missing
    then prompts the user for a command which is then executed
    """

    global db
    global buffer
    global sel
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

    line = input("GestionQCM >> ")
    command_and_args = line.split()
    command = command_and_args[0]
    args = command_and_args[1:]

    while command != "exit":

        if command == "parsef":
            parse_file(args)

        elif command == "persist":
            db.persist()
            print("Le fichier de la base à été mis à jour.")

        elif command == "printb":
            print_buffer(args)

        elif command == "latexb":
            print_latex_buffer(args)

        elif command == "clearb":
            buffer = []
            print("Buffer cleared")

        elif command == "tagb":
            tag_buffer(args)
            print("Tag applied!")

        elif command == "tag":
            tag_selection(args)
            print("Tag applied!")

        elif command == "saveb":
            db.add_multiple(buffer)
            print("Buffer saved!")
            if "-s" in args:
                select_name(["-a"] + [question.nom for question in buffer])
            if "-c" not in args:
                buffer = []
                print("Buffer cleared")

        elif command == "save":
            for index, question in sel:
                db.update_question(index, question)
            print("Modifications saved!")

        elif command == "clear":
            sel = []
            print("Selection cleared!")

        elif command == "selectbyname":
            select_name(args)

        elif command == "selectbytag":
            select_tag(args)

        elif command == "print":
            print_selection(args)

        elif command == "latex":
            print_latex(args)

        elif command == "moodle":
            print_moodle(args)

        elif command == "exportlatex":
            export_latex(args)

        elif command == "exportmoodle":
            export_moodle(args)

        elif command == "help":
            print_help(args)

        else:
            print("Commande inconnue, tapez help pour une liste des commandes")

        line = input("GestionQCM >> ")
        command_and_args = line.split()
        command = command_and_args[0]
        args = command_and_args[1:]

    db.persist()


def parse(arg):
    global buffer
    questions = Parser.parse_latex(arg)
    buffer += questions


def parse_file(args):
    """Parse un ou plusieurs fichiers LaTeX passé(s) en argument.
Les QCMs trouvées sont stockées dans le buffer et non directement ajoutées à la base.
Utilisez ">>saveb" pour sauvegarder les questions trouvées.
    """

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
    """Affiche les QCM du buffer
Si aucun argument n'est spécifié, affiche une courte descrption de toutes les questions.
Si des indexs sont passés en argument, affiche seulement les QCM(s) spécifiée(s) en détails.
    """

    global buffer
    if len(args) == 0:
        for question in buffer:
            print(question.short_str())
    else:
        for index in args:
            try:
                print(buffer[int(index)])
            except IndexError:
                print("Index invalide")


def print_latex_buffer(args):
    """Affiche le code LaTeX des QCM du buffer
Si aucun argument n'est spécifié, affiche toutes les QCM.
Si des indexs sont passés en argument n'affiche que ces derniers.
    """

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


def print_selection(args):
    """Affiche les QCM de la sélection
Si aucun argument n'est spécifié, affiche une courte descrption de toutes les questions.
Si des indexs sont passés en argument, affiche seulement les QCM(s) spécifiée(s) en détails.
    """

    global sel
    if len(args) == 0:
        for index, question in sel:
            print(question.short_str())
    else:
        for index in args:
            try:
                print(sel[int(index)][1])
            except IndexError:
                print("Index invalide")


def print_latex(args):
    """Affiche le code LaTeX des QCM de la sélection
Si aucun argument n'est spécifié, affiche toutes les QCM.
Si des indexs sont passés en argument n'affiche que ces derniers.
    """

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


def print_moodle(args):
    """Affiche le code LaTeX Moodle des QCM de la sélection
    Si aucun argument n'est spécifié, affiche toutes les QCM.
    Si des indexs sont passés en argument n'affiche que ces derniers.
        """

    global sel
    if len(args) == 0:
        for index, question in sel:
            print(question.to_moodle_latex())
    else:
        for index in args:
            try:
                print(sel[int(index)][1].to_moodle_latex())
            except IndexError:
                print("Index invalide")


def tag_buffer(args):
    """Applique un ensemble ce tags à toutes les QCMs du buffer"""
    global buffer
    for tag in args:
        for question in buffer:
            question.add_tag(tag)


def tag_selection(args):
    """Applique un ensemble de tags au questions de la sélection"""
    global sel
    for tag in args:
        for index, question in sel:
            question.add_tag(tag)


def select_name(args):
    """Recherche des QCMs dans la base qui ont le nom spécifié et les ajoutes à la sélection.
Plusieurs noms peuvent êtres recherchés à la fois.

Par défaut la sélection courante est remplacée par le résultat de la requête,
pour ajouter le résultat à la sélection utilisez l'option "-a".
    """

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
    """Recherche des QCMs dans la base qui possèdent l'ensemble des tags passés en argument
et les ajoutes à la sélection.

Par défaut la sélection courante est remplacée par le résultat de la requête,
pour ajouter le résultat à la sélection utilisez l'option "-a".
    """

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


def export_latex(args):
    """Exporte le code LaTeX des QCMs sélectionnées dans le fichier ppassé en argument"""

    global sel
    if len(args) == 0:
        print("Veuillez spécifier un fichier de sortie")
    else:
        try:
            with open(args[0], "w") as file:
                for index, question in sel:
                    file.write(question.to_latex())
        except FileNotFoundError:
            with open(args[0], "x") as file:
                for index, question in sel:
                    file.write(question.to_latex())
        print("Exporté!")


def export_moodle(args):
    """Exporte le code LaTeX moodle des QCMs sélectionnées dans le fichier passé en argument"""

    global sel
    if len(args) == 0:
        print("Veuillez spécifier un fichier de sortie")
    else:
        try:
            with open(args[0], "w") as file:
                for index, question in sel:
                    file.write(question.to_moodle_latex() + "\n")
        except FileNotFoundError:
            with open(args[0], "x") as file:
                for index, question in sel:
                    file.write(question.to_moodle_latex() + "\n")
        print("Exporté!")


def print_help(args):
    """Affiche un message d'aide pour les commandes,
si aucun argument n'est spécifié, affiche un message générique
si des commandes sont spécifiées, affiche leurs messages d'aide respectifs à la suite.
    """

    if len(args) == 0:
        print(help_message_global)
    else:
        for command in args:
            if command == "parsef":
                print(parse_file.__doc__)

            elif command == "persist":
                print("Répercute les modifications de la base sur le disque")

            elif command == "printb":
                print(print_buffer.__doc__)

            elif command == "latexb":
                print(print_latex_buffer.__doc__)

            elif command == "clearb":
                print("Efface le contenu du buffer.\nLe contenu effacé est définitivement perdu.")

            elif command == "tagb":
                print(tag_buffer.__doc__)

            elif command == "saveb":
                print("""Sauvegarde le contenu du buffer dans la base,
par défaut efface le buffer, utilisez l'option "-c" pour conserver le buffer.
Utilisez l'option "-s" pour ajouter le buffer à la sélection immédiatement après.
NOTE : cette sauvegarde n'est effectivement répercutée sur le fichier de la base
qu'après un appel à ">> persist" ou à ">> exit".""")

            elif command == "save":
                print("""Sauvegarde les modification de la sélection dans la base
NOTE : cette sauvegarde n'est effectivement répercutée sur le fichier de la base
qu'après un appel à ">> persist" ou à ">> exit".""")

            elif command == "clear":
                print("Efface le contenu de la sélection.\nToute modification non enregistrée est définitivement perdu.")

            elif command == "selectbyname":
                print(select_name.__doc__)

            elif command == "selectbytag":
                print(select_tag.__doc__)

            elif command == "print":
                print(print_selection.__doc__)

            elif command == "latex":
                print(print_latex.__doc__)

            elif command == "moodle":
                print(print_moodle.__doc__)

            elif command == "exportlatex":
                print(export_latex.__doc__)

            elif command == "exportmoodle":
                print(export_moodle.__doc__)

            else:
                print("""Commande inconnue, tapez "help" pour une liste des commandes""")


if __name__ == "__main__":
    main()