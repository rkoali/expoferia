import tkinter as tk
from tkinter import ttk, messagebox
from views.reportes_view import ReportesWindow
from views.proyecto_form import ProyectoForm
from views.usuario_form import UsuarioForm
from views.usuario_edit_form import UsuarioEditForm
from views.evento_form import EventoForm
from PIL import Image, ImageTk
import requests
from io import BytesIO

class AdminDashboard:
    def __init__(self, app, usuario):
        self.app = app
        self.usuario = usuario
        self.db = app.db
        
        # Configure main window
        self.app.root.title(f"Panel de Administración - {usuario['nombre']}")
        self.app.root.configure(bg='#ffffff')
        
        # Clear existing widgets
        for widget in self.app.root.winfo_children():
            widget.destroy()
            
        self.setup_ui()
        self.load_proyectos()
        self.load_usuarios()
        self.load_eventos()

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
        for text in ['Dashboard', 'Proyectos', 'Usuarios', 'Reportes']:
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
            # Fallback if image loading fails
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
        
        # Main content area
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sidebar
        sidebar = ttk.Frame(content_frame, style='Sidebar.TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Sidebar items
        sidebar_items = [
            ('📊 Dashboard', None),
            ('📁 Proyectos', self.show_proyectos),
            ('👥 Usuarios', self.show_usuarios),
            ('📈 Reportes', self.open_reportes),
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
        self.setup_proyectos_tab()
        self.setup_usuarios_tab()
        self.setup_eventos_tab()

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
        
        # Modern table for projects
        columns = ('id', 'titulo', 'profesor', 'estado', 'fecha', 'acciones')
        self.proyectos_tree = ttk.Treeview(
            frame,
            columns=columns,
            show='headings',
            style='Modern.Treeview'
        )
        
        # Configure columns
        self.proyectos_tree.heading('id', text='ID')
        self.proyectos_tree.heading('titulo', text='Título')
        self.proyectos_tree.heading('profesor', text='Profesor')
        self.proyectos_tree.heading('estado', text='Estado')
        self.proyectos_tree.heading('fecha', text='Fecha')
        self.proyectos_tree.heading('acciones', text='Acciones')
        
        # Column widths
        self.proyectos_tree.column('id', width=50)
        self.proyectos_tree.column('titulo', width=300)
        self.proyectos_tree.column('profesor', width=200)
        self.proyectos_tree.column('estado', width=100)
        self.proyectos_tree.column('fecha', width=100)
        self.proyectos_tree.column('acciones', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.proyectos_tree.yview)
        self.proyectos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.proyectos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_usuarios_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Usuarios")
        
        toolbar = ttk.Frame(frame, style='Toolbar.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            toolbar,
            text="+ Nuevo Usuario",
            command=self.nuevo_usuario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        self.usuarios_tree = ttk.Treeview(frame, columns=('id', 'nombre', 'email', 'rol', 'activo'), selectmode='browse')
        self.usuarios_tree.pack(expand=True, fill=tk.BOTH)
        
        # Configurar columnas
        columns = [
            ('#0', '#', 50),
            ('id', 'ID', 50),
            ('nombre', 'Nombre', 150),
            ('email', 'Email', 200),
            ('rol', 'Rol', 100),
            ('activo', 'Activo', 60)
        ]
        
        for col, text, width in columns:
            self.usuarios_tree.heading(col, text=text)
            self.usuarios_tree.column(col, width=width, stretch=tk.NO if width < 100 else tk.YES)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.usuarios_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.usuarios_tree.configure(yscrollcommand=scrollbar.set)

    def setup_eventos_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Eventos")
        
        toolbar = ttk.Frame(frame, style='Toolbar.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            toolbar,
            text="+ Nuevo Evento",
            command=self.nuevo_evento,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        self.eventos_tree = ttk.Treeview(frame, columns=('id', 'nombre', 'fecha_inicio', 'fecha_fin', 'tipo'), selectmode='browse')
        self.eventos_tree.pack(expand=True, fill=tk.BOTH)
        
        # Configurar columnas
        columns = [
            ('#0', '#', 50),
            ('id', 'ID', 50),
            ('nombre', 'Nombre', 200),
            ('fecha_inicio', 'Fecha Inicio', 120),
            ('fecha_fin', 'Fecha Fin', 120),
            ('tipo', 'Tipo', 100)
        ]
        
        for col, text, width in columns:
            self.eventos_tree.heading(col, text=text)
            self.eventos_tree.column(col, width=width, stretch=tk.NO if width < 100 else tk.YES)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.eventos_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.eventos_tree.configure(yscrollcommand=scrollbar.set)

    def show_proyectos(self):
        self.notebook.select(0)

    def show_usuarios(self):
        self.notebook.select(1)

    def logout(self):
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.app.logout()

    def load_proyectos(self):
        try:
            self.proyectos_tree.delete(*self.proyectos_tree.get_children())
            
            query = """
            SELECT p.id_proyecto, p.titulo, CONCAT(u.nombre, ' ', u.apellido) as profesor, 
                   p.estado, p.fecha_creacion 
            FROM proyectos p
            JOIN profesores pr ON p.id_profesor_responsable = pr.id_profesor
            JOIN usuarios u ON pr.id_usuario = u.id_usuario
            """
            proyectos = self.db.execute_query(query, fetch_all=True)
            
            for idx, proyecto in enumerate(proyectos, start=1):
                self.proyectos_tree.insert('', tk.END, text=str(idx), values=(
                    proyecto['id_proyecto'],
                    proyecto['titulo'],
                    proyecto['profesor'],
                    proyecto['estado'],
                    proyecto['fecha_creacion']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar proyectos: {str(e)}")

    def load_usuarios(self):
        try:
            self.usuarios_tree.delete(*self.usuarios_tree.get_children())
            
            query = "SELECT id_usuario, nombre, email, rol, activo FROM usuarios"
            usuarios = self.db.execute_query(query, fetch_all=True)
            
            for idx, usuario in enumerate(usuarios, start=1):
                self.usuarios_tree.insert('', tk.END, text=str(idx), values=(
                    usuario['id_usuario'],
                    usuario['nombre'],
                    usuario['email'],
                    usuario['rol'],
                    'Sí' if usuario['activo'] else 'No'
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")

    def load_eventos(self):
        try:
            self.eventos_tree.delete(*self.eventos_tree.get_children())
            
            query = "SELECT id_evento, nombre, fecha_inicio, fecha_fin, tipo FROM eventos"
            eventos = self.db.execute_query(query, fetch_all=True)
            
            for idx, evento in enumerate(eventos, start=1):
                self.eventos_tree.insert('', tk.END, text=str(idx), values=(
                    evento['id_evento'],
                    evento['nombre'],
                    evento['fecha_inicio'].strftime('%Y-%m-%d %H:%M'),
                    evento['fecha_fin'].strftime('%Y-%m-%d %H:%M'),
                    evento['tipo']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar eventos: {str(e)}")

    def nuevo_proyecto(self):
        ProyectoForm(self.window, self.db, None, self.load_proyectos)

    def editar_proyecto(self):
        selected = self.proyectos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un proyecto")
            return
            
        proyecto_id = self.proyectos_tree.item(selected[0])['values'][0]
        proyecto = self.db.execute_query(
            "SELECT * FROM proyectos WHERE id_proyecto = %s", 
            (proyecto_id,), 
            fetch_one=True
        )
        
        if proyecto:
            form = ProyectoForm(self.window, self.db, None, self.load_proyectos)
            form.proyecto = proyecto
        else:
            messagebox.showerror("Error", "No se encontró el proyecto seleccionado")

    def eliminar_proyecto(self):
        selected = self.proyectos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un proyecto")
            return
            
        proyecto_id = self.proyectos_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proyecto?"):
            try:
                self.db.execute_query(
                    "DELETE FROM proyectos WHERE id_proyecto = %s",
                    (proyecto_id,),
                    commit=True
                )
                messagebox.showinfo("Éxito", "Proyecto eliminado correctamente")
                self.load_proyectos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar proyecto: {str(e)}")

    def nuevo_usuario(self):
        UsuarioForm(self.window, self.db, self.load_usuarios)

    def editar_usuario(self):
        selected = self.usuarios_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
            
        usuario_id = self.usuarios_tree.item(selected[0])['values'][0]
        UsuarioEditForm(self.window, self.db, usuario_id, self.load_usuarios)

    def eliminar_usuario(self):
        selected = self.usuarios_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
            
        usuario_id = self.usuarios_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            try:
                self.db.execute_query(
                    "DELETE FROM usuarios WHERE id_usuario = %s",
                    (usuario_id,),
                    commit=True
                )
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.load_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {str(e)}")

    def nuevo_evento(self):
        EventoForm(self.window, self.db, self.load_eventos)

    def editar_evento(self):
        selected = self.eventos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un evento")
            return
            
        evento_id = self.eventos_tree.item(selected[0])['values'][0]
        evento = self.db.execute_query(
            "SELECT * FROM eventos WHERE id_evento = %s",
            (evento_id,),
            fetch_one=True
        )
        
        if evento:
            form = EventoForm(self.window, self.db, self.load_eventos)
            form.evento = evento
        else:
            messagebox.showerror("Error", "No se encontró el evento seleccionado")

    def eliminar_evento(self):
        selected = self.eventos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un evento")
            return
            
        evento_id = self.eventos_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este evento?"):
            try:
                self.db.execute_query(
                    "DELETE FROM eventos WHERE id_evento = %s",
                    (evento_id,),
                    commit=True
                )
                messagebox.showinfo("Éxito", "Evento eliminado correctamente")
                self.load_eventos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar evento: {str(e)}")

    def open_reportes(self):
        ReportesWindow(self.window, self.db)