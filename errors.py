# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 3/11/2022
# Description:
import tkinter as tk


class ErrorBox:
    def __init__(self, root, message: str):
        window = tk.Toplevel(root)
        window.title('error')
        window.grid_propagate(True)
        window.geometry('200x100')
        tk.Label(window, text="").grid(column=0, row=0)
        tk.Label(window, text=message).grid(column=1, row=1)
        tk.Label(window, text="").grid(column=2, row=2)
