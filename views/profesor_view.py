import tkinter as tk
from tkinter import ttk, messagebox
from views.proyecto_form import ProyectoForm

class ProfesorDashboard:
    def __init__(self, app, usuario):
        self.app = app
        self.usuario = usuario
        self.db = app.db
        
        self.window = tk.Toplevel(app.root)
        self.window.title(f"Panel de Profesor - {usuario['nombre']}")
        self.window.geometry("1000x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Obtener ID del profesor
        self.profesor_id = self.obtener_id_profesor()
        if not self.profesor_id:
            messagebox.showerror("Error", "No se pudo identificar su perfil de profesor")
            self.window.destroy()
            return
            
        self.setup_ui()
        self.load_proyectos()

    def obtener_id_profesor(self):
        """Obtiene el ID del profesor desde la base de datos"""
        try:
            query = "SELECT id_profesor FROM profesores WHERE id_usuario = %s"
            resultado = self.db.execute_query(
                query, 
                (self.usuario['id_usuario'],),  # Nota la coma para crear una tupla
                fetch_one=True
            )
            return resultado['id_profesor'] if resultado else None
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ID de profesor: {str(e)}")
            return None

    def setup_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Barra superior
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_frame, text=f"Bienvenido, Profesor {self.usuario['nombre']}", style='Title.TLabel').pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="Cerrar Sesión", command=self.logout).pack(side=tk.LEFT, padx=2)

        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Pestaña de Proyectos
        proyectos_frame = ttk.Frame(self.notebook)
        self.notebook.add(proyectos_frame, text="Mis Proyectos")
        self.setup_proyectos_tab(proyectos_frame)

    def setup_proyectos_tab(self, parent):
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="Nuevo Proyecto", command=self.nuevo_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Editar", command=self.editar_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Actualizar", command=self.load_proyectos).pack(side=tk.LEFT, padx=2)

        # Treeview
        self.proyectos_tree = ttk.Treeview(parent, 
                                         columns=('id', 'titulo', 'estado', 'fecha', 'estudiantes'), 
                                         selectmode='browse')
        self.proyectos_tree.pack(expand=True, fill=tk.BOTH)
        
        # Configurar columnas
        columns = [
            ('#0', '#', 50),
            ('id', 'ID', 50),
            ('titulo', 'Título', 250),
            ('estado', 'Estado', 100),
            ('fecha', 'Fecha', 100),
            ('estudiantes', 'Estudiantes', 100)
        ]
        
        for col, text, width in columns:
            self.proyectos_tree.heading(col, text=text)
            self.proyectos_tree.column(col, width=width, stretch=tk.NO if width < 100 else tk.YES)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.proyectos_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.proyectos_tree.configure(yscrollcommand=scrollbar.set)

    def load_proyectos(self):
        """Carga los proyectos del profesor"""
        try:
            self.proyectos_tree.delete(*self.proyectos_tree.get_children())
            
            query = """
            SELECT p.id_proyecto, p.titulo, p.estado, p.fecha_creacion, 
                   COUNT(pe.id_estudiante) as num_estudiantes
            FROM proyectos p
            LEFT JOIN proyecto_estudiantes pe ON p.id_proyecto = pe.id_proyecto
            WHERE p.id_profesor_responsable = %s
            GROUP BY p.id_proyecto
            ORDER BY p.fecha_creacion DESC
            """
            proyectos = self.db.execute_query(query, (self.profesor_id,), fetch_all=True)
            
            for idx, proyecto in enumerate(proyectos, 1):
                self.proyectos_tree.insert('', tk.END, text=str(idx), values=(
                    proyecto['id_proyecto'],
                    proyecto['titulo'],
                    proyecto['estado'],
                    proyecto['fecha_creacion'].strftime('%Y-%m-%d'),
                    proyecto['num_estudiantes']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {str(e)}")

    def nuevo_proyecto(self):
        """Abre formulario para nuevo proyecto"""
        ProyectoForm(self.window, self.db, self.usuario, self.load_proyectos)

    def editar_proyecto(self):
        """Abre formulario para editar proyecto"""
        selected = self.proyectos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proyecto")
            return
            
        proyecto_id = self.proyectos_tree.item(selected[0])['values'][0]
        proyecto = self.db.execute_query(
            "SELECT * FROM proyectos WHERE id_proyecto = %s",
            (proyecto_id,),
            fetch_one=True
        )
        
        if proyecto:
            form = ProyectoForm(self.window, self.db, self.usuario, self.load_proyectos)
            form.proyecto = proyecto
        else:
            messagebox.showerror("Error", "No se encontró el proyecto")

    def logout(self):
        self.window.destroy()
        self.app.logout()

    def on_close(self):
        if messagebox.askokcancel("Salir", "¿Cerrar sesión?"):
            self.logout()