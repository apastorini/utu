# editor.py
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import json
import math
import os

from editores.tile_editor.v1.tool_tip import ToolTip
from map_model import MapModel



class TilemapEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("Editor de Mapas por Capas v10.0")
        master.geometry("1600x900")

        self.model = MapModel()

        self.tk_tiles = {};
        self.tk_layer_images = {}
        self.palette_layout = {};
        self.active_layer_index = -1
        self.selected_tile_gid = -1
        self.current_tool = tk.StringVar(value="paint")

        self.create_widgets()
        self.update_layer_listbox(0)
        self.redraw_map()

    def create_widgets(self):
        main_paned = tk.PanedWindow(self.master, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True)

        left_panel = tk.Frame(main_paned, width=350, relief=tk.SUNKEN, bd=2)
        b_add_spritesheet = tk.Button(left_panel, text="Añadir Spritesheet a Paleta",
                                      command=self.add_spritesheet_to_palette)
        b_add_spritesheet.pack(fill=tk.X, padx=5, pady=5);
        ToolTip(b_add_spritesheet, "Corta una imagen en tiles y añade los únicos a la paleta.")
        palette_frame = tk.LabelFrame(left_panel, text="Paleta de Tiles");
        palette_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        pal_canvas_frame = tk.Frame(palette_frame);
        pal_canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.palette_canvas = tk.Canvas(pal_canvas_frame, bg="#333333")
        v_scroll_pal = tk.Scrollbar(pal_canvas_frame, orient=tk.VERTICAL, command=self.palette_canvas.yview);
        h_scroll_pal = tk.Scrollbar(pal_canvas_frame, orient=tk.HORIZONTAL, command=self.palette_canvas.xview)
        self.palette_canvas.configure(yscrollcommand=v_scroll_pal.set, xscrollcommand=h_scroll_pal.set)
        v_scroll_pal.pack(side=tk.RIGHT, fill=tk.Y);
        h_scroll_pal.pack(side=tk.BOTTOM, fill=tk.X);
        self.palette_canvas.pack(fill=tk.BOTH, expand=True)
        self.palette_canvas.bind("<Button-1>", self.on_palette_click)
        main_paned.add(left_panel, stretch="never")

        map_frame = tk.Frame(main_paned, relief=tk.SUNKEN, bd=2)
        self.map_canvas = tk.Canvas(map_frame, bg="#555555")
        v_scroll_map = tk.Scrollbar(map_frame, orient=tk.VERTICAL, command=self.map_canvas.yview);
        h_scroll_map = tk.Scrollbar(map_frame, orient=tk.HORIZONTAL, command=self.map_canvas.xview)
        self.map_canvas.configure(yscrollcommand=v_scroll_map.set, xscrollcommand=h_scroll_map.set)
        v_scroll_map.pack(side=tk.RIGHT, fill=tk.Y);
        h_scroll_map.pack(side=tk.BOTTOM, fill=tk.X);
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.map_canvas.bind("<B1-Motion>", self.on_map_paint);
        self.map_canvas.bind("<Button-1>", self.on_map_paint);
        self.map_canvas.bind("<Button-3>", self.on_map_paint)
        main_paned.add(map_frame, stretch="always")

        tools_frame = tk.Frame(main_paned, width=300, relief=tk.GROOVE, bd=2)
        file_tools_frame = tk.LabelFrame(tools_frame, text="Archivo");
        file_tools_frame.pack(fill=tk.X, padx=5, pady=5)
        b_load = tk.Button(file_tools_frame, text="Cargar Mapa (JSON)", command=self.load_json);
        b_load.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_load, "Carga un proyecto de mapa desde un archivo .json.")
        b_save = tk.Button(file_tools_frame, text="Guardar Mapa (JSON)", command=self.save_json);
        b_save.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_save, "Guarda el mapa actual y el tileset optimizado.")

        tool_mode_frame = tk.LabelFrame(tools_frame, text="Herramientas");
        tool_mode_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Radiobutton(tool_mode_frame, text="Pintar", variable=self.current_tool, value="paint").pack(side=tk.LEFT,
                                                                                                       expand=True)
        tk.Radiobutton(tool_mode_frame, text="Bloqueo", variable=self.current_tool, value="blocking").pack(side=tk.LEFT,
                                                                                                           expand=True)

        layer_frame = tk.LabelFrame(tools_frame, text="Capas");
        layer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layer_listbox = tk.Listbox(layer_frame, exportselection=False);
        self.layer_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layer_listbox.bind("<<ListboxSelect>>", self.on_layer_select)
        self.layer_listbox.bind("<Double-1>", self.on_layer_toggle_visibility)

        layer_buttons = tk.Frame(layer_frame);
        layer_buttons.pack(fill=tk.X, pady=2)
        b_add_tile = tk.Button(layer_buttons, text="+ Tile", command=self.add_tile_layer);
        b_add_tile.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_tile, "Añadir nueva capa de tiles (con rejilla).")
        b_add_img = tk.Button(layer_buttons, text="+ Imagen", command=self.add_image_layer);
        b_add_img.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_img, "Añadir nueva capa de imagen (para fondos).")
        b_add_obj = tk.Button(layer_buttons, text="+ Objeto", command=self.add_object_layer);
        b_add_obj.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_obj, "Añadir nueva capa de objetos (sin rejilla).")

        layer_buttons_2 = tk.Frame(layer_frame);
        layer_buttons_2.pack(fill=tk.X, pady=2)
        b_rem_layer = tk.Button(layer_buttons_2, text="-", command=self.remove_layer);
        b_rem_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_rem_layer, "Eliminar capa seleccionada.")
        b_up_layer = tk.Button(layer_buttons_2, text="▲", command=lambda: self.move_layer(-1));
        b_up_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_up_layer, "Subir capa (dibujar antes).")
        b_down_layer = tk.Button(layer_buttons_2, text="▼", command=lambda: self.move_layer(1));
        b_down_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_down_layer, "Bajar capa (dibujar después).")
        main_paned.add(tools_frame, stretch="never")

    def add_tile_layer(self):
        name = simpledialog.askstring("Nueva Capa de Tiles", "Nombre:", initialvalue="Capa de Tiles")
        if not name: return
        size_str = simpledialog.askstring("Tamaño de Tile", "Tamaño (ej: 16):",
                                          initialvalue=self.model.properties.get('tile_size', 16))
        if not size_str: return
        try:
            self.model.add_layer(name, layer_type='tilelayer', tile_size=int(size_str))
            self.update_layer_listbox(len(self.model.layers) - 1)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_image_layer(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.webp")])
        if not path: return
        name = simpledialog.askstring("Nueva Capa de Imagen", "Nombre:", initialvalue=os.path.basename(path))
        if not name: return
        try:
            self.model.add_layer(name, layer_type='imagelayer', image_path=path)
            img = Image.open(path)
            if len(self.model.layers) == 1 or self.model.properties.get('width_pixels', 0) == 0:
                self.model.properties['width_pixels'] = img.width
                self.model.properties['height_pixels'] = img.height
                for l in self.model.layers:
                    if l['type'] == 'tilelayer':
                        w = img.width // l['tile_size'];
                        h = img.height // l['tile_size']
                        l['data'] = [[{"gid": -1, "blocking": False} for _ in range(w)] for _ in range(h)]
            self.update_layer_listbox(len(self.model.layers) - 1)
            self.redraw_map()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_object_layer(self):
        name = simpledialog.askstring("Nueva Capa de Objetos", "Nombre:", initialvalue="Capa de Objetos")
        if not name: return
        try:
            self.model.add_layer(name, layer_type='objectgroup')
            self.update_layer_listbox(len(self.model.layers) - 1)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_layer_toggle_visibility(self, event):
        selection = self.layer_listbox.curselection()
        if not selection: return
        idx = selection[0]
        self.model.layers[idx]['visible'] = not self.model.layers[idx].get('visible', True)
        self.update_layer_listbox(idx)
        self.redraw_map()

    def on_layer_select(self, event):
        selection = self.layer_listbox.curselection()
        if selection: self.active_layer_index = selection[0]

    def remove_layer(self):
        selection = self.layer_listbox.curselection()
        if not selection: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar la capa seleccionada?"):
            self.model.remove_layer(selection[0])
            self.update_layer_listbox()
            self.redraw_map()

    def move_layer(self, direction):
        selection = self.layer_listbox.curselection()
        if not selection: return
        new_index = self.model.move_layer(selection[0], direction)
        self.update_layer_listbox(new_index)
        self.redraw_map()

    def update_layer_listbox(self, select_index=None):
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.model.layers):
            visibility_char = "👁️" if layer.get('visible', True) else "➖"
            blocking_char = "🧱" if layer.get('blocking', False) else "➡️"
            type_char = layer.get('type', 'T')[0].upper()
            self.layer_listbox.insert(tk.END, f"[{i}] {layer['name']} ({type_char}) {visibility_char} {blocking_char}")
        if select_index is not None and select_index < self.layer_listbox.size():
            self.layer_listbox.selection_clear(0, tk.END)
            self.layer_listbox.selection_set(select_index)
            self.active_layer_index = select_index

    def add_spritesheet_to_palette(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.webp")])
        if not path: return
        ts = self.model.properties.get('tile_size', 16)
        size_str = simpledialog.askstring("Tamaño de Tile", "Tamaño (ej: 16):", initialvalue=str(ts))
        if size_str:
            try:
                new_tiles_count = self.model.process_image_for_palette(path, int(size_str))
                self.redraw_palette()
                messagebox.showinfo("Éxito", f"Se añadieron {new_tiles_count} tiles únicos a la paleta.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar la imagen:\n{e}")

    def on_palette_click(self, event):
        canvas_y, canvas_x = self.palette_canvas.canvasy(event.y), self.palette_canvas.canvasx(event.x)
        for gid, rect in self.palette_layout.items():
            if rect[0] <= canvas_x < rect[2] and rect[1] <= canvas_y < rect[3]:
                self.selected_tile_gid = gid
                self.redraw_palette()
                break

    def on_map_paint(self, event):
        if self.active_layer_index == -1: return
        layer = self.model.layers[self.active_layer_index]
        map_x, map_y = self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y)

        tool = self.current_tool.get()

        if tool == "paint":
            if layer['type'] == 'tilelayer':
                gid_to_paint = self.selected_tile_gid if event.num == 1 else -1
                ts = layer.get('tile_size', self.model.properties.get('tile_size', 16))
                if ts == 0: return
                grid_x, grid_y = int(map_x // ts), int(map_y // ts)
                if self.model.paint_tile(self.active_layer_index, grid_x, grid_y, gid_to_paint):
                    self.redraw_map_tile(self.active_layer_index, grid_x, grid_y)
            elif layer['type'] == 'objectgroup' and event.num == 1 and self.selected_tile_gid != -1:
                self.model.add_object(self.active_layer_index, int(map_x), int(map_y), self.selected_tile_gid)
                self.redraw_map()

        elif tool == "blocking" and layer['type'] == 'tilelayer':
            if event.type == tk.EventType.ButtonPress:
                ts = layer.get('tile_size', self.model.properties.get('tile_size', 16))
                grid_x, grid_y = int(map_x // ts), int(map_y // ts)
                if self.model.toggle_tile_blocking(self.active_layer_index, grid_x, grid_y):
                    self.redraw_map_tile(self.active_layer_index, grid_x, grid_y)

    def redraw_map(self):
        self.map_canvas.delete("all")
        width_px = self.model.properties['width_pixels'];
        height_px = self.model.properties['height_pixels']
        self.map_canvas.config(scrollregion=(0, 0, width_px, height_px))
        self.tk_layer_images.clear()
        for layer_idx, layer in enumerate(self.model.layers):
            if not layer.get('visible', True): continue
            if layer.get('type') == 'imagelayer':
                self.redraw_image_layer(layer)
            elif layer.get('type') == 'tilelayer':
                for y, row in enumerate(layer.get('data', [])):
                    for x, _ in enumerate(row): self.redraw_map_tile(layer_idx, x, y)
            elif layer.get('type') == 'objectgroup':
                self.redraw_object_layer(layer)

    def redraw_image_layer(self, layer):
        path = layer.get('image_path');
        if not path: return
        if path not in self.tk_layer_images:
            try:
                img = Image.open(path).convert("RGBA");
                self.tk_layer_images[path] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"No se pudo cargar imagen de capa {path}: {e}"); return
        offset = layer.get('offset', [0, 0]);
        self.map_canvas.create_image(offset[0], offset[1], anchor='nw', image=self.tk_layer_images[path])

    def redraw_map_tile(self, layer_index, grid_x, grid_y):
        layer = self.model.layers[layer_index];
        tile_info = layer['data'][grid_y][grid_x]
        gid = tile_info['gid'];
        is_blocking = tile_info['blocking']
        ts = layer.get('tile_size', self.model.properties.get('tile_size', 16))
        x, y = grid_x * ts, grid_y * ts
        tag = f"L{layer_index}_{grid_x}_{grid_y}";
        self.map_canvas.delete(tag)
        if gid != -1:
            if gid not in self.tk_tiles:
                if gid in self.model.all_tiles: self.tk_tiles[gid] = ImageTk.PhotoImage(
                    self.model.all_tiles[gid].resize((ts, ts)))
            if gid in self.tk_tiles: self.map_canvas.create_image(x, y, anchor='nw', image=self.tk_tiles[gid], tags=tag)
        if is_blocking:
            self.map_canvas.create_rectangle(x, y, x + ts, y + ts, fill="red", stipple="gray50", outline="", tags=tag)

    def redraw_object_layer(self, layer):
        ts = self.model.properties.get('tile_size', 16)
        for obj in layer.get('data', []):
            gid = obj['gid']
            if gid in self.model.all_tiles:
                if gid not in self.tk_tiles: self.tk_tiles[gid] = ImageTk.PhotoImage(
                    self.model.all_tiles[gid].resize((ts, ts)))
                if gid in self.tk_tiles: self.map_canvas.create_image(obj['x'], obj['y'], anchor='center',
                                                                      image=self.tk_tiles[gid])

    def save_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path: return
        self.model.file_path = file_path
        try:
            output_data, final_tileset_img, tile_size = self.model.get_save_data()
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            tileset_filename = f"{base_name}_tileset.png"
            tileset_save_path = os.path.join(os.path.dirname(file_path), tileset_filename)
            final_tileset_img.save(tileset_save_path)
            output_data["tileset"] = {"path": tileset_filename, "tile_size": tile_size}
            with open(file_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            messagebox.showinfo("Guardado", "Mapa y Tileset guardados.")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar:\n{e}")

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path: return
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.model.load_from_json(data, file_path)
            self.update_layer_listbox(0);
            self.redraw_palette();
            self.redraw_map()
            messagebox.showinfo("Cargado", "Mapa cargado.")
        except Exception as e:
            messagebox.showerror("Error al Cargar", f"No se pudo cargar:\n{e}")

    def redraw_palette(self):
        self.palette_canvas.delete("all");
        self.tk_tiles.clear();
        self.palette_layout.clear()
        if not self.model.all_tiles: return
        display_tile_size = 32
        width = self.palette_canvas.winfo_width()
        cols = max(1, width // display_tile_size)
        sorted_gids = sorted(self.model.all_tiles.keys())
        for i, gid in enumerate(sorted_gids):
            row, col = divmod(i, cols)
            x, y = col * display_tile_size, row * display_tile_size
            rect = (x, y, x + display_tile_size, y + display_tile_size)
            self.palette_layout[gid] = rect
            tile_img = self.model.all_tiles[gid]
            tk_img = ImageTk.PhotoImage(tile_img.resize((display_tile_size, display_tile_size)))
            self.tk_tiles[gid] = tk_img
            self.palette_canvas.create_image(x, y, anchor='nw', image=tk_img)
            if gid == self.selected_tile_gid:
                self.palette_canvas.create_rectangle(rect, outline="red", width=2)
        num_rows = math.ceil(len(sorted_gids) / cols) if cols > 0 else 0
        self.palette_canvas.config(scrollregion=(0, 0, cols * display_tile_size, num_rows * display_tile_size))