import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import json
import math
import os
import collections


# --- Clase de Ayuda para los Tooltips ---
class ToolTip:
    """Crea una ayuda emergente (tooltip) para un widget de tkinter."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.cancel()
        if self.tooltip_window: self.tooltip_window.destroy()

    def schedule(self):
        self.cancel()
        self.id = self.widget.after(500, self.show_tooltip)

    def cancel(self):
        if self.id: self.widget.after_cancel(self.id); self.id = None

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)


# --- Clase Principal del Editor ---
class TilemapEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("Editor de Tilemaps v7.0 - Interactivo")
        master.geometry("1600x900")

        self.tilesets = {}
        self.all_tiles = {}
        self.tk_tiles = {}
        self.tile_hashes = {}
        self.gid_counter = 0

        self.map_properties = {"width": 50, "height": 30, "tile_size": 16}
        self.layers = []
        self.active_layer_index = -1

        self.selected_tile_gid = -1
        self.palette_layout = {}
        self.drag_data = {"gid": -1, "window": None, "label": None, "type": None, "start_pos": None}
        self.selection = {"layer_idx": -1, "x": -1, "y": -1, "rect_id": None, "gid": -1}
        self.file_path = None
        self.current_tool = tk.StringVar(value="paint")

        self.create_widgets()
        self.new_map()

        master.bind("<Delete>", self.delete_selected_from_map)
        master.bind("<BackSpace>", self.delete_selected_from_map)

    def create_widgets(self):
        main_paned = tk.PanedWindow(self.master, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True)

        left_panel = tk.Frame(main_paned, width=350, relief=tk.SUNKEN, bd=2)
        tileset_frame = tk.LabelFrame(left_panel, text="Tilesets Cargados");
        tileset_frame.pack(fill=tk.X, padx=5, pady=5)
        self.tileset_tree = ttk.Treeview(tileset_frame, height=6, selectmode="browse");
        self.tileset_tree.pack(fill=tk.X, padx=5, pady=5)
        self.tileset_tree.bind("<<TreeviewSelect>>", self.on_tileset_selected)

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
        self.palette_canvas.bind("<ButtonPress-1>", self.on_palette_press)
        main_paned.add(left_panel, stretch="never")

        map_frame = tk.Frame(main_paned, relief=tk.SUNKEN, bd=2)
        self.map_canvas = tk.Canvas(map_frame, bg="#555555")
        v_scroll_map = tk.Scrollbar(map_frame, orient=tk.VERTICAL, command=self.map_canvas.yview);
        h_scroll_map = tk.Scrollbar(map_frame, orient=tk.HORIZONTAL, command=self.map_canvas.xview)
        self.map_canvas.configure(yscrollcommand=v_scroll_map.set, xscrollcommand=h_scroll_map.set)
        v_scroll_map.pack(side=tk.RIGHT, fill=tk.Y);
        h_scroll_map.pack(side=tk.BOTTOM, fill=tk.X);
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.map_canvas.bind("<ButtonPress-1>", self.on_map_press);
        self.map_canvas.bind("<B1-Motion>", self.on_map_drag_motion)
        self.map_canvas.bind("<ButtonRelease-1>", self.on_map_release);
        self.map_canvas.bind("<Button-3>", self.on_map_paint)
        main_paned.add(map_frame, stretch="always")

        tools_frame = tk.Frame(main_paned, width=300, relief=tk.GROOVE, bd=2)
        file_tools_frame = tk.LabelFrame(tools_frame, text="Archivo");
        file_tools_frame.pack(fill=tk.X, padx=5, pady=5)
        b_new = tk.Button(file_tools_frame, text="Nuevo Mapa", command=self.new_map_dialog);
        b_new.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_new, "Crea un mapa nuevo y vacío.")
        b_load = tk.Button(file_tools_frame, text="Cargar Mapa (JSON)", command=self.load_json);
        b_load.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_load, "Carga un proyecto .json.")
        b_save = tk.Button(file_tools_frame, text="Guardar Mapa (JSON)", command=self.save_json);
        b_save.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_save, "Guarda el mapa y el tileset optimizado.")

        tool_mode_frame = tk.LabelFrame(tools_frame, text="Herramientas");
        tool_mode_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Radiobutton(tool_mode_frame, text="Pintar", variable=self.current_tool, value="paint",
                       command=self.clear_selection).pack(side=tk.LEFT, expand=True)
        tk.Radiobutton(tool_mode_frame, text="Seleccionar", variable=self.current_tool, value="select").pack(
            side=tk.LEFT, expand=True)

        map_tools_frame = tk.LabelFrame(tools_frame, text="Propiedades del Mapa");
        map_tools_frame.pack(fill=tk.X, padx=5, pady=5)
        b_resize = tk.Button(map_tools_frame, text="Redimensionar Mapa", command=self.resize_map_dialog)
        b_resize.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_resize, "Cambia el tamaño del mapa en tiles.")

        tileset_tools_frame = tk.LabelFrame(tools_frame, text="Gestión de Tilesets");
        tileset_tools_frame.pack(fill=tk.X, padx=5, pady=5)
        b_add_tileset = tk.Button(tileset_tools_frame, text="Añadir Tileset (Grid)", command=self.add_tileset);
        b_add_tileset.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_add_tileset, "Añade tiles desde una imagen en cuadrícula.")
        b_tile_image = tk.Button(tileset_tools_frame, text="Añadir Imagen de Capa", command=self.add_image_layer)
        b_tile_image.pack(fill=tk.X, padx=5, pady=2);
        ToolTip(b_tile_image, "Añade una imagen completa como una nueva capa.\nTambién añade sus tiles a la paleta.")

        layer_frame = tk.LabelFrame(tools_frame, text="Capas");
        layer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layer_listbox = tk.Listbox(layer_frame, exportselection=False);
        self.layer_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layer_listbox.bind("<<ListboxSelect>>", self.on_layer_select);
        self.layer_listbox.bind("<Double-1>", self.toggle_layer_visibility)
        layer_buttons = tk.Frame(layer_frame);
        layer_buttons.pack(fill=tk.X, pady=2)
        b_add_layer = tk.Button(layer_buttons, text="+", command=self.add_layer);
        b_add_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_add_layer, "Añadir nueva capa.")
        b_rem_layer = tk.Button(layer_buttons, text="-", command=self.remove_layer);
        b_rem_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_rem_layer, "Eliminar capa seleccionada.")
        b_up_layer = tk.Button(layer_buttons, text="▲", command=lambda: self.move_layer(-1));
        b_up_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_up_layer, "Subir capa.")
        b_down_layer = tk.Button(layer_buttons, text="▼", command=lambda: self.move_layer(1));
        b_down_layer.pack(side=tk.LEFT, padx=2);
        ToolTip(b_down_layer, "Bajar capa.")

        main_paned.add(tools_frame, stretch="never")

    def new_map(self):
        if hasattr(self, 'layers') and self.layers and not messagebox.askyesno("Confirmar",
                                                                               "Esto borrará el mapa y los tilesets actuales. ¿Continuar?"):
            return
        self.clear_tilesets()
        self.map_properties = {"width": 50, "height": 30, "tile_size": 16}
        self.layers = []
        self.add_layer("Fondo")
        self.add_layer("Objetos")
        self.update_layer_listbox(select_index=0)
        self.redraw_map()

    def new_map_dialog(self):
        if hasattr(self, 'layers') and self.layers and not messagebox.askyesno("Confirmar",
                                                                               "Esto borrará el mapa y los tilesets actuales. ¿Continuar?"):
            return
        dims = simpledialog.askstring("Nuevo Mapa", "Dimensiones (ancho,alto) y tamaño de tile (ej: 50,30,16):",
                                      initialvalue=f"{self.map_properties['width']},{self.map_properties['height']},{self.map_properties['tile_size']}")
        if not dims: return
        try:
            w, h, ts = map(int, dims.split(','))
            self.map_properties = {"width": w, "height": h, "tile_size": ts}
            self.clear_tilesets()
            self.layers = []
            self.add_layer("Fondo")
            self.update_layer_listbox(select_index=0)
            self.redraw_map()
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Formato inválido. Usa 'ancho,alto,tamaño_tile'.")

    def resize_map_dialog(self):
        dims = simpledialog.askstring("Redimensionar Mapa", "Nuevo tamaño (ancho,alto):",
                                      initialvalue=f"{self.map_properties['width']},{self.map_properties['height']}")
        if not dims: return
        try:
            new_width, new_height = map(int, dims.split(','))

            for layer in self.layers:
                if layer['type'] == 'tilelayer':
                    old_data = layer['data']
                    old_h, old_w = len(old_data), len(old_data[0]) if old_data else 0
                    new_data = [[-1 for _ in range(new_width)] for _ in range(new_height)]
                    for y in range(min(old_h, new_height)):
                        for x in range(min(old_w, new_width)):
                            new_data[y][x] = old_data[y][x]
                    layer['data'] = new_data

            self.map_properties['width'], self.map_properties['height'] = new_width, new_height
            self.redraw_map()
        except ValueError:
            messagebox.showerror("Error", "Formato inválido. Usa 'ancho,alto'.")

    def add_layer(self, name=None):
        if name is None: name = simpledialog.askstring("Nueva Capa", "Nombre de la capa:")
        if not name or any(l['name'] == name for l in self.layers):
            if name: messagebox.showerror("Error", "El nombre de la capa ya existe."); return

        layer_type = "tilelayer" if "objeto" not in name.lower() and "imagen" not in name.lower() else "objectgroup"
        new_layer = {"name": name, "type": layer_type, "visible": True}
        if layer_type == "tilelayer":
            new_layer["data"] = [[-1 for _ in range(self.map_properties['width'])] for _ in
                                 range(self.map_properties['height'])]
        else:
            new_layer["data"] = []
        self.layers.append(new_layer)
        self.update_layer_listbox(select_index=len(self.layers) - 1)

    def remove_layer(self):
        selection = self.layer_listbox.curselection()
        if not selection: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar la capa '{self.layers[selection[0]]['name']}'?"):
            del self.layers[selection[0]]
            self.update_layer_listbox()
            self.redraw_map()

    def move_layer(self, direction):
        selection = self.layer_listbox.curselection()
        if not selection: return
        idx = selection[0]
        new_idx = idx + direction
        if 0 <= new_idx < len(self.layers):
            self.layers.insert(new_idx, self.layers.pop(idx))
            self.update_layer_listbox(select_index=new_idx)
            self.redraw_map()

    def update_layer_listbox(self, select_index=None):
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.layers):
            visibility = "" if layer.get('visible', True) else "(Oculta)"
            layer_type_char = "T"
            if layer.get('type') == 'objectgroup': layer_type_char = "O"
            if layer.get('type') == 'imagelayer': layer_type_char = "I"
            self.layer_listbox.insert(tk.END, f"[{i}] {layer['name']} ({layer_type_char}) {visibility}")
        if select_index is not None and select_index < self.layer_listbox.size():
            self.layer_listbox.selection_clear(0, tk.END)
            self.layer_listbox.selection_set(select_index)
            self.active_layer_index = select_index

    def on_layer_select(self, event):
        selection = self.layer_listbox.curselection()
        if selection: self.active_layer_index = selection[0]

    def add_tileset(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not file_paths: return

        first_img = Image.open(file_paths[0])
        suggested_size = math.gcd(first_img.width, first_img.height)
        if suggested_size <= 4: suggested_size = self.map_properties.get('tile_size', 16)

        size_str = simpledialog.askstring("Tamaño del Tile",
                                          f"Tamaño de tile para esta cuadrícula (sugerido: {suggested_size}):",
                                          initialvalue=str(suggested_size))
        if not size_str: return
        try:
            tile_size = int(size_str)
        except ValueError:
            messagebox.showerror("Error", "Tamaño inválido."); return

        for path in file_paths: self._process_image(path, tile_size)
        self.update_tileset_tree()

    def add_image_layer(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.webp")])
        if not path: return

        layer_name = os.path.basename(path)
        new_layer = {"name": f"Imagen-{layer_name}", "type": "imagelayer", "visible": True, "image_path": path,
                     "offset": [0, 0]}
        self.layers.append(new_layer)
        self.update_layer_listbox(select_index=len(self.layers) - 1)
        self.redraw_map()

        if messagebox.askyesno("Paleta",
                               "La imagen se ha añadido como capa.\n¿Quieres también extraer sus tiles a la paleta?"):
            size_str = simpledialog.askstring("Tilear para Paleta", "Tamaño de tile para extraer (ej: 16):",
                                              initialvalue=str(self.map_properties['tile_size']))
            if size_str:
                try:
                    tile_size = int(size_str)
                    self._process_image(path, tile_size)
                    self.update_tileset_tree()
                except ValueError:
                    messagebox.showerror("Error", "Tamaño inválido.")

    def clear_tilesets(self):
        if messagebox.askyesno("Confirmar", "¿Limpiar todos los tilesets cargados?"):
            self.tilesets.clear();
            self.tile_hashes.clear();
            self.tk_tiles.clear();
            self.all_tiles.clear()
            self.gid_counter = 0;
            self.selected_tile_gid = -1
            self.update_tileset_tree();
            self.redraw_palette(None)

    def _process_image(self, path, tile_size, return_stamp=False):
        try:
            img = Image.open(path).convert("RGBA")
            tileset_name = os.path.basename(path)
            if tileset_name not in self.tilesets:
                self.tilesets[tileset_name] = {"tiles": {}, "tile_size": tile_size}

            stamp_data = []
            if return_stamp:
                stamp_rows = math.ceil(img.height / tile_size)
                stamp_cols = math.ceil(img.width / tile_size)
                stamp_data = [[-1 for _ in range(stamp_cols)] for _ in range(stamp_rows)]

            for y_idx, y in enumerate(range(0, img.height, tile_size)):
                for x_idx, x in enumerate(range(0, img.width, tile_size)):
                    tile = img.crop((x, y, x + tile_size, y + tile_size))
                    if tile.getbbox() is None: continue

                    tile_hash = hash(tile.tobytes())
                    existing_gid = next((gid for gid, h in self.tile_hashes.items() if h == tile_hash), None)

                    if existing_gid is None:
                        self.gid_counter += 1;
                        gid = self.gid_counter
                        self.tile_hashes[gid] = tile_hash
                        self.all_tiles[gid] = tile
                    else:
                        gid = existing_gid

                    self.tilesets[tileset_name]["tiles"][gid] = tile

                    if return_stamp:
                        if y_idx < len(stamp_data) and x_idx < len(stamp_data[0]):
                            stamp_data[y_idx][x_idx] = gid

            if return_stamp: return stamp_data, tileset_name
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen {path}:\n{e}")
            if return_stamp: return None, None

    def update_tileset_tree(self):
        self.tileset_tree.delete(*self.tileset_tree.get_children())
        for name in sorted(self.tilesets.keys()):
            self.tileset_tree.insert("", "end", text=name, iid=name)

    def on_tileset_selected(self, event=None, select_name=None):
        if select_name:
            if select_name in self.tileset_tree.get_children(""):
                self.tileset_tree.selection_set(select_name)
            else:
                return
            tileset_name = select_name
        else:
            selection = self.tileset_tree.selection()
            if not selection: return
            tileset_name = selection[0]
        self.redraw_palette(tileset_name)

    def redraw_palette(self, tileset_name):
        self.palette_canvas.delete("all");
        self.tk_tiles.clear();
        self.palette_layout.clear()
        if not tileset_name or tileset_name not in self.tilesets: return

        tileset = self.tilesets[tileset_name]
        display_tile_size = min(tileset['tile_size'], 64)
        width = self.palette_canvas.winfo_width()
        cols = max(1, width // display_tile_size)

        sorted_gids = sorted(tileset["tiles"].keys())
        for i, gid in enumerate(sorted_gids):
            row, col = divmod(i, cols)
            x, y = col * display_tile_size, row * display_tile_size
            rect = (x, y, x + display_tile_size, y + display_tile_size)
            self.palette_layout[gid] = rect

            tile_img = tileset["tiles"][gid]
            tk_img = ImageTk.PhotoImage(tile_img.resize((display_tile_size, display_tile_size)))
            self.tk_tiles[gid] = tk_img
            self.palette_canvas.create_image(x, y, anchor='nw', image=tk_img)

        num_rows = math.ceil(len(sorted_gids) / cols) if cols > 0 else 0
        self.palette_canvas.config(scrollregion=(0, 0, cols * display_tile_size, num_rows * display_tile_size))

    def on_palette_press(self, event):
        canvas_y, canvas_x = self.palette_canvas.canvasy(event.y), self.palette_canvas.canvasx(event.x)
        for gid, rect in self.palette_layout.items():
            if rect[0] <= canvas_x < rect[2] and rect[1] <= canvas_y < rect[3]:
                self.selected_tile_gid = gid;
                self.drag_data["gid"] = gid
                self.drag_data["type"] = 'paint_tile'
                self.create_drag_window(event, self.all_tiles[gid]);
                break

    def create_drag_window(self, event, pil_image):
        if self.drag_data["gid"] != -1:
            self.drag_data["window"] = tk.Toplevel(self.master)
            self.drag_data["window"].overrideredirect(True)
            self.drag_data["window"].attributes("-topmost", True)
            map_tile_size = self.map_properties['tile_size']
            tk_img = ImageTk.PhotoImage(pil_image.resize((map_tile_size, map_tile_size)))
            self.drag_data["label"] = tk.Label(self.drag_data["window"], image=tk_img, relief="raised", bg="black")
            self.drag_data["label"].image = tk_img;
            self.drag_data["label"].pack()
            self.on_map_drag(event)

    def on_map_drag(self, event):
        if self.drag_data["window"]: self.drag_data["window"].geometry(f"+{event.x_root + 15}+{event.y_root + 10}")

    def on_map_press(self, event):
        self.clear_selection()
        if self.current_tool.get() == "paint":
            self.on_map_paint(event)
        elif self.current_tool.get() == "select":
            self.on_map_select_press(event)

    def on_map_drag_motion(self, event):
        if self.current_tool.get() == "paint":
            self.on_map_paint(event)
        elif self.current_tool.get() == "select":
            self.on_map_drag_select(event)

    def on_map_select_press(self, event):
        if self.active_layer_index == -1: return
        map_x, map_y = self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y)
        grid_x, grid_y = int(map_x // self.map_properties['tile_size']), int(map_y // self.map_properties['tile_size'])

        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            if not layer.get('visible', True) or layer['type'] != 'tilelayer': continue
            if 0 <= grid_x < self.map_properties['width'] and 0 <= grid_y < self.map_properties['height']:
                gid = layer['data'][grid_y][grid_x]
                if gid != -1:
                    self.selection = {"layer_idx": i, "x": grid_x, "y": grid_y, "gid": gid}
                    ts = self.map_properties['tile_size']
                    rect_id = self.map_canvas.create_rectangle(grid_x * ts, grid_y * ts, (grid_x + 1) * ts,
                                                               (grid_y + 1) * ts, outline="yellow", width=2,
                                                               tags="selection_rect")
                    self.selection['rect_id'] = rect_id
                    self.drag_data['type'] = 'move_tile'
                    self.drag_data['start_pos'] = (grid_x, grid_y)
                    self.layer_listbox.selection_set(i);
                    self.active_layer_index = i
                    return

    def on_map_drag_select(self, event):
        if self.drag_data['type'] == 'move_tile' and self.selection['gid'] != -1:
            if not self.drag_data["window"]:
                self.create_drag_window(event, self.all_tiles[self.selection['gid']])
            self.on_map_drag(event)

    def on_map_release(self, event):
        if self.drag_data["window"]: self.drag_data["window"].destroy()

        if self.drag_data['type'] == 'paint_tile':
            map_x, map_y = self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y)
            grid_x, grid_y = int(map_x // self.map_properties['tile_size']), int(
                map_y // self.map_properties['tile_size'])
            self.paint_tile(grid_x, grid_y, self.drag_data["gid"])
        elif self.drag_data['type'] == 'move_tile':
            original_layer_idx = self.selection['layer_idx']
            original_x, original_y = self.selection['x'], self.selection['y']
            self.layers[original_layer_idx]['data'][original_y][original_x] = -1
            self.redraw_map_tile(original_layer_idx, original_x, original_y)

            map_x, map_y = self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y)
            grid_x, grid_y = int(map_x // self.map_properties['tile_size']), int(
                map_y // self.map_properties['tile_size'])

            if self.layers[original_layer_idx]['type'] == 'tilelayer':
                self.paint_tile(grid_x, grid_y, self.selection['gid'], layer_idx_override=original_layer_idx)

        self.clear_selection()
        self.drag_data = {"gid": -1, "window": None, "label": None, "type": None, "start_pos": None}

    def on_map_paint(self, event):
        if self.drag_data["gid"] != -1 or self.current_tool.get() != "paint": return
        gid_to_paint = self.selected_tile_gid if event.num == 1 else -1
        map_x, map_y = self.map_canvas.canvasx(event.x), self.map_canvas.canvasy(event.y)
        grid_x, grid_y = int(map_x // self.map_properties['tile_size']), int(map_y // self.map_properties['tile_size'])
        self.paint_tile(grid_x, grid_y, gid_to_paint)

    def paint_tile(self, grid_x, grid_y, gid, layer_idx_override=None):
        target_layer_idx = layer_idx_override if layer_idx_override is not None else self.active_layer_index
        if target_layer_idx == -1 or not (
                0 <= grid_x < self.map_properties['width'] and 0 <= grid_y < self.map_properties['height']): return

        active_layer = self.layers[target_layer_idx]
        if active_layer['type'] != 'tilelayer': return
        if active_layer['data'][grid_y][grid_x] != gid:
            active_layer['data'][grid_y][grid_x] = gid
            self.redraw_map_tile(target_layer_idx, grid_x, grid_y)

    def redraw_map(self):
        self.map_canvas.delete("all");
        self.clear_selection()
        ts = self.map_properties['tile_size']
        self.map_canvas.config(
            scrollregion=(0, 0, self.map_properties['width'] * ts, self.map_properties['height'] * ts))
        for layer_idx, layer in enumerate(self.layers):
            if not layer.get('visible', True): continue
            if layer.get('type') == 'tilelayer':
                for y, row in enumerate(layer.get('data', [])):
                    for x, gid in enumerate(row):
                        self.redraw_map_tile(layer_idx, x, y)
            elif layer.get('type') == 'imagelayer':
                self.redraw_image_layer(layer)

    def redraw_image_layer(self, layer):
        path = layer.get('image_path')
        if not path: return
        if path not in self.tk_tiles:
            try:
                img = Image.open(path).convert("RGBA")
                self.tk_tiles[path] = ImageTk.PhotoImage(img)
            except Exception as e:
                return
        offset = layer.get('offset', [0, 0])
        self.map_canvas.create_image(offset[0], offset[1], anchor='nw', image=self.tk_tiles[path])

    def redraw_map_tile(self, layer_index, grid_x, grid_y):
        if not (0 <= layer_index < len(self.layers)): return
        layer = self.layers[layer_index]
        if not layer.get('data') or not (0 <= grid_y < len(layer['data'])) or not (
                0 <= grid_x < len(layer['data'][0])): return

        gid = layer['data'][grid_y][grid_x]
        ts = self.map_properties['tile_size']
        x, y = grid_x * ts, grid_y * ts
        tag = f"L{layer_index}_{grid_x}_{grid_y}"
        self.map_canvas.delete(tag)

        if gid != -1:
            if gid not in self.tk_tiles:
                if gid in self.all_tiles: self.tk_tiles[gid] = ImageTk.PhotoImage(self.all_tiles[gid].resize((ts, ts)))
            if gid in self.tk_tiles:
                self.map_canvas.create_image(x, y, anchor='nw', image=self.tk_tiles[gid], tags=tag)

    def save_json(self):
        if not self.layers:
            messagebox.showwarning("Nada que guardar", "El mapa está vacío.");
            return
        if self.file_path is None:
            self.file_path = filedialog.asksaveasfilename(initialfile="nuevo_mapa.json", defaultextension=".json",
                                                          filetypes=[("JSON files", "*.json")])
        if not self.file_path: return

        sorted_tiles = sorted(self.all_tiles.items())
        gid_map = {old_gid: new_gid for new_gid, (old_gid, _) in enumerate(sorted_tiles)}

        ts = self.map_properties['tile_size'];
        cols = 16
        rows = math.ceil(len(sorted_tiles) / cols) if sorted_tiles else 1
        final_tileset_img = Image.new('RGBA', (cols * ts, rows * ts))

        for new_gid, (old_gid, tile_img) in enumerate(sorted_tiles):
            row, col = divmod(new_gid, cols)
            final_tileset_img.paste(tile_img.resize((ts, ts)), (col * ts, row * ts))

        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        tileset_filename = f"{base_name}_tileset.png"
        tileset_save_path = os.path.join(os.path.dirname(self.file_path), tileset_filename)
        final_tileset_img.save(tileset_save_path)

        layers_to_save = []
        for layer in self.layers:
            new_layer = layer.copy()
            if layer['type'] == 'tilelayer':
                new_layer['data'] = [[gid_map.get(gid, -1) for gid in row] for row in layer['data']]
            elif layer['type'] == 'imagelayer':
                json_dir = os.path.dirname(self.file_path)
                try:
                    new_layer['image_path'] = os.path.relpath(layer['image_path'], json_dir).replace('\\', '/')
                except ValueError:
                    new_layer['image_path'] = layer['image_path']
            layers_to_save.append(new_layer)

        output_data = {"properties": self.map_properties, "tileset_path": tileset_filename, "layers": layers_to_save}
        with open(self.file_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        messagebox.showinfo("Guardado", f"Mapa y Tileset guardados.")

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path: return
        self.file_path = file_path

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.clear_tilesets()
            self.map_properties = data['properties']

            json_dir = os.path.dirname(file_path)
            tileset_path = os.path.join(json_dir, data['tileset_path'])
            if not os.path.exists(tileset_path): raise FileNotFoundError(
                f"No se encontró el tileset: {data['tileset_path']}")

            self._process_image(tileset_path, self.map_properties['tile_size'])

            loaded_layers = data['layers']
            gid_map_load = {i: gid for i, gid in enumerate(sorted(self.all_tiles.keys()))}

            for layer in loaded_layers:
                if layer['type'] == 'tilelayer':
                    layer['data'] = [[gid_map_load.get(gid, -1) for gid in row] for row in layer['data']]
                elif layer['type'] == 'imagelayer':
                    img_path = layer['image_path']
                    if not os.path.isabs(img_path):
                        layer['image_path'] = os.path.normpath(os.path.join(json_dir, img_path))

            self.layers = loaded_layers
            self.update_tileset_tree()
            self.update_layer_listbox(0)
            self.redraw_map()

            messagebox.showinfo("Cargado", f"Mapa '{os.path.basename(file_path)}' cargado.")
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo de mapa:\n{e}")

    def delete_selected_from_map(self, event=None):
        if self.selection['layer_idx'] != -1 and self.selection['gid'] != -1:
            sel = self.selection
            self.paint_tile(sel['x'], sel['y'], -1, layer_idx_override=sel['layer_idx'])
            self.clear_selection()
            return "break"

    def clear_selection(self):
        self.map_canvas.delete("selection_rect")
        self.selection = {"layer_idx": -1, "x": -1, "y": -1, "rect_id": None, "gid": -1}

    def toggle_layer_visibility(self, event):
        selection = self.layer_listbox.curselection()
        if not selection: return
        idx = selection[0]
        self.layers[idx]['visible'] = not self.layers[idx]['visible']
        self.update_layer_listbox(select_index=idx)
        self.redraw_map()

    def place_stamp(self, stamp_data, grid_x, grid_y):
        active_layer = self.layers[self.active_layer_index]
        if active_layer['type'] != 'tilelayer':
            messagebox.showwarning("Capa Incorrecta", "Solo se puede colocar en capas de tiles.")
            return

        for y, row in enumerate(stamp_data):
            for x, gid in enumerate(row):
                if gid != -1:
                    map_x, map_y = grid_x + x, grid_y + y
                    if 0 <= map_x < self.map_properties['width'] and 0 <= map_y < self.map_properties['height']:
                        active_layer['data'][map_y][map_x] = gid


if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Error", "La librería 'Pillow' es necesaria.\nInstálala con: pip install Pillow")
        exit()

    root = tk.Tk()
    app = TilemapEditorApp(root)
    root.mainloop()