# editor_ui.py
import tkinter as tk
from tkinter import ttk

from editores.tile_editor.v1.tool_tip import ToolTip


class EditorUI:
    """Clase dedicada a crear y organizar todos los widgets de la interfaz."""

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        main_paned = tk.PanedWindow(self.master, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True)

        self._create_left_panel(main_paned)
        self._create_center_panel(main_paned)
        self._create_right_panel(main_paned)

    def _create_left_panel(self, parent):
        left_panel = tk.Frame(parent, width=350, relief=tk.SUNKEN, bd=2)
        b_add = tk.Button(left_panel, text="Añadir Spritesheet a Paleta",
                          command=self.controller.add_spritesheet_to_palette)
        b_add.pack(fill=tk.X, padx=5, pady=5);
        ToolTip(b_add, "Corta una imagen en tiles y añade los únicos a la paleta.")

        p_frame = tk.LabelFrame(left_panel, text="Paleta de Tiles");
        p_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        pc_frame = tk.Frame(p_frame);
        pc_frame.pack(fill=tk.BOTH, expand=True)
        self.palette_canvas = tk.Canvas(pc_frame, bg="#333333")
        v_scroll = tk.Scrollbar(pc_frame, o=tk.VERTICAL, command=self.palette_canvas.yview)
        h_scroll = tk.Scrollbar(pc_frame, o=tk.HORIZONTAL, command=self.palette_canvas.xview)
        self.palette_canvas.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y);
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.palette_canvas.pack(fill=tk.BOTH, expand=True)
        self.palette_canvas.bind("<Button-1>", self.controller.on_palette_click)
        parent.add(left_panel, stretch="never")

    def _create_center_panel(self, parent):
        map_frame = tk.Frame(parent, relief=tk.SUNKEN, bd=2)
        self.map_canvas = tk.Canvas(map_frame, bg="#555555")
        v_scroll = tk.Scrollbar(map_frame, o=tk.VERTICAL, command=self.map_canvas.yview)
        h_scroll = tk.Scrollbar(map_frame, o=tk.HORIZONTAL, command=self.map_canvas.xview)
        self.map_canvas.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y);
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.map_canvas.bind("<B1-Motion>", self.controller.on_map_paint)
        self.map_canvas.bind("<Button-1>", self.controller.on_map_paint)
        self.map_canvas.bind("<Button-3>", self.controller.on_map_paint)
        parent.add(map_frame, stretch="always")

    def _create_right_panel(self, parent):
        tools_frame = tk.Frame(parent, width=300, relief=tk.GROOVE, bd=2)
        file_tools = tk.LabelFrame(tools_frame, text="Archivo");
        file_tools.pack(fill=tk.X, padx=5, pady=5)
        b_load = tk.Button(file_tools, text="Cargar Mapa (JSON)", command=self.controller.load_json)
        b_load.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_load, "Carga un proyecto .json.")
        b_save = tk.Button(file_tools, text="Guardar Mapa (JSON)", command=self.controller.save_json)
        b_save.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_save, "Guarda el mapa y el tileset optimizado.")

        layer_frame = tk.LabelFrame(tools_frame, text="Capas");
        layer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layer_listbox = tk.Listbox(layer_frame, exportselection=False)
        self.layer_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layer_listbox.bind("<<ListboxSelect>>", self.controller.on_layer_select)
        self.layer_listbox.bind("<Double-1>", self.controller.on_layer_toggle_visibility)

        buttons1 = tk.Frame(layer_frame);
        buttons1.pack(fill=tk.X, pady=2)
        b_add_t = tk.Button(buttons1, text="+ Tile", command=self.controller.add_tile_layer);
        b_add_t.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_t, "Añadir capa de tiles.")
        b_add_i = tk.Button(buttons1, text="+ Imagen", command=self.controller.add_image_layer);
        b_add_i.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_i, "Añadir capa de imagen.")
        b_add_o = tk.Button(buttons1, text="+ Objeto", command=self.controller.add_object_layer);
        b_add_o.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_o, "Añadir capa de objetos.")

        buttons2 = tk.Frame(layer_frame);
        buttons2.pack(fill=tk.X, pady=2)
        b_rem = tk.Button(buttons2, text="-", command=self.controller.remove_layer);
        b_rem.pack(side=tk.LEFT, padx=2);
        ToolTip(b_rem, "Eliminar capa.")
        b_up = tk.Button(buttons2, text="▲", command=lambda: self.controller.move_layer(-1));
        b_up.pack(side=tk.LEFT, padx=2);
        ToolTip(b_up, "Subir capa.")
        b_down = tk.Button(buttons2, text="▼", command=lambda: self.controller.move_layer(1));
        b_down.pack(side=tk.LEFT, padx=2);
        ToolTip(b_down, "Bajar capa.")
        b_block = tk.Button(buttons2, text="Bloqueante", command=self.controller.toggle_layer_blocking);
        b_block.pack(side=tk.LEFT, padx=2);
        ToolTip(b_block, "Marcar/Desmarcar como bloqueante.")
        parent.add(tools_frame, stretch="never")