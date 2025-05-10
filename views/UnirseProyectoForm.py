import tkinter as tk
from tkinter import ttk, messagebox

class UnirseProyectoForm:
    def __init__(self, parent, db, estudiante_id, on_success_callback=None):
        self.parent = parent
        self.db = db
        self.estudiante_id = estudiante_id
        self.on_success = on_success_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Unirse a Proyecto")
        self.window.geometry("500x300")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(main_frame, text="Unirse a Proyecto Existente", style='Title.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(form_frame, text="ID del Proyecto:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.proyecto_id_entry = ttk.Entry(form_frame, width=40)
        self.proyecto_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Rol en el Proyecto:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.rol_entry = ttk.Entry(form_frame, width=40)
        self.rol_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Ej: Desarrollador, Diseñador, Investigador").grid(row=2, column=1, padx=5, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Unirse", command=self.unirse_proyecto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
    def unirse_proyecto(self):
        proyecto_id = self.proyecto_id_entry.get().strip()
        rol = self.rol_entry.get().strip()
        
        if not proyecto_id or not rol:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return
            
        try:
            proyecto_id = int(proyecto_id)
            
            # Verificar que el proyecto existe
            proyecto = self.db.execute_query(
                "SELECT id_proyecto FROM proyectos WHERE id_proyecto = %s",
                (proyecto_id,),
                fetch_one=True
            )
            
            if not proyecto:
                messagebox.showerror("Error", "El proyecto no existe")
                return
                
            # Verificar que no está ya en el proyecto
            existe = self.db.execute_query(
                "SELECT 1 FROM proyecto_estudiantes WHERE id_proyecto = %s AND id_estudiante = %s",
                (proyecto_id, self.estudiante_id),
                fetch_one=True
            )
            
            if existe:
                messagebox.showwarning("Advertencia", "Ya estás en este proyecto")
                return
                
            # Unirse al proyecto
            query = """
            INSERT INTO proyecto_estudiantes 
            (id_proyecto, id_estudiante, rol_en_proyecto, fecha_incorporacion)
            VALUES (%s, %s, %s, CURDATE())
            """
            self.db.execute_query(
                query,
                (proyecto_id, self.estudiante_id, rol),
                commit=True
            )
            
            messagebox.showinfo("Éxito", "Te has unido al proyecto exitosamente")
            self.window.destroy()
            
            if self.on_success:
                self.on_success()
                
        except ValueError:
            messagebox.showerror("Error", "ID de proyecto debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo unir al proyecto: {str(e)}")