# Bloque de ejecución, al final del archivo editor.py
from tkinter import messagebox

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from editores.tile_editor.v1.editor_app import TilemapEditorApp

if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Error de Dependencia",
                             "La librería 'Pillow' es necesaria.\nInstálala con: pip install Pillow")
        exit()

    root = tk.Tk()
    # Pega aquí la clase MapModel completa
    # Pega aquí la clase TilemapEditorApp completa
    app = TilemapEditorApp(root)
    root.mainloop()