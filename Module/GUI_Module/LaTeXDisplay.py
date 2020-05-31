import os

import sympy as sp
from io import BytesIO
from PIL import Image as PILImage, ImageTk

from tkinter import *


def on_latex(master, latex_str):
    preview_window = Toplevel(master)
    label = Label(preview_window)

    expr = latex_str + "\\end{document}"

    styles_location = os.path.dirname(os.path.realpath(__file__)) + "/src_styles"

    the_color = "{" + master.cget('bg')[1:].upper() + "}"
    preamble = r"\newcommand{\pathSrcStyleFiles}{" + styles_location + "}"
    preamble += r"\documentclass{article}"
    preamble += r"\usepackage{pagecolor}"
    preamble += r"\usepackage[utf8x]{inputenc}"
    preamble += r"\usepackage[T1]{fontenc}"
    preamble += r"\usepackage{automultiplechoice}"
    preamble += r"\usepackage{amssymb}"
    preamble += r"\usepackage{amsmath}"
    #r"\definecolor{graybg}{HTML}" + the_color +
    #r"\pagecolor{graybg}"
    preamble += r"\input{\pathSrcStyleFiles/defGras.tex}"
    preamble += r"\input{\pathSrcStyleFiles/defCdes.tex}"
    preamble += r"\begin{document}"
    # This creates a ByteIO stream and saves there the output of sympy.preview
    f = BytesIO()

    sp.preview(expr, euler=False, preamble=preamble,
               viewer="BytesIO", output="ps", outputbuffer=f)
    f.seek(0)
    # Open the image as if it were a file. This works only for .ps!
    img = PILImage.open(f)
    # See note at the bottom
    img.load(scale=5)
    img = img.resize((int(img.size[0] / 3), int(img.size[1] / 3)), PILImage.BILINEAR)

    width, height = img.size
    left = width/8
    top = height/9
    right = width
    bottom = height/3.5
    img = img.crop((left, top, right, bottom))

    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo
    f.close()

    label.pack()
    preview_window_width = str(int(right-left))
    preview_window_height = str(int(bottom-top))
    preview_window.geometry(preview_window_width + "x" + preview_window_height)
    preview_window.resizable(False, False)
    preview_window.mainloop()




