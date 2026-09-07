import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import json
import collections
import os


class SpritesheetSelectorApp:
    def __init__(self, master):
        self.master = master
        master.title("Spritesheet Editor v2.2 (con Carga/Guardado)")
        master.geometry("1200x800")

        self.project_data = {
            "project_name": "Nuevo Proyecto",
            "spritesheet_path": None,
            "character_name": "",
            "animations": collections.defaultdict(list)
        }

        self.tk_spritesheet_image = None
        self.spritesheet_image = None
        self.rect_ids = {}
        self.start_x, self.start_y = None, None
        self.current_rect_id = None
        self.drawing_mode = False
        self.fixed_size_mode = False

        self.create_widgets()

    def create_widgets(self):
        main_paned_window = tk.PanedWindow(self.master, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned_window.pack(fill=tk.BOTH, expand=True)

        canvas_frame = tk.Frame(main_paned_window, relief=tk.SUNKEN, bd=2)
        main_paned_window.add(canvas_frame, stretch="always")

        self.canvas = tk.Canvas(canvas_frame, bg="gray", cursor="arrow")

        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press_left)
        self.canvas.bind("<B1-Motion>", self.on_drag_left)
        self.canvas.bind("<ButtonRelease-1>", self.on_release_left)
        self.canvas.bind("<Button-3>", self.on_press_right)

        right_frame = tk.Frame(main_paned_window, width=400, relief=tk.GROOVE, bd=2)
        main_paned_window.add(right_frame, stretch="never")

        top_controls_frame = tk.Frame(right_frame)
        top_controls_frame.pack(fill=tk.X, pady=5, padx=5)

        # --- MEJORA: Añadido el botón "Cargar JSON" ---
        tk.Button(top_controls_frame, text="Cargar JSON", command=self.load_json).pack(side=tk.LEFT, padx=5, fill=tk.X,
                                                                                       expand=True)
        tk.Button(top_controls_frame, text="Cargar Spritesheet", command=self.load_spritesheet_dialog).pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(top_controls_frame, text="Sugerir Sprites", command=self.suggest_sprites).pack(side=tk.LEFT, padx=5,
                                                                                                 fill=tk.X, expand=True)
        tk.Button(top_controls_frame, text="Guardar JSON", command=self.save_json).pack(side=tk.LEFT, padx=5, fill=tk.X,
                                                                                        expand=True)

        project_frame = tk.LabelFrame(right_frame, text="Información del Proyecto")
        project_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(project_frame, text="Nombre del Personaje:").pack(side=tk.LEFT, padx=5)
        self.character_name_entry = tk.Entry(project_frame)
        self.character_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        drawing_frame = tk.LabelFrame(right_frame, text="Modo de Selección")
        drawing_frame.pack(fill=tk.X, padx=5, pady=5)
        self.drawing_mode_btn = tk.Button(drawing_frame, text="Modo Libre", command=self.toggle_drawing_mode,
                                          relief=tk.RAISED)
        self.drawing_mode_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.fixed_size_btn = tk.Button(drawing_frame, text="Modo Fijo", command=self.toggle_fixed_size_mode,
                                        relief=tk.RAISED)
        self.fixed_size_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.size_entry_frame = tk.Frame(drawing_frame)
        self.size_entry_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(self.size_entry_frame, text="W:").pack(side=tk.LEFT)
        self.width_entry = tk.Entry(self.size_entry_frame, width=4)
        self.width_entry.pack(side=tk.LEFT)
        tk.Label(self.size_entry_frame, text="H:").pack(side=tk.LEFT)
        self.height_entry = tk.Entry(self.size_entry_frame, width=4)
        self.height_entry.pack(side=tk.LEFT)

        sprite_panel_frame = tk.LabelFrame(right_frame, text="Sprites Guardados")
        sprite_panel_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        list_frame = tk.Frame(sprite_panel_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        self.sprite_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.sprite_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sprite_listbox.bind('<<ListboxSelect>>', self.on_sprite_select)
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.sprite_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sprite_listbox.config(yscrollcommand=scrollbar.set)

        panel_buttons_frame = tk.Frame(right_frame)
        panel_buttons_frame.pack(fill=tk.X, pady=5, padx=5)
        tk.Button(panel_buttons_frame, text="Eliminar", command=self.delete_selected_sprite).pack(side=tk.LEFT, padx=5,
                                                                                                  fill=tk.X,
                                                                                                  expand=True)
        tk.Button(panel_buttons_frame, text="Modificar", command=self.edit_selected_sprite).pack(side=tk.LEFT, padx=5,
                                                                                                 fill=tk.X, expand=True)

        anim_frame = tk.LabelFrame(right_frame, text="Gestión de Animaciones")
        anim_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(anim_frame, text="Agrupar en:").pack(side=tk.LEFT, padx=5)
        self.anim_name_entry = tk.Entry(anim_frame)
        self.anim_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(anim_frame, text="Agrupar", command=self.group_sprites_to_animation).pack(side=tk.LEFT, padx=5,
                                                                                            pady=2)

    def set_cursor(self, cursor_type):
        self.canvas.config(cursor=cursor_type)
        self.drawing_mode = cursor_type == "cross"
        self.fixed_size_mode = cursor_type == "tcross"
        self.drawing_mode_btn.config(relief=tk.SUNKEN if self.drawing_mode else tk.RAISED)
        self.fixed_size_btn.config(relief=tk.SUNKEN if self.fixed_size_mode else tk.RAISED)
        if self.current_rect_id: self.canvas.delete(self.current_rect_id); self.current_rect_id = None

    def toggle_drawing_mode(self):
        self.set_cursor("cross" if not self.drawing_mode else "arrow")

    def toggle_fixed_size_mode(self):
        self.set_cursor("tcross" if not self.fixed_size_mode else "arrow")

    def _display_spritesheet(self, file_path):
        """Función interna para cargar y mostrar una imagen en el canvas."""
        try:
            self.spritesheet_image = Image.open(file_path)
            self.tk_spritesheet_image = ImageTk.PhotoImage(self.spritesheet_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_spritesheet_image)
            self.canvas.config(scrollregion=(0, 0, self.spritesheet_image.width, self.spritesheet_image.height))
            self.project_data['spritesheet_path'] = file_path
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
            return False

    def load_spritesheet_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not file_path: return

        self.project_data['animations'] = collections.defaultdict(list)
        self.character_name_entry.delete(0, tk.END)
        self.update_sprite_listbox()
        self.rect_ids.clear()

        self._display_spritesheet(file_path)

    # --- MEJORA: Nueva función para cargar un proyecto JSON ---
    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path: return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. Limpiar estado actual
            self.rect_ids.clear()
            self.project_data = {
                "project_name": data.get("project_name", "Sin Título"),
                "spritesheet_path": data.get("spritesheet_path"),
                "character_name": data.get("character_name", ""),
                "animations": collections.defaultdict(list, {k: v for k, v in data.get("animations", {}).items()})
            }

            # 2. Cargar la imagen del spritesheet asociada
            json_dir = os.path.dirname(file_path)
            spritesheet_path = os.path.join(json_dir, self.project_data['spritesheet_path'])
            if not os.path.exists(spritesheet_path):
                raise FileNotFoundError(f"No se encontró el archivo de imagen: {self.project_data['spritesheet_path']}")

            if not self._display_spritesheet(spritesheet_path):
                return

            # 3. Actualizar la UI con los datos cargados
            self.character_name_entry.delete(0, tk.END)
            self.character_name_entry.insert(0, self.project_data['character_name'])
            self.update_sprite_listbox()
            self.redraw_sprites()

            messagebox.showinfo("Éxito", f"Proyecto '{self.project_data['project_name']}' cargado correctamente.")

        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo JSON:\n{e}")

    def on_press_left(self, event):
        if not self.spritesheet_image: return
        canvas_x, canvas_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if not self.drawing_mode and not self.fixed_size_mode:
            clicked_items = self.canvas.find_closest(canvas_x, canvas_y)
            if clicked_items and self.canvas.type(clicked_items[0]) == 'rectangle':
                for sprite_name, rect_id in self.rect_ids.items():
                    if rect_id == clicked_items[0]:
                        self.select_sprite_in_listbox(sprite_name);
                        self.on_sprite_select(None);
                        return
        self.start_x, self.start_y = canvas_x, canvas_y
        if self.current_rect_id: self.canvas.delete(self.current_rect_id)
        if self.drawing_mode or self.fixed_size_mode:
            self.current_rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                                outline="red", width=2)

    def on_drag_left(self, event):
        if not self.current_rect_id: return
        canvas_x, canvas_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.drawing_mode:
            self.canvas.coords(self.current_rect_id, self.start_x, self.start_y, canvas_x, canvas_y)
        elif self.fixed_size_mode:
            try:
                width, height = int(self.width_entry.get()), int(self.height_entry.get())
                self.canvas.coords(self.current_rect_id, self.start_x, self.start_y, self.start_x + width,
                                   self.start_y + height)
            except (ValueError, tk.TclError):
                pass

    def on_release_left(self, event):
        if not self.current_rect_id: return
        coords = self.canvas.coords(self.current_rect_id)
        if len(coords) < 4: self.canvas.delete(self.current_rect_id); self.current_rect_id = None; return
        x1, y1, x2, y2 = coords
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        if (x2 - x1) > 0 and (y2 - y1) > 0:
            sprite_data = {"x": int(x1), "y": int(y1), "width": int(x2 - x1), "height": int(y2 - y1),
                           "name": f"sprite_{len(self.get_all_sprites()) + 1}", "description": "",
                           "animation": "default"}
            self.add_sprite_to_list(sprite_data, self.current_rect_id)
        else:
            self.canvas.delete(self.current_rect_id)
        self.current_rect_id = None

    def get_all_sprites(self):
        return [sprite for anim_list in self.project_data['animations'].values() for sprite in anim_list]

    def on_press_right(self, event):
        canvas_x, canvas_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        clicked_items = self.canvas.find_closest(canvas_x, canvas_y)
        if clicked_items and self.canvas.type(clicked_items[0]) == 'rectangle':
            item_id = clicked_items[0]
            for sprite_name, rect_id in self.rect_ids.items():
                if rect_id == item_id:
                    if messagebox.askyesno("Confirmar", f"¿Eliminar el sprite '{sprite_name}'?"):
                        self.delete_sprite(sprite_name);
                        self.update_sprite_listbox();
                        self.redraw_sprites()
                    return

    def on_sprite_select(self, event):
        self.redraw_sprites(highlight_selected=False)
        selected_names = [self.sprite_listbox.get(i) for i in self.sprite_listbox.curselection()]
        for name in selected_names:
            if name.strip().startswith("---"): continue
            sprite_name = name.strip()
            rect_id = self.rect_ids.get(sprite_name)
            if rect_id: self.canvas.itemconfig(rect_id, outline="blue", width=2)

    def select_sprite_in_listbox(self, sprite_name_to_select):
        self.sprite_listbox.selection_clear(0, tk.END)
        for i, item_name in enumerate(self.sprite_listbox.get(0, tk.END)):
            if item_name.strip() == sprite_name_to_select:
                self.sprite_listbox.selection_set(i);
                self.sprite_listbox.see(i);
                break

    def add_sprite_to_list(self, sprite_data, rect_id):
        anim_name = sprite_data.get('animation', 'default')
        self.project_data['animations'][anim_name].append(sprite_data)
        self.rect_ids[sprite_data['name']] = rect_id
        self.update_sprite_listbox()

    def delete_selected_sprite(self):
        selected_names = [self.sprite_listbox.get(i).strip() for i in self.sprite_listbox.curselection() if
                          not self.sprite_listbox.get(i).strip().startswith("---")]
        if not selected_names or not messagebox.askyesno("Confirmar",
                                                         f"¿Eliminar {len(selected_names)} sprite(s) seleccionado(s)?"): return
        for sprite_name in selected_names:
            self.delete_sprite(sprite_name)
        self.update_sprite_listbox();
        self.redraw_sprites()

    def delete_sprite(self, sprite_name):
        for anim_name, anim_list in list(self.project_data['animations'].items()):
            anim_list[:] = [s for s in anim_list if s['name'] != sprite_name]
            if not anim_list: del self.project_data['animations'][anim_name]
        if sprite_name in self.rect_ids:
            self.canvas.delete(self.rect_ids[sprite_name]);
            del self.rect_ids[sprite_name]

    def edit_selected_sprite(self):
        selected_indices = self.sprite_listbox.curselection()
        if not selected_indices: messagebox.showinfo("Error", "Selecciona un sprite para modificar."); return
        sprite_name = self.sprite_listbox.get(selected_indices[0]).strip()
        if sprite_name.startswith("---"): return
        sprite_data = next((s for anim_list in self.project_data['animations'].values() for s in anim_list if
                            s['name'] == sprite_name), None)
        if sprite_data: self.show_edit_dialog(sprite_data)

    def show_edit_dialog(self, sprite_data):
        dialog = tk.Toplevel(self.master);
        dialog.title("Modificar Sprite")
        dialog.transient(self.master);
        dialog.grab_set()
        tk.Label(dialog, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry = tk.Entry(dialog);
        name_entry.grid(row=0, column=1, padx=5, pady=5);
        name_entry.insert(0, sprite_data['name'])
        tk.Label(dialog, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        desc_entry = tk.Entry(dialog);
        desc_entry.grid(row=1, column=1, padx=5, pady=5);
        desc_entry.insert(0, sprite_data['description'])
        tk.Label(dialog, text="Animación:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        anim_entry = tk.Entry(dialog);
        anim_entry.grid(row=2, column=1, padx=5, pady=5);
        anim_entry.insert(0, sprite_data['animation'])

        def save_changes():
            old_name, old_anim = sprite_data['name'], sprite_data['animation']
            new_name, new_desc, new_anim = name_entry.get().strip(), desc_entry.get().strip(), anim_entry.get().strip()
            if not new_name: messagebox.showerror("Error", "El nombre no puede estar vacío.", parent=dialog); return
            if new_name != old_name and new_name in self.rect_ids:
                messagebox.showerror("Error", f"El nombre '{new_name}' ya existe.", parent=dialog);
                return
            sprite_data['name'] = new_name;
            sprite_data['description'] = new_desc
            if new_anim != old_anim:
                self.project_data['animations'][old_anim].remove(sprite_data)
                if not self.project_data['animations'][old_anim]: del self.project_data['animations'][old_anim]
                if new_anim not in self.project_data['animations']: self.project_data['animations'][new_anim] = []
                self.project_data['animations'][new_anim].append(sprite_data);
                sprite_data['animation'] = new_anim
            if new_name != old_name:
                rect_id = self.rect_ids.pop(old_name);
                self.rect_ids[new_name] = rect_id
            self.update_sprite_listbox();
            self.redraw_sprites();
            dialog.destroy()

        tk.Button(dialog, text="Guardar", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)
        dialog.wait_window()

    def group_sprites_to_animation(self):
        selected_names = [self.sprite_listbox.get(i).strip() for i in self.sprite_listbox.curselection() if
                          not self.sprite_listbox.get(i).strip().startswith("---")]
        if not selected_names: messagebox.showinfo("Error", "Selecciona al menos un sprite para agrupar."); return
        anim_name = self.anim_name_entry.get().strip()
        if not anim_name: messagebox.showinfo("Error", "Ingresa un nombre para la animación."); return
        for sprite_name in selected_names:
            sprite_data = next((s for anim_list in self.project_data['animations'].values() for s in anim_list if
                                s['name'] == sprite_name), None)
            if sprite_data:
                old_anim = sprite_data['animation']
                if old_anim != anim_name:
                    self.project_data['animations'][old_anim].remove(sprite_data)
                    if not self.project_data['animations'][old_anim]: del self.project_data['animations'][old_anim]
                    if anim_name not in self.project_data['animations']: self.project_data['animations'][anim_name] = []
                    self.project_data['animations'][anim_name].append(sprite_data);
                    sprite_data['animation'] = anim_name
        self.update_sprite_listbox();
        self.redraw_sprites()
        messagebox.showinfo("Agrupado", f"Sprites agrupados en la animación '{anim_name}'.")

    def update_sprite_listbox(self):
        self.sprite_listbox.delete(0, tk.END)
        for anim_name in sorted(self.project_data['animations'].keys()):
            self.sprite_listbox.insert(tk.END, f"--- {anim_name.upper()} ---")
            for sprite in sorted(self.project_data['animations'][anim_name], key=lambda s: s['name']):
                self.sprite_listbox.insert(tk.END, f"  {sprite['name']}")

    def redraw_sprites(self, highlight_selected=True):
        self.canvas.delete("rect")
        self.rect_ids.clear()
        for sprites_list in self.project_data['animations'].values():
            for sprite_data in sprites_list:
                rect_id = self.canvas.create_rectangle(sprite_data["x"], sprite_data["y"],
                                                       sprite_data["x"] + sprite_data["width"],
                                                       sprite_data["y"] + sprite_data["height"], outline="red", width=1,
                                                       tags="rect")
                self.rect_ids[sprite_data['name']] = rect_id
        if highlight_selected: self.on_sprite_select(None)

    def suggest_sprites(self):
        if not self.spritesheet_image: messagebox.showinfo("Info", "Primero carga una spritesheet."); return
        if self.get_all_sprites() and not messagebox.askyesno("Confirmar",
                                                              "Esto borrará los sprites actuales. ¿Continuar?"): return

        self.project_data['animations'] = collections.defaultdict(list)
        self.redraw_sprites(highlight_selected=False)

        image = self.spritesheet_image.convert('RGBA')
        pixels = image.load()
        width, height = image.size
        visited = [[False for _ in range(height)] for _ in range(width)]
        background_color = pixels[0, 0] if self.spritesheet_image.mode != 'RGBA' else None

        def find_sprite_bounds(start_x, start_y):
            pixel_color = pixels[start_x, start_y]
            is_transparent = pixel_color[3] == 0
            is_background = background_color and pixel_color[:3] == background_color[:3]
            if visited[start_x][start_y] or is_transparent or is_background: return None

            q = collections.deque([(start_x, start_y)]);
            visited[start_x][start_y] = True
            min_x, max_x, min_y, max_y = start_x, start_x, start_y, start_y

            while q:
                x, y = q.popleft()
                min_x, max_x, min_y, max_y = min(min_x, x), max(max_x, x), min(min_y, y), max(max_y, y)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and not visited[nx][ny]:
                        next_pixel_color = pixels[nx, ny]
                        next_is_trans = next_pixel_color[3] == 0
                        next_is_bg = background_color and next_pixel_color[:3] == background_color[:3]
                        if not next_is_trans and not next_is_bg:
                            visited[nx][ny] = True;
                            q.append((nx, ny))
            return (min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

        count = 0
        for y in range(height):
            for x in range(width):
                rect = find_sprite_bounds(x, y)
                if rect:
                    count += 1
                    sprite_data = {"x": rect[0], "y": rect[1], "width": rect[2], "height": rect[3],
                                   "name": f"sprite_{count}", "description": "Sugerido", "animation": "default"}
                    self.project_data['animations']['default'].append(sprite_data)

        self.redraw_sprites(highlight_selected=False);
        self.update_sprite_listbox()
        messagebox.showinfo("Sugerencia", f"Se encontraron {count} sprites sugeridos.")

    def save_json(self):
        if not self.project_data['spritesheet_path']: messagebox.showinfo("Información",
                                                                          "No hay spritesheet cargada."); return
        project_name = simpledialog.askstring("Nombre del Proyecto", "Introduce el nombre del proyecto:",
                                              initialvalue=self.project_data.get('project_name', 'NuevoProyecto'))
        if not project_name: return
        self.project_data['project_name'] = project_name
        self.project_data['character_name'] = self.character_name_entry.get().strip()

        file_path = filedialog.asksaveasfilename(initialfile=f"{project_name}.json", defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if file_path:
            serializable_data = self.project_data.copy()
            serializable_data['spritesheet_path'] = os.path.basename(self.project_data['spritesheet_path'])
            serializable_data['animations'] = {k: v for k, v in self.project_data['animations'].items()}

            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=4)
            messagebox.showinfo("Guardado", f"Archivo JSON guardado en: {file_path}")


if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Error de Dependencia",
                             "La librería 'Pillow' es necesaria.\n\nPor favor, instálala desde tu terminal con:\npip install Pillow")
        exit()

    root = tk.Tk()
    app = SpritesheetSelectorApp(root)
    root.mainloop()