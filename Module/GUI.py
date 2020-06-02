import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import DB
import CL
import Gestion
import QCM
from GUI_Module import LaTeXDisplay

db = None
buffer = []
highest_id = 0
master = Tk()

# Ajout des 3 frames
base_frame = LabelFrame(master, text="Base")
detail_frame = LabelFrame(master, text="Détail")
selection_frame = LabelFrame(master, text="Selection")

# Ajout des listes
list_base = Listbox(base_frame, selectmode=SINGLE)
last_id_base = 0

list_selection = Listbox(selection_frame, selectmode=SINGLE)
list_selection.pack()
last_id_selection = 0

# Ajout des composants frame détail
detail_frame.columnconfigure(1, weight=10)
Label(detail_frame, text="Nom :").grid(row=0, column=0, sticky="W")
question_nom_var = StringVar()
question_nom_entry = Entry(detail_frame, textvariable=question_nom_var)
question_nom_entry.grid(row=0, column=1)

Label(detail_frame, text="Énoncé :").grid(row=1, column=0, sticky="W")
question_enonce_var = StringVar()
question_enonce_entry = Entry(detail_frame, textvariable=question_enonce_var)
question_enonce_entry.grid(row=1, column=1, ipadx=150)

Label(detail_frame, text="Question à choix multiple ?").grid(row=2, column=0, sticky="W")
question_type_var = IntVar()
question_type_check = Checkbutton(detail_frame, variable=question_type_var, onvalue=2, offvalue=1)
question_type_check.grid(row=2, column=1)

reponses_labels = [Label(detail_frame, text="Réponse " + str(i+1) + ":").grid(row=3+i, column=0, sticky="W") for i in range(6)]
reponses_var = [StringVar() for i in range(6)]
reponses_entry = [Entry(detail_frame, textvariable=reponses_var[i]).grid(row=3+i, column=1, ipadx=150) for i in range(6)]
reponses_vraies_var = [IntVar() for i in range(6)]
reponses_vraies_checks = [Checkbutton(detail_frame, variable=reponses_vraies_var[i]) for i in range(6)]
for i in range(6):
    reponses_vraies_checks[i].grid(row=3+i, column=2)

button_preview = Button(detail_frame, text="Prévisualiser la question", state=DISABLED)
button_update = Button(detail_frame, text="Mettre à jour", state=DISABLED)
button_export = Button(detail_frame, text="Selectionner", state=DISABLED)


# Gère l'affichages des détails d'une question
def display_detail_question(question):
    question_nom_var.set(question["nom"])
    question_enonce_var.set(question["enonce"])
    if QCM.type_from_str(question["type"]) == QCM.TypeQCM.QUESTION_MULT:
        question_type_check.select()
    else:
        question_type_check.deselect()
    nbr_reponses = 0
    for reponse in question["reponses"]:
        reponses_var[nbr_reponses].set(reponse["enonce"])
        reponses_vraies_checks[nbr_reponses].select() if reponse["est_correcte"] else reponses_vraies_checks[nbr_reponses].deselect()
        nbr_reponses += 1
    for i in range(nbr_reponses, 6):
        reponses_vraies_checks[i].deselect()
        reponses_var[i].set("")


# Commande des boutons de détail
# Bouton de preview
def button_preview_command():
    selected_question = db.get_question(last_id_base)
    LaTeXDisplay.on_latex(master, DB.question_from_dict(selected_question).to_latex())


button_preview['command'] = button_preview_command
button_preview.grid(row=9, column=0)


# Bouton de mise à jour de la question
def button_update_command():
    global db, last_id_base
    type_qcm = QCM.TypeQCM.QUESTION_MULT if question_type_var.get() == 2 else QCM.TypeQCM.QUESTION
    options = db.get_question(last_id_base)["amc_options"]
    reponses = []
    bonnes_reponses = 0
    for i in range(6):
        if reponses_var[i].get() != "":
            reponses.append(QCM.Reponse((reponses_vraies_var[i].get() == 1), reponses_var[i].get()))
            bonnes_reponses += reponses_vraies_var[i].get()

    if (type_qcm == QCM.TypeQCM.QUESTION_MULT and bonnes_reponses > 0) or (type_qcm == QCM.TypeQCM.QUESTION and bonnes_reponses == 1):
        question = QCM.Question(type_qcm, question_nom_var.get(), options, question_enonce_var.get(), reponses, None)
        db.update_question(last_id_base, question)
    else:
        messagebox.showerror("Mauvais nombre de bonnes réponses", "Veuillez mettre un nombre de réponse(s) approprié")

    list_base.pack(expand=YES, fill=BOTH)


button_update['command'] = button_update_command
button_update.grid(row=9, column=1)


# Bouton d'ajout dans la zone d'export
def button_export_command():
    list_selection.insert(END, list_base.get(int(last_id_base)-1))
    list_selection.pack(expand=YES, fill=BOTH)


button_export['command'] = button_export_command
button_export.grid(row=9, column=2)


# Commande remplacant l'export quand on clique dans la liste de selection
def button_export_retirer():
    list_selection.delete(list_selection.curselection())
    list_selection.pack(expand=YES, fill=BOTH)


# Permet de mettre à jour l'affichage de la question sur laquelle on travaille
def base_onselect(event):
    global db, last_id_base
    selected = list_base.get(list_base.curselection())
    last_id_base = selected[(selected.find(" id: ") + 5):]
    selected_question = db.get_question(last_id_base)
    display_detail_question(selected_question)
    button_preview["state"] = "normal"
    button_update["state"] = "normal"
    button_export["state"] = "normal"
    button_export["text"] = "Selectionner"
    button_export["command"] = button_export_command


list_base.bind('<<ListboxSelect>>', base_onselect)


def selection_onselect(event):
    global db, last_id_selection
    selected = list_selection.get(list_selection.curselection())
    last_id_selection = selected[(selected.find(" id: ") + 5):]
    selected_question = db.get_question(last_id_selection)
    display_detail_question(selected_question)
    button_preview["state"] = "disabled"
    button_update["state"] = "disabled"
    button_export["state"] = "normal"
    button_export["text"] = "Retirer"
    button_export["command"] = button_export_retirer


list_selection.bind('<<ListboxSelect>>', selection_onselect)


# Charge la base de donnée au démarrage de l'app
def load_db():
    global db, highest_id
    location = os.path.dirname(os.path.realpath(__file__))
    base_path = location + "/db.json"
    try:
        db = DB.Base(base_path)
        questions = db.select_all_questions()
        for question in questions:
            list_base.insert(END, question[1]["nom"] + " id: " + str(question[0]))
            list_base.pack(expand=YES, fill=BOTH)
        highest_id = int(questions[-1][0])
        messagebox.showinfo(title="Info BDD", message="Fichier db.json trouvé, base chargée", parent=master)
    except FileNotFoundError:
        with open(base_path, "w") as file:
            file.write("{}")
        db = DB.Base(base_path)
        messagebox.showinfo(title="Info BDD",
                            message="Fichier db.json non trouvé, création d'une base vierge, base chargée",
                            parent=master)


# Fonctions du menu
def import_tex():
    global highest_id
    tex_file_name = filedialog.askopenfilename(title="Veuillez sélectionner un fichier TeX", filetypes=(("fichiers TeX", "*.tex"), ("tous les fichiers", "*.*")))
    Gestion.parse_file(tex_file_name)
    for question in Gestion.buffer:
        db.add_question(question)
        highest_id += 1
        list_base.insert(END, question.nom + " id: " + str(highest_id))

    Gestion.buffer = []
    list_base.pack(expand=YES, fill=BOTH)


def export_tex():
    global db
    to_export = list_selection.get(0, END)
    tex_file_name = filedialog.asksaveasfilename(title="Sauvegarder un fichier TeX", filetypes=(("fichiers TeX", "*.tex"), ("tous les fichiers", "*.*")))
    try:
        with open(tex_file_name, "w") as file:
            for question_str in to_export:
                id = question_str[(question_str.find(" id: ") + 5):]
                question = db.get_question(id)
                question = DB.question_from_dict(question)
                file.write(question.to_latex() + "\n")
    except FileNotFoundError:
        with open(tex_file_name, "x") as file:
            for question_str in to_export:
                id = question_str[(question_str.find(" id: ") + 5):]
                question = db.get_question(id)
                question = DB.question_from_dict(question)
                file.write(question.to_latex() + "\n")


def export_moodle():
    global db
    to_export = list_selection.get(0, END)
    tex_file_name = filedialog.asksaveasfilename(title="Sauvegarder un fichier TeX Moodle",
                                                 filetypes=(("fichiers TeX", "*.tex"), ("tous les fichiers", "*.*")))
    try:
        with open(tex_file_name, "w") as file:
            for question_str in to_export:
                id = question_str[(question_str.find(" id: ") + 5):]
                question = db.get_question(id)
                question = DB.question_from_dict(question)
                file.write(question.to_moodle_latex() + "\n")
    except FileNotFoundError:
        with open(tex_file_name, "x") as file:
            for question_str in to_export:
                id = question_str[(question_str.find(" id: ") + 5):]
                question = db.get_question(id)
                question = DB.question_from_dict(question)
                file.write(question.to_moodle_latex() + "\n")


# Création du menu en top bar
def create_menu():
    menu_bar = Menu(master)
    master['menu'] = menu_bar

    menu_import = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Importer", menu=menu_import)
    menu_import.add_command(label="Importer un fichier TeX...", command=import_tex)

    menu_export = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Exporter", menu=menu_export)
    menu_export.add_command(label="Exporter un QCM...", command=export_tex)
    menu_export.add_command(label="Exporter un fichier Moodle...", command=export_moodle)


def create_frames():
    print("create_frames")
    base_frame.pack(fill=BOTH, expand=YES, side=LEFT)
    selection_frame.pack(fill=BOTH, expand=YES, side=RIGHT)
    detail_frame.pack(fill=BOTH, expand=YES, side=RIGHT)


# Après le chargement de la BDD, on met en place l'interface graphique
def set_gui():
    load_db_label.pack_forget()
    create_menu()
    create_frames()


# Fonction permettant de sauvegarder la base de donnée au moment de quitter l'application
def exit_protocol():
    global db
    if messagebox.askyesno("Quitter", "Voulez-vous sauvegarder la BDD ?"):
        db.persist()
        master.destroy()
    else:
        master.destroy()


master.geometry("800x300")
load_db_label = Label(master, text="Chargement de la BDD...")

load_db_label.pack()
load_db()
master.after(100, set_gui)

master.wm_protocol("WM_DELETE_WINDOW", exit_protocol)

master.mainloop()
