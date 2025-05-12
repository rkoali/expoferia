import tkinter as tk
from tkinter import ttk, messagebox
from views.proyecto_form import ProyectoForm
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ProfesorDashboard:
    def __init__(self, app, usuario):
        self.app = app
        self.usuario = usuario
        self.db = app.db
        
        # Configure main window
        self.app.root.title(f"Panel de Profesor - {usuario['nombre']}")
        self.app.root.configure(bg='#ffffff')
        
        # Clear existing widgets
        for widget in self.app.root.winfo_children():
            widget.destroy()
            
        # Obtener ID del profesor
        self.profesor_id = self.obtener_id_profesor()
        if not self.profesor_id:
            messagebox.showerror("Error", "No se pudo identificar su perfil de profesor")
            return
            
        self.setup_ui()
        self.load_proyectos()

    def obtener_id_profesor(self):
        try:
            query = "SELECT id_profesor FROM profesores WHERE id_usuario = %s"
            resultado = self.db.execute_query(
                query, 
                (self.usuario['id_usuario'],),
                fetch_one=True
            )
            return resultado['id_profesor'] if resultado else None
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ID de profesor: {str(e)}")
            return None

    def setup_ui(self):
        # Main container
        self.main_container = ttk.Frame(self.app.root, style='Main.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top navigation bar
        nav_frame = ttk.Frame(self.main_container, style='Nav.TFrame')
        nav_frame.pack(fill=tk.X, pady=0)
        
        # Configure styles for modern look
        style = ttk.Style()
        style.configure('Nav.TFrame', background='#6366f1')
        style.configure('Nav.TLabel', background='#6366f1', foreground='white')
        style.configure('NavButton.TButton', background='#4f46e5', padding=5)
        
        # Navigation content
        nav_content = ttk.Frame(nav_frame, style='Nav.TFrame')
        nav_content.pack(fill=tk.X, padx=20, pady=10)
        
        # Left side - Brand and navigation
        nav_left = ttk.Frame(nav_content, style='Nav.TFrame')
        nav_left.pack(side=tk.LEFT)
        
        ttk.Label(
            nav_left,
            text="ExpoFeria",
            style='Nav.TLabel',
            font=('Helvetica', 16, 'bold')
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # Navigation buttons
        self.nav_buttons = []
        for text in ['Proyectos', 'Estudiantes', 'Reportes']:
            btn = ttk.Button(
                nav_left,
                text=text,
                style='NavButton.TButton'
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.nav_buttons.append(btn)
            
        # Right side - User menu
        nav_right = ttk.Frame(nav_content, style='Nav.TFrame')
        nav_right.pack(side=tk.RIGHT)
        
        # User profile section
        profile_frame = ttk.Frame(nav_right, style='Nav.TFrame')
        profile_frame.pack(side=tk.RIGHT, padx=10)
        
        # Load and display profile image
        try:
            response = requests.get("https://i.pravatar.cc/32")
            img = Image.open(BytesIO(response.content))
            photo = ImageTk.PhotoImage(img)
            profile_label = ttk.Label(profile_frame, image=photo)
            profile_label.image = photo
            profile_label.pack(side=tk.LEFT, padx=5)
        except:
            ttk.Label(
                profile_frame,
                text="👤",
                style='Nav.TLabel',
                font=('Helvetica', 16)
            ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            profile_frame,
            text=self.usuario['nombre'],
            style='Nav.TLabel'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            profile_frame,
            text="Cerrar Sesión",
            command=self.logout,
            style='NavButton.TButton'
        ).pack(side=tk.LEFT, padx=5)

        # Main content area with sidebar
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sidebar
        sidebar = ttk.Frame(content_frame, style='Sidebar.TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Sidebar items with icons
        sidebar_items = [
            ('📊 Dashboard', self.show_dashboard),
            ('📁 Proyectos', self.show_proyectos),
            ('👥 Estudiantes', None),
            ('📈 Reportes', None),
            ('⚙️ Configuración', None)
        ]
        
        for text, command in sidebar_items:
            btn = ttk.Button(
                sidebar,
                text=text,
                command=command,
                style='Sidebar.TButton',
                width=20
            )
            btn.pack(fill=tk.X, pady=2)

        # Main content notebook
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Setup tabs
        self.setup_dashboard_tab()
        self.setup_proyectos_tab()

    def setup_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        
        # Statistics section
        stats_frame = ttk.Frame(frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats = [
            ("Proyectos Activos", "5"),
            ("Estudiantes", "15"),
            ("Proyectos Completados", "3"),
            ("Evaluaciones Pendientes", "2")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = ttk.Frame(stats_frame, style='Stat.TFrame')
            stat_frame.grid(row=0, column=i, padx=10)
            
            ttk.Label(
                stat_frame,
                text=value,
                style='StatValue.TLabel',
                font=('Helvetica', 24, 'bold')
            ).pack()
            
            ttk.Label(
                stat_frame,
                text=label,
                style='StatLabel.TLabel'
            ).pack()

    def setup_proyectos_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Proyectos")
        
        # Toolbar with modern styling
        toolbar = ttk.Frame(frame, style='Toolbar.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            toolbar,
            text="+ Nuevo Proyecto",
            command=self.nuevo_proyecto,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Search box
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.insert(0, "Buscar proyectos...")
        
        # Projects table
        columns = ('id', 'titulo', 'estado', 'fecha', 'estudiantes', 'acciones')
        self.proyectos_tree = ttk.Treeview(
            frame,
            columns=columns,
            show='headings',
            style='Modern.Treeview'
        )
        
        # Configure columns
        self.proyectos_tree.heading('id', text='ID')
        self.proyectos_tree.heading('titulo', text='Título')
        self.proyectos_tree.heading('estado', text='Estado')
        self.proyectos_tree.heading('fecha', text='Fecha')
        self.proyectos_tree.heading('estudiantes', text='Estudiantes')
        self.proyectos_tree.heading('acciones', text='Acciones')
        
        # Column widths
        self.proyectos_tree.column('id', width=50)
        self.proyectos_tree.column('titulo', width=300)
        self.proyectos_tree.column('estado', width=100)
        self.proyectos_tree.column('fecha', width=100)
        self.proyectos_tree.column('estudiantes', width=100)
        self.proyectos_tree.column('acciones', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.proyectos_tree.yview)
        self.proyectos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.proyectos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_dashboard(self):
        self.notebook.select(0)

    def show_proyectos(self):
        self.notebook.select(1)

    def load_proyectos(self):
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
                    proyecto['num_estudiantes'],
                    "✏️ 🗑️"
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {str(e)}")

    def nuevo_proyecto(self):
        ProyectoForm(self.app.root, self.db, self.usuario, self.load_proyectos)

    def logout(self):
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.app.logout()