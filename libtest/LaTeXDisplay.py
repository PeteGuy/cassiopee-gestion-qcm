import sympy as sp
from io import BytesIO
from PIL import Image as PILImage, ImageTk

from tkinter import *


class Root():
    def __init__(self, master):
        # Define the main window and the relevant widgets
        self.master = master
        master.geometry("800x300")
        self.strvar = StringVar()
        self.label = Label(master)
        self.entry = Text(master, width=80, height=10)
        self.button = Button(text="LaTeX!", command=self.on_latex)

        # Pack everything
        self.entry.pack()
        self.button.pack()
        self.label.pack()

    def on_latex(self):
        expr = "$\displaystyle " + self.entry.get("1.0",END) + "$"

        # This creates a ByteIO stream and saves there the output of sympy.preview
        f = BytesIO()
        the_color = "{" + self.master.cget('bg')[1:].upper() + "}"
        sp.preview(expr, euler=False, preamble=r"\documentclass{standalone}"
                                               r"\usepackage{pagecolor}"
                                               r"\usepackage[francais,bloc,completemulti]{automultiplechoice}" 
                                               r"\definecolor{graybg}{HTML}" + the_color +
                                               r"\pagecolor{graybg}"
                                               r"\begin{document}",
                   viewer="BytesIO", output="ps", outputbuffer=f)
        f.seek(0)
        # Open the image as if it were a file. This works only for .ps!
        img = PILImage.open(f)
        # See note at the bottom
        img.load(scale=10)
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), PILImage.BILINEAR)
        photo = ImageTk.PhotoImage(img)
        self.label.config(image=photo)
        self.label.image = photo
        f.close()


master = Tk()
root = Root(master)
master.mainloop()
