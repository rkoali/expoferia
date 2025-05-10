import tkinter as tk
from tkinter import ttk, messagebox
from views.proyecto_form import UnirseProyectoForm  # Necesitarás crear este formulario

class EstudianteDashboard:
    def __init__(self, app, usuario):
        self.app = app
        self.usuario = usuario
        self.db = app.db
        
        # Obtener ID del estudiante
        self.estudiante_id = self.obtener_id_estudiante()
        if not self.estudiante_id:
            messagebox.showerror("Error", "No se pudo identificar su perfil de estudiante")
            self.window.destroy()
            return
            
        self.window = tk.Toplevel(app.root)
        self.window.title(f"Panel de Estudiante - {usuario['nombre']}")
        self.window.geometry("1000x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
        self.load_proyectos()

    def obtener_id_estudiante(self):
        """Obtiene el ID del estudiante desde la base de datos"""
        query = "SELECT id_estudiante FROM estudiantes WHERE id_usuario = %s"
        resultado = self.db.execute_query(query, (self.usuario['id_usuario'],), fetch_one=True)
        return resultado['id_estudiante'] if resultado else None

    def setup_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Barra superior
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_frame, text=f"Bienvenido, Estudiante {self.usuario['nombre']}", style='Title.TLabel').pack(side=tk.LEFT)
        
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
        
        ttk.Button(toolbar, text="Unirse a Proyecto", command=self.unirse_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Actualizar", command=self.load_proyectos).pack(side=tk.LEFT, padx=2)

        # Treeview
        self.proyectos_tree = ttk.Treeview(parent, columns=('id', 'titulo', 'profesor', 'rol', 'fecha'), selectmode='browse')
        self.proyectos_tree.pack(expand=True, fill=tk.BOTH)
        
        # Configurar columnas
        columns = [
            ('#0', '#', 50),
            ('id', 'ID', 50),
            ('titulo', 'Título', 250),
            ('profesor', 'Profesor', 150),
            ('rol', 'Mi Rol', 100),
            ('fecha', 'Fecha Ingreso', 100)
        ]
        
        for col, text, width in columns:
            self.proyectos_tree.heading(col, text=text)
            self.proyectos_tree.column(col, width=width, stretch=tk.NO if width < 100 else tk.YES)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.proyectos_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.proyectos_tree.configure(yscrollcommand=scrollbar.set)

    def load_proyectos(self):
        """Carga los proyectos del estudiante"""
        try:
            self.proyectos_tree.delete(*self.proyectos_tree.get_children())
            
            query = """
            SELECT p.id_proyecto, p.titulo, CONCAT(u.nombre, ' ', u.apellido) as profesor, 
                   pe.rol_en_proyecto, pe.fecha_incorporacion
            FROM proyecto_estudiantes pe
            JOIN proyectos p ON pe.id_proyecto = p.id_proyecto
            JOIN profesores pr ON p.id_profesor_responsable = pr.id_profesor
            JOIN usuarios u ON pr.id_usuario = u.id_usuario
            WHERE pe.id_estudiante = %s
            ORDER BY pe.fecha_incorporacion DESC
            """
            proyectos = self.db.execute_query(query, (self.estudiante_id,), fetch_all=True)
            
            for idx, proyecto in enumerate(proyectos, 1):
                self.proyectos_tree.insert('', tk.END, text=str(idx), values=(
                    proyecto['id_proyecto'],
                    proyecto['titulo'],
                    proyecto['profesor'],
                    proyecto['rol_en_proyecto'],
                    proyecto['fecha_incorporacion'].strftime('%Y-%m-%d')
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {str(e)}")

    def unirse_proyecto(self):
        """Abre formulario para unirse a proyecto"""
        UnirseProyectoForm(self.window, self.db, self.estudiante_id, self.load_proyectos)

    def logout(self):
        self.window.destroy()
        self.app.logout()

    def on_close(self):
        if messagebox.askokcancel("Salir", "¿Cerrar sesión?"):
            self.logout()