from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import Gestion
import QCM
from GUI_Module import LaTeXDisplay

current = None
master = Tk()

# Ajout des 3 frames
base_frame = LabelFrame(master, text="Base")
detail_frame = LabelFrame(master, text="Détail")
selection_frame = LabelFrame(master, text="Selection")

# Ajout des listes
list_view = Listbox(base_frame, selectmode=SINGLE)

list_selection = Listbox(selection_frame, selectmode=SINGLE)
list_selection.pack()

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

Label(detail_frame, text="Cocher si plusieurs réponses vraies :").grid(row=2, column=0, sticky="W")
question_type_var = IntVar()
question_type_check = Checkbutton(detail_frame, variable=question_type_var, onvalue=2, offvalue=1)
question_type_check.grid(row=2, column=1)

NBR_MAX_REPONSES = 6
reponses_labels = [Label(detail_frame, text="Réponse " + str(i + 1) + ":").grid(row=3 + i, column=0, sticky="W") for i
                   in range(NBR_MAX_REPONSES)]
reponses_var = [StringVar() for i in range(NBR_MAX_REPONSES)]
reponses_entry = [Entry(detail_frame, textvariable=reponses_var[i]).grid(row=3 + i, column=1, ipadx=150) for i in
                  range(NBR_MAX_REPONSES)]
reponses_vraies_var = [IntVar() for i in range(NBR_MAX_REPONSES)]
reponses_vraies_checks = [Checkbutton(detail_frame, variable=reponses_vraies_var[i]) for i in range(NBR_MAX_REPONSES)]
for i in range(NBR_MAX_REPONSES):
    reponses_vraies_checks[i].grid(row=3 + i, column=2)

button_preview = Button(detail_frame, text="Prévisualiser la question", state=DISABLED)
button_update = Button(detail_frame, text="Mettre à jour", state=DISABLED)
button_export = Button(detail_frame, text="Selectionner", state=DISABLED)


# Gère l'affichages des détails d'une question
def display_detail_question(question):
    """
    displays the given QCM.Question object in the center of the screen
    :param question: the question to display
    """
    question_nom_var.set(question.nom)
    question_enonce_var.set(question.enonce)
    if question.type == QCM.TypeQCM.QUESTION_MULT:
        question_type_check.select()
    else:
        question_type_check.deselect()
    nbr_reponses = 0
    for reponse in question.reponses:
        reponses_var[nbr_reponses].set(reponse.enonce)
        if reponse.est_correcte:
            reponses_vraies_checks[nbr_reponses].select()
        else:
            reponses_vraies_checks[nbr_reponses].deselect()
        nbr_reponses += 1
    for i in range(nbr_reponses, NBR_MAX_REPONSES):
        reponses_vraies_checks[i].deselect()
        reponses_var[i].set("")


# Commande des boutons de détail
# Bouton de preview
def button_preview_command():
    """
    preview the currently shown question by compiling the LaTeX code
    """
    selected_question = Gestion.get_index(current)
    LaTeXDisplay.on_latex(master, selected_question.to_latex())


button_preview['command'] = button_preview_command
button_preview.grid(row=3 + NBR_MAX_REPONSES, column=0)


# Bouton de mise à jour de la question
def button_update_command():
    """
    updates the currently shown question in the database
    """
    type_qcm = QCM.TypeQCM.QUESTION_MULT if question_type_var.get() == 2 else QCM.TypeQCM.QUESTION
    options = Gestion.get_index(current).amc_options
    reponses = []
    bonnes_reponses = 0
    for i in range(NBR_MAX_REPONSES):
        if reponses_var[i].get() != "":
            reponses.append(QCM.Reponse((reponses_vraies_var[i].get() == 1), reponses_var[i].get()))
            bonnes_reponses += reponses_vraies_var[i].get()
    if (type_qcm == QCM.TypeQCM.QUESTION_MULT and bonnes_reponses > 0) \
            or (type_qcm == QCM.TypeQCM.QUESTION and bonnes_reponses == 1):
        question = QCM.Question(type_qcm, question_nom_var.get(), options, question_enonce_var.get(), reponses)
        Gestion.update_index(current, question)
    else:
        messagebox.showerror("Mauvais nombre de bonnes réponses", "Veuillez mettre un nombre de réponse(s) approprié")
    refresh()


button_update['command'] = button_update_command
button_update.grid(row=3 + NBR_MAX_REPONSES, column=1)


# Bouton d'ajout dans la zone d'export
def button_export_command():
    """
    adds the currently shown question to the selection/export view (rightmost part of the screen)
    """
    Gestion.select_id(current)
    update_selection()


button_export['command'] = button_export_command
button_export.grid(row=3 + NBR_MAX_REPONSES, column=2)


# Commande remplacant l'export quand on clique dans la liste de selection
def button_export_retirer():
    Gestion.remove_sel(list_selection.curselection()[0])
    update_selection()


# Permet de mettre à jour l'affichage de la question sur laquelle on travaille
def base_onselect(event):
    """
    updates the display when a question is selected in the database view (leftmost part of the screen)
    :param event: the Tk event
    """
    global current
    selected = list_view.curselection()[0]
    current = Gestion.view[selected][0]
    display_detail_question(Gestion.view[selected][1])
    button_preview["state"] = "normal"
    button_update["state"] = "normal"
    button_export["state"] = "normal"
    button_export["text"] = "Selectionner"
    button_export["command"] = button_export_command


list_view.bind('<<ListboxSelect>>', base_onselect)


def selection_onselect(event):
    """
    updates the display when a question is selected in the selection view (rightmost part of the screen)
    :param event: the Tk event
    """
    global current
    selected = list_selection.curselection()[0]
    current = Gestion.sel[selected][0]
    display_detail_question(Gestion.sel[selected][1])
    button_preview["state"] = "disabled"
    button_update["state"] = "disabled"
    button_export["state"] = "normal"
    button_export["text"] = "Retirer"
    button_export["command"] = button_export_retirer


list_selection.bind('<<ListboxSelect>>', selection_onselect)


# Charge la base de donnée au démarrage de l'app
def load_db():
    """
    initializes the Gestion module
    the Gestion module will open the database
    this function then updates the database view to show every question in the database
    """
    found = Gestion.init()
    Gestion.view_all()
    update_view()
    if found:
        messagebox.showinfo(title="Info BDD",
                            message="Fichier db.json trouvé, base chargée",
                            parent=master)
    else:
        messagebox.showinfo(title="Info BDD",
                            message="Fichier db.json non trouvé, création d'une base vierge, base chargée",
                            parent=master)


# Fonctions du menu
type_tex = ("fichiers TeX", "*.tex")
type_all = ("tous les fichiers", "*.*")


def import_tex():
    """
    imports a .tex file and saves it directly to the database
    """
    tex_file_name = filedialog.askopenfilename(title="Veuillez sélectionner un fichier TeX",
                                               filetypes=(type_tex, type_all))
    Gestion.parse_file(tex_file_name)
    Gestion.save_bufer()
    Gestion.clear_buffer()
    Gestion.view_all()
    update_view()


def export_tex():
    """
    exports the questions in the selection to a .tex file
    """
    tex_file_name = filedialog.asksaveasfilename(title="Sauvegarder un fichier TeX",
                                                 filetypes=(type_tex, type_all))
    Gestion.export_sel_latex(tex_file_name)


def export_moodle():
    """
    exports the questions in the selection to a .tex file
    """
    tex_file_name = filedialog.asksaveasfilename(title="Sauvegarder un fichier TeX Moodle",
                                                 filetypes=(type_tex, type_all))
    Gestion.export_sel_moodle(tex_file_name)


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
    if messagebox.askyesno("Quitter", "Voulez-vous sauvegarder la BDD ?"):
        Gestion.persist_db()
        master.destroy()
    else:
        master.destroy()


# Fonction permettant d'actualiser la vue
def update_view():
    """
    updates the view list shown on screen to match the internal Gestion.view list
    """
    global list_view
    list_view.delete(0, END)
    for index, question in Gestion.view:
        list_view.insert(END, question.nom + " id: " + index)
        list_view.pack(expand=YES, fill=BOTH)


def update_selection():
    """
    updates the selection list shown on screen to match the internal Gestion.sel list
    """
    global list_selection
    list_selection.delete(0, END)
    for index, question in Gestion.sel:
        list_selection.insert(END, question.nom + " id: " + index)
        list_view.pack(expand=YES, fill=BOTH)


def refresh():
    """
    refresh the current view and selection from the database
    """
    Gestion.refresh_view()
    Gestion.refresh_sel()
    update_view()
    update_selection()


master.geometry("800x300")
load_db_label = Label(master, text="Chargement de la BDD...")

load_db_label.pack()
load_db()
master.after(100, set_gui)

master.wm_protocol("WM_DELETE_WINDOW", exit_protocol)

master.mainloop()
