import Gestion


# This module is responsible for creating a command line tool to use the app
# the core of the app located in the Gestion module can be used without this module
# but this module makes it harder to mess up.
# In this module the "view" (database view) and "selection" (selection for export)
# are merged together to simplify the process of selecting questions.
# Otherwise this module simply wraps the Gestion module by providing some error handling
# and help massages


help_message_global = """Application de Gestion de QCMs
Pour obtenir plus d'information sur une commande ">>help <commande>"

commande(variante)
<argument> <?argument optionnel> <arguments multiples>...

Liste des commandes :
    - help <commande> : affiche un message d'aide
    - parsef <fichier>... : ouvre le(s) fichier(s) spécifié(s) et recherche les QCM écrites en LaTeX
    - print(printb) <?index>... : affiche les questions de la sélection (du buffer) ou seulement les indexs spécifiés
    - latex(latexb) <?index>... : affiche le code LaTeX des questions sélectionnées (du buffer) spécifiées
    - moodle(moodleb) <?index>... : affiche le code LaTeX moodle des questions sélectionnées (du buffer) spécifiées
    - save(saveb) : enregistre les modifications sur la sélection (enregistre le buffer) dans la base
    - clear(clearb) : Remet à zéro la sélection (le buffer) sans sauvegarder
    - remove(removeb) <index>... : enlève les questions aux indexs voulues de la sélection (du buffer)
    - tag(tagb) <tag>... : applique un tag à la sélection (au buffer)
    - selectbytag, selectbyname, selectbykeyword <arg>... : sélectionne dans la base suivant un critère
    - exportlatex (exportmoodle) <fichier> : exporte la sélection au format LaTeX (Moodle LaTeX) dans le fichier
    - exit : enregistre la base et ferme l'application
"""

index_error = "Index Invalide!"


def main():
    """
    reads the data from db.json or creates it if missing
    then prompts the user for a command which is then executed
    """

    Gestion.init()

    line = input("GestionQCM >> ")
    command_and_args = line.split()
    command = command_and_args[0]
    args = command_and_args[1:]

    while command != "exit":

        if command == "parsef":
            parse_file(args)

        elif command == "persist":
            Gestion.persist_db()
            print("Le fichier de la base à été mis à jour.")

        elif command == "printb":
            print_buffer(args)

        elif command == "latexb":
            print_latex_buffer(args)

        elif command == "moodleb":
            print_moodle_buffer(args)

        elif command == "clearb":
            Gestion.clear_buffer()
            print("Buffer cleared")

        elif command == "removeb":
            remove_buffer(args)

        elif command == "tagb":
            tag_buffer(args)
            print("Tag applied!")

        elif command == "tag":
            tag_selection(args)
            print("Tag applied!")

        elif command == "saveb":
            Gestion.save_bufer()
            print("Buffer saved!")
            if "-s" in args:
                Gestion.select_name(["-a"] + [question.nom for question in Gestion.buffer])
            if "-c" not in args:
                Gestion.clear_buffer()
                print("Buffer cleared")

        elif command == "save":
            Gestion.save_sel()
            print("Modifications saved!")

        elif command == "clear":
            Gestion.clear_sel()
            print("Selection cleared!")

        elif command == "remove":
            remove_selection(args)

        elif command == "selectbyname":
            select_name(args)

        elif command == "selectbytag":
            select_tag(args)

        elif command == "selectbykeyword":
            select_keyword(args)

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

    Gestion.persist_db()
    print("base de donnée sauvegardée, arrêt...")


#
# Parse functions
#


def parse_file(args):
    """Parse un ou plusieurs fichiers LaTeX passé(s) en argument.
Les QCMs trouvées sont stockées dans le buffer et non directement ajoutées à la base.
Utilisez ">>saveb" pour sauvegarder les questions trouvées.
    """

    if len(args) == 0:
        print("Pas de fichier spécifié")
    else:
        n = 0
        for filename in args:
            n += Gestion.parse_file(filename)
        print(str(len(args)) + " fichier(s) parsé(s), " + str(n) + " questions trouvées")
        print(str(len(Gestion.buffer)) + " questions non sauvegardées")


#
# Print Functions
#


def print_buffer(args):
    """Affiche les QCM du buffer
Si aucun argument n'est spécifié, affiche une courte descrption de toutes les questions.
Si des indexs sont passés en argument, affiche seulement les QCM(s) spécifiée(s) en détails.
    """

    if len(args) == 0:
        for string in Gestion.get_all_short_buffer_str():
            print(string)
    else:
        for index in args:
            try:
                print(Gestion.get_buffer_str(index))
            except IndexError:
                print(index_error)


def print_latex_buffer(args):
    """Affiche le code LaTeX des QCM du buffer
Si aucun argument n'est spécifié, affiche toutes les QCM.
Si des indexs sont passés en argument n'affiche que ces derniers.
    """

    if len(args) == 0:
        for question in Gestion.get_all_buffer_latex_str():
            print(question)
    else:
        for index in args:
            try:
                print(Gestion.get_buffer_latex_str(index))
            except IndexError:
                print(index_error)


def print_moodle_buffer(args):
    """Affiche le code LaTeX Moodle des QCM du buffer
Si aucun argument n'est spécifié, affiche toutes les QCM.
Si des indexs sont passés en argument n'affiche que ces derniers.
    """

    if len(args) == 0:
        for question in Gestion.get_all_buffer_moodle_str():
            print(question)
    else:
        for index in args:
            try:
                print(Gestion.get_buffer_moodle_str(index))
            except IndexError:
                print(index_error)


def print_selection(args):
    """Affiche les QCM de la sélection
Si aucun argument n'est spécifié, affiche une courte descrption de toutes les questions.
Si des indexs sont passés en argument, affiche seulement les QCM(s) spécifiée(s) en détails.
    """

    if len(args) == 0:
        for string in Gestion.get_all_short_sel_str():
            print(string)
    else:
        for index in args:
            try:
                print(Gestion.get_sel_str(index))
            except IndexError:
                print(index_error)


def print_latex(args):
    """Affiche le code LaTeX des QCM de la sélection
Si aucun argument n'est spécifié, affiche toutes les QCM.
Si des indexs sont passés en argument n'affiche que ces derniers.
    """

    if len(args) == 0:
        for question in Gestion.get_all_latex_str():
            print(question)
    else:
        for index in args:
            try:
                print(Gestion.get_latex_str(index))
            except IndexError:
                print(index_error)


def print_moodle(args):
    """Affiche le code LaTeX Moodle des QCM de la sélection
Si aucun argument n'est spécifié, affiche toutes les QCM.
Si des indexs sont passés en argument n'affiche que ces derniers.
    """

    if len(args) == 0:
        for question in Gestion.get_all_moodle_str():
            print(question)
    else:
        for index in args:
            try:
                print(Gestion.get_moodle_str(index))
            except IndexError:
                print(index_error)


#
# Tag functions
#


def tag_buffer(args):
    """Applique un ensemble ce tags à toutes les QCMs du buffer"""
    for tag in args:
        Gestion.apply_tag_all_buffer(tag)


def tag_selection(args):
    """Applique un ensemble de tags au questions de la sélection"""
    for tag in args:
        Gestion.apply_tag_all(tag)


#
# Remove functions
#


def remove_buffer(args):
    """Retire les question voulues du buffer"""
    for index in args:
        try:
            Gestion.remove_buffer(index)
        except IndexError:
            print(index_error)


def remove_selection(args):
    """retire les questions voulues de la sélection"""
    for index in args:
        try:
            Gestion.remove_sel(index)
        except IndexError:
            print(index_error)


#
# Select functions
#


def select_name(args):
    """Recherche des QCMs dans la base qui ont le nom spécifié et les ajoutes à la sélection.
Plusieurs noms peuvent êtres recherchés à la fois.

Par défaut la sélection courante est remplacée par le résultat de la requête,
pour ajouter le résultat à la sélection utilisez l'option "-a".
    """

    if "-a" in args:
        args.remove("-a")
        Gestion.clear_sel()
    for name in args:
        Gestion.select_name(name)


def select_tag(args):
    """Recherche des QCMs dans la base qui possèdent l'ensemble des tags passés en argument
et les ajoutes à la sélection.

Par défaut la sélection courante est remplacée par le résultat de la requête,
pour ajouter le résultat à la sélection utilisez l'option "-a".
    """

    if "-a" in args:
        args.remove("-a")
        Gestion.clear_sel()
    Gestion.select_tags(args)


def select_keyword(args):
    """recherche des QCMs dans la base qui possèdent l'ensemble des mots-clefs passés en argument dans leur énoncé
et les ajountent à la sélection.

Par défaut la sélection courante est remplacée par le résultat de la requête,
pour ajouter le résultat à la sélection utilisez l'option "-a".
    """

    if "-a" in args:
        args.remove("-a")
        Gestion.clear_sel()
    Gestion.select_keywords(args)


#
# Export functions
#


def export_latex(args):
    """Exporte le code LaTeX des QCMs sélectionnées dans le fichier ppassé en argument"""

    if len(args) == 0:
        print("Veuillez spécifier un fichier de sortie")
    else:
        Gestion.export_sel_latex(args[0])
        print("Exporté!")


def export_moodle(args):
    """Exporte le code LaTeX moodle des QCMs sélectionnées dans le fichier passé en argument"""

    if len(args) == 0:
        print("Veuillez spécifier un fichier de sortie")
    else:
        Gestion.export_sel_moodle(args[0])
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

            elif command == "moodleb":
                print(print_moodle_buffer.__doc__)

            elif command == "clearb":
                print("Efface le contenu du buffer.\nLe contenu effacé est définitivement perdu.")

            elif command == "removeb":
                print(remove_buffer.__doc__)

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
                print("Efface le contenu de la sélection.\n"
                      "Toute modification non enregistrée est définitivement perdu.")

            elif command == "remove":
                print(remove_selection.__doc__)

            elif command == "selectbyname":
                print(select_name.__doc__)

            elif command == "selectbytag":
                print(select_tag.__doc__)

            elif command == "seletbykeyword":
                print(select_keyword.__doc__)

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
