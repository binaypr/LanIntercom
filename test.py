import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

import time


def gui(window, listofhosts):

    scrollbar = ScrollBar(window)
    scrollbar.pack(side = tk.RIGHT, fill = "y")


    messages = tk.Text(font = ('calibre', 14, "normal"))
    messages.pack(fill ="both", expand = True, side = tk.TOP)

    inputVar = tk.StringVar()
    inputField = tk.Text(font = ('calibre', 14, "normal"), height= .1)
    inputField.pack(side= tk.BOTTOM, fill= "both")

    message = inputField.get("1.0",tk.END)
    messages['yscrollcommand'] = scrollb.set
    



window = tk.Tk()

listofhosts = []

gui(window, listofhosts)
window.mainloop()
