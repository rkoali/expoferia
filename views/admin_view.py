import tkinter as tk
from tkinter import ttk, messagebox
from views.reportes_view import ReportesWindow
from views.proyecto_form import ProyectoForm
from views.usuario_form import UsuarioForm
from views.usuario_edit_form import UsuarioEditForm
from views.evento_form import EventoForm  # Asumiendo que existe este módulo

class AdminDashboard:
    def __init__(self, app, usuario):
        self.app = app
        self.usuario = usuario
        self.db = app.db
        
        self.window = tk.Toplevel(app.root)
        self.window.title(f"Panel de Administración - Bienvenido {usuario['nombre']}")
        self.window.geometry("1200x700")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
        self.load_proyectos()
        self.load_usuarios()
        self.load_eventos()

    def setup_ui(self):
        """Configura la interfaz principal del dashboard"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Barra superior
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_frame, text="Panel de Administración", style='Title.TLabel').pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Generar Reporte", command=self.open_reportes).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Cerrar Sesión", command=self.logout).pack(side=tk.LEFT, padx=2)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # Configurar pestañas
        self.setup_proyectos_tab()
        self.setup_usuarios_tab()
        self.setup_eventos_tab()

    def setup_proyectos_tab(self):
        """Configura la pestaña de proyectos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Proyectos")
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="Nuevo", command=self.nuevo_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Editar", command=self.editar_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Eliminar", command=self.eliminar_proyecto).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Actualizar", command=self.load_proyectos).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        self.proyectos_tree = ttk.Treeview(frame, columns=('id', 'titulo', 'profesor', 'estado', 'fecha'), selectmode='browse')
        self.proyectos_tree.pack(expand=True, fill=tk.BOTH)
        
        # Configurar columnas
        columns = [
            ('#0', '#', 50),
            ('id', 'ID', 50),
            ('titulo', 'Título', 200),
            ('profesor', 'Profesor', 150),
            ('estado', 'Estado', 100),
            ('fecha', 'Fecha Creación', 100)
        ]
        
        for col, text, width in columns:
            self.proyectos_tree.heading(col, text=text)
            self.proyectos_tree.column(col, width=width, stretch=tk.NO if width < 100 else tk.YES)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.proyectos_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.proyectos_tree.configure(yscrollcommand=scrollbar.set)

    def setup_usuarios_tab(self):
        """Configura la pestaña de usuarios"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Usuarios")
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="Nuevo", command=self.nuevo_usuario).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Editar", command=self.editar_usuario).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Eliminar", command=self.eliminar_usuario).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Actualizar", command=self.load_usuarios).pack(side=tk.LEFT, padx=2)
        
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
        """Configura la pestaña de eventos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Eventos")
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="Nuevo", command=self.nuevo_evento).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Editar", command=self.editar_evento).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Eliminar", command=self.eliminar_evento).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Actualizar", command=self.load_eventos).pack(side=tk.LEFT, padx=2)
        
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

    # Métodos para cargar datos
    def load_proyectos(self):
        """Carga los proyectos desde la base de datos"""
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
        """Carga los usuarios desde la base de datos"""
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
        """Carga los eventos desde la base de datos"""
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

    # Métodos CRUD para Proyectos
    def nuevo_proyecto(self):
        """Abre el formulario para crear un nuevo proyecto"""
        ProyectoForm(self.window, self.db, None, self.load_proyectos)

    def editar_proyecto(self):
        """Abre el formulario para editar un proyecto existente"""
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
        """Elimina el proyecto seleccionado"""
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

    # Métodos CRUD para Usuarios
    def nuevo_usuario(self):
        """Abre el formulario para crear un nuevo usuario"""
        UsuarioForm(self.window, self.db, self.load_usuarios)

    def editar_usuario(self):
        """Abre el formulario para editar un usuario existente"""
        selected = self.usuarios_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
            
        usuario_id = self.usuarios_tree.item(selected[0])['values'][0]
        UsuarioEditForm(self.window, self.db, usuario_id, self.load_usuarios)

    def eliminar_usuario(self):
        """Elimina el usuario seleccionado"""
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

    # Métodos CRUD para Eventos
    def nuevo_evento(self):
        """Abre el formulario para crear un nuevo evento"""
        EventoForm(self.window, self.db, self.load_eventos)

    def editar_evento(self):
        """Abre el formulario para editar un evento existente"""
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
        """Elimina el evento seleccionado"""
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

    # Otros métodos
    def open_reportes(self):
        """Abre la ventana de generación de reportes"""
        ReportesWindow(self.window, self.db)

    def logout(self):
        """Cierra la sesión del administrador"""
        self.window.destroy()
        self.app.logout()

    def on_close(self):
        """Maneja el cierre de la ventana"""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir del sistema?"):
            self.window.destroy()
            self.app.root.quit()