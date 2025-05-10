import tkinter as tk
from tkinter import ttk, messagebox
from models.proyecto import Proyecto
from models.profesor import Profesor

class ProyectoForm:
    def __init__(self, parent, db, usuario, on_save_callback=None):
        self.parent = parent
        self.db = db
        self.usuario = usuario  # None para admin, objeto usuario para estudiantes/profesores
        self.on_save = on_save_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Proyecto" if not hasattr(self, 'proyecto') else "Editar Proyecto")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.profesor_model = Profesor(db)
        self.proyecto_model = Proyecto(db)
        
        # Configurar protocolo para manejar cierre de ventana
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        title = "Nuevo Proyecto" if not hasattr(self, 'proyecto') else "Editar Proyecto"
        ttk.Label(main_frame, text=title, style='Title.TLabel').pack(pady=5)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, fill=tk.X)
        
        # Campos comunes
        ttk.Label(form_frame, text="Título*:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.titulo_entry = ttk.Entry(form_frame, width=40)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.NE)
        self.descripcion_text = tk.Text(form_frame, width=40, height=5)
        self.descripcion_text.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Área de Conocimiento:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.area_entry = ttk.Entry(form_frame, width=40)
        self.area_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Campo específico para estudiantes (selección de profesor)
        if self.usuario and self.usuario['rol'] == 'estudiante':
            ttk.Label(form_frame, text="Profesor Responsable*:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
            self.profesor_combo = ttk.Combobox(form_frame, width=37, state="readonly")
            self.profesor_combo.grid(row=3, column=1, padx=5, pady=5)
            self._cargar_profesores()
        
        # Campo específico para profesores (estado del proyecto)
        if self.usuario and self.usuario['rol'] == 'profesor' and hasattr(self, 'proyecto'):
            ttk.Label(form_frame, text="Estado*:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
            self.estado_combo = ttk.Combobox(
                form_frame, 
                values=['en_proceso', 'aprobado', 'rechazado'], 
                width=37,
                state="readonly"
            )
            self.estado_combo.grid(row=4, column=1, padx=5, pady=5)
            self.estado_combo.current(0)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame, 
            text="Guardar", 
            command=self._guardar,
            style='Accent.TButton' if hasattr(ttk.Style(), 'map') else None
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=self._on_close
        ).pack(side=tk.LEFT, padx=5)
        
        # Configurar enfoque inicial
        self.titulo_entry.focus_set()
        
    def _cargar_profesores(self):
        try:
            profesores = self.profesor_model.obtener_todos()
            opciones = []
            self.profesor_map = {}
            
            for profesor in profesores:
                nombre = f"{profesor['nombre']} {profesor['apellido']} - {profesor['departamento']}"
                opciones.append(nombre)
                self.profesor_map[nombre] = profesor['id_profesor']
            
            self.profesor_combo['values'] = opciones
            if opciones:
                self.profesor_combo.current(0)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los profesores: {str(e)}")
            self._on_close()
    
    def _guardar(self):
        titulo = self.titulo_entry.get().strip()
        descripcion = self.descripcion_text.get("1.0", tk.END).strip()
        area = self.area_entry.get().strip()
        
        # Validaciones básicas
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            self.titulo_entry.focus_set()
            return
            
        try:
            if self.usuario and self.usuario['rol'] == 'estudiante':
                # Nuevo proyecto desde estudiante
                profesor_nombre = self.profesor_combo.get()
                if not profesor_nombre:
                    messagebox.showerror("Error", "Debe seleccionar un profesor responsable")
                    return
                
                id_profesor = self.profesor_map[profesor_nombre]
                
                proyecto_id = self.proyecto_model.crear_proyecto(
                    titulo=titulo,
                    descripcion=descripcion if descripcion else None,
                    profesor_id=id_profesor,
                    area_conocimiento=area if area else None
                )
                
                messagebox.showinfo("Éxito", "Proyecto creado correctamente")
                
            elif self.usuario and self.usuario['rol'] == 'profesor' and hasattr(self, 'proyecto'):
                # Edición de estado por profesor
                estado = self.estado_combo.get()
                
                self.proyecto_model.actualizar_proyecto(
                    proyecto_id=self.proyecto['id_proyecto'],
                    titulo=titulo,
                    descripcion=descripcion if descripcion else None,
                    area_conocimiento=area if area else None,
                    estado=estado
                )
                messagebox.showinfo("Éxito", "Proyecto actualizado correctamente")
            
            elif not self.usuario:  # Modo administrador
                if hasattr(self, 'proyecto'):
                    # Edición completa (admin)
                    self.proyecto_model.actualizar_proyecto(
                        proyecto_id=self.proyecto['id_proyecto'],
                        titulo=titulo,
                        descripcion=descripcion if descripcion else None,
                        area_conocimiento=area if area else None
                    )
                    messagebox.showinfo("Éxito", "Proyecto actualizado correctamente")
                else:
                    messagebox.showerror("Error", "En modo administrador debe seleccionar un profesor")
                    return
            
            if self.on_save:
                self.on_save()
                
            self._on_close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar proyecto: {str(e)}")
            print(f"Error detallado: {e}")  # Para depuración
    
    def _on_close(self):
        self.window.destroy()