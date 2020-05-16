import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import DB
import CL

db = None
buffer = []
master = Tk()

# Ajout des 3 frames
base_frame = LabelFrame(master, text="Base")
selection_frame = LabelFrame(master, text="Selection")
detail_frame = LabelFrame(master, text="Détail")

# Ajout de la liste
list_base = Listbox(base_frame, selectmode=EXTENDED)


# Charge la base de donnée au démarrage de l'app
def load_db():
    global db
    location = os.path.dirname(os.path.realpath(__file__))
    base_path = location + "/db.json"
    try:
        db = DB.Base(base_path)
        questions = db.get_all_questions()
        for question in questions:
            list_base.insert(END, question["nom"])
            list_base.pack(expand=YES, fill=BOTH)
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
    global db
    tex_file_name = filedialog.askopenfilename(title="Veuillez sélectionner un fichier TeX", filetypes=(("fichiers TeX", "*.tex"), ("tous les fichiers", "*.*")))
    CL.parse_file([tex_file_name])
    for question in CL.buffer:
        db.add_question(question)
        list_base.insert(END, question.nom)
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
