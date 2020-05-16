import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import DB
import CL
import QCM

db = None
buffer = []
highest_id = 0
master = Tk()

# Ajout des 3 frames
base_frame = LabelFrame(master, text="Base")
detail_frame = LabelFrame(master, text="Détail")
selection_frame = LabelFrame(master, text="Selection")

# Ajout de la liste
list_base = Listbox(base_frame, selectmode=SINGLE)

# Ajout des composants frame détail
Label(detail_frame, text="Nom :").grid(row=0, column=0)
question_nom_var = StringVar()
question_nom_entry = Entry(detail_frame, textvariable=question_nom_var)
question_nom_entry.grid(row=0, column=1)

Label(detail_frame, text="Énoncé :").grid(row=1, column=0)
question_enonce_var = StringVar()
question_enonce_entry = Entry(detail_frame, textvariable=question_enonce_var)
question_enonce_entry.grid(row=1, column=1)

Label(detail_frame, text="Question à choix multiple ?").grid(row=2, column=0)
question_type_check = Checkbutton(detail_frame)
question_type_check.grid(row=2, column=1)


# Gère l'affichages des détails d'une question
def display_detail_question(question):
    question_nom_var.set(question["nom"])
    question_enonce_var.set(question["enonce"])
    if QCM.type_from_str(question["type"]) == QCM.TypeQCM.QUESTION_MULT:
        question_type_check.select()
    else:
        question_type_check.deselect()


# Permet de mettre à jour l'affichage de la question sur laquelle on travaille
def base_onselect(event):
    global db
    selected = list_base.get(list_base.curselection())
    id = selected[(selected.find(" id: ")+5):]
    selected_question = db.get_question(id)
    display_detail_question(selected_question)


list_base.bind('<<ListboxSelect>>', base_onselect)


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
    CL.parse_file([tex_file_name])
    for question in CL.buffer:
        db.add_question(question)
        highest_id += 1
        list_base.insert(END, question.nom + " id: " + str(highest_id))

    CL.buffer = []
    list_base.pack(expand=YES, fill=BOTH)


# Création du menu en top bar
def create_menu():
    menu_bar = Menu(master)
    master['menu'] = menu_bar

    menu_import = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Importer", menu=menu_import)
    menu_import.add_command(label="Importer un fichier TeX...", command=import_tex)
    menu_import.add_command(label="Importer un fichier JSON...")

    menu_export = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Exporter", menu=menu_export)
    menu_export.add_command(label="Exporter un QCM...")
    menu_export.add_command(label="Exporter un fichier JSON...")


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
    return


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
