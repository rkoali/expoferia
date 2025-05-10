# evento_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.database_connection import DatabaseConnection
from models.profesor import Profesor

class EventoForm:
    def __init__(self, parent, db, on_save_callback=None, evento=None):
        self.parent = parent
        self.db = db
        self.on_save = on_save_callback
        self.evento = evento  # Datos existentes para edición
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Evento" if not evento else "Editar Evento")
        self.window.geometry("500x450")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.profesor_model = Profesor(db)
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        title = "Nuevo Evento" if not self.evento else "Editar Evento"
        ttk.Label(main_frame, text=title, style='Title.TLabel').pack(pady=5)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, fill=tk.X)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre*:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.nombre_entry = ttk.Entry(form_frame, width=40)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.NE)
        self.descripcion_text = tk.Text(form_frame, width=40, height=5)
        self.descripcion_text.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Fecha Inicio*:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.fecha_inicio_entry = ttk.Entry(form_frame, width=40)
        self.fecha_inicio_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Formato: YYYY-MM-DD HH:MM").grid(row=3, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Fecha Fin*:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.fecha_fin_entry = ttk.Entry(form_frame, width=40)
        self.fecha_fin_entry.grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Formato: YYYY-MM-DD HH:MM").grid(row=5, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Tipo*:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.tipo_combo = ttk.Combobox(
            form_frame, 
            values=['inscripcion', 'evaluacion', 'feria', 'reunion', 'otro'], 
            width=37,
            state="readonly"
        )
        self.tipo_combo.grid(row=6, column=1, padx=5, pady=5)
        self.tipo_combo.current(0)
        
        ttk.Label(form_frame, text="Ubicación:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.ubicacion_entry = ttk.Entry(form_frame, width=40)
        self.ubicacion_entry.grid(row=7, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Responsable:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.responsable_combo = ttk.Combobox(form_frame, width=37, state="readonly")
        self.responsable_combo.grid(row=8, column=1, padx=5, pady=5)
        self._cargar_profesores()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Cargar datos si estamos editando
        if self.evento:
            self._cargar_datos()
        
        self.nombre_entry.focus_set()
    
    def _cargar_profesores(self):
        try:
            profesores = self.profesor_model.obtener_todos()
            opciones = []
            self.profesor_map = {}
            
            for profesor in profesores:
                nombre = f"{profesor['nombre']} {profesor['apellido']} - {profesor['departamento']}"
                opciones.append(nombre)
                self.profesor_map[nombre] = profesor['id_profesor']
            
            self.responsable_combo['values'] = opciones
            if opciones:
                self.responsable_combo.current(0)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los profesores: {str(e)}")
    
    def _cargar_datos(self):
        """Carga los datos del evento en el formulario para edición"""
        self.nombre_entry.insert(0, self.evento['nombre'])
        self.descripcion_text.insert("1.0", self.evento.get('descripcion', ''))
        self.fecha_inicio_entry.insert(0, self.evento['fecha_inicio'].strftime('%Y-%m-%d %H:%M'))
        self.fecha_fin_entry.insert(0, self.evento['fecha_fin'].strftime('%Y-%m-%d %H:%M'))
        self.tipo_combo.set(self.evento['tipo'])
        self.ubicacion_entry.insert(0, self.evento.get('ubicacion', ''))
        
        # Seleccionar responsable si existe
        if self.evento.get('responsable'):
            profesor = self.db.execute_query(
                "SELECT p.*, u.nombre, u.apellido FROM profesores p JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.id_profesor = %s",
                (self.evento['responsable'],),
                fetch_one=True
            )
            if profesor:
                nombre = f"{profesor['nombre']} {profesor['apellido']} - {profesor['departamento']}"
                if nombre in self.profesor_map:
                    index = list(self.profesor_map.keys()).index(nombre)
                    self.responsable_combo.current(index)
    
    def _validar_fecha(self, fecha_str):
        try:
            return datetime.strptime(fecha_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return None
    
    def _guardar(self):
        nombre = self.nombre_entry.get().strip()
        descripcion = self.descripcion_text.get("1.0", tk.END).strip()
        fecha_inicio_str = self.fecha_inicio_entry.get().strip()
        fecha_fin_str = self.fecha_fin_entry.get().strip()
        tipo = self.tipo_combo.get()
        ubicacion = self.ubicacion_entry.get().strip()
        responsable_nombre = self.responsable_combo.get()
        
        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
            
        fecha_inicio = self._validar_fecha(fecha_inicio_str)
        if not fecha_inicio:
            messagebox.showerror("Error", "Formato de fecha inicio inválido. Use YYYY-MM-DD HH:MM")
            return
            
        fecha_fin = self._validar_fecha(fecha_fin_str)
        if not fecha_fin:
            messagebox.showerror("Error", "Formato de fecha fin inválido. Use YYYY-MM-DD HH:MM")
            return
            
        if fecha_fin <= fecha_inicio:
            messagebox.showerror("Error", "La fecha fin debe ser posterior a la fecha inicio")
            return
            
        responsable_id = None
        if responsable_nombre:
            responsable_id = self.profesor_map.get(responsable_nombre)
        
        try:
            if self.evento:
                # Actualizar evento existente
                query = """
                UPDATE eventos 
                SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s, 
                    tipo = %s, ubicacion = %s, responsable = %s
                WHERE id_evento = %s
                """
                params = (
                    nombre,
                    descripcion if descripcion else None,
                    fecha_inicio,
                    fecha_fin,
                    tipo,
                    ubicacion if ubicacion else None,
                    responsable_id,
                    self.evento['id_evento']
                )
            else:
                # Crear nuevo evento
                query = """
                INSERT INTO eventos 
                (nombre, descripcion, fecha_inicio, fecha_fin, tipo, ubicacion, responsable)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    nombre,
                    descripcion if descripcion else None,
                    fecha_inicio,
                    fecha_fin,
                    tipo,
                    ubicacion if ubicacion else None,
                    responsable_id
                )
            
            self.db.execute_query(query, params, commit=True)
            messagebox.showinfo("Éxito", "Evento guardado correctamente")
            
            if self.on_save:
                self.on_save()
                
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar evento: {str(e)}")