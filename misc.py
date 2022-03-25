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

class Style:
    colors = {
        "l_sel": "lightblue2",
        "l_hover": "lightblue1",
        'l_active_hover': 'lightblue3',
        "b_reset": "#fff",
        "b_sel": 'medium turquoise',
        'b_hover': 'turquoise',
        'b_active_hover': 'dark turquoise',
        'fin_type': 'red',
        'save_button': 'green',
        'save_button_hover': 'darkgreen'
    }

    @classmethod
    def color(cls, color_string: str):
        color = cls.colors.get(color_string)
        if color is None:
            color = cls.colors.get('b_reset')
        return color
