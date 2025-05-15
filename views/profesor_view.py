import tkinter as tk
from tkinter import ttk, messagebox
from views.proyecto_form import ProyectoForm
from PIL import Image, ImageTk
import requests
from io import BytesIO
from ttkthemes import ThemedTk

class ProyectoCard(ttk.Frame):
    def __init__(self, parent, proyecto, on_approve, on_reject, on_comment):
        super().__init__(parent, style='Card.TFrame')
        
        # Project title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=10, pady=(10,5))
        
        ttk.Label(
            title_frame,
            text=proyecto['titulo'],
            style='CardTitle.TLabel'
        ).pack(side=tk.LEFT)
        
        status_label = ttk.Label(
            title_frame,
            text=proyecto['estado'],
            style=f'Status{proyecto["estado"].capitalize()}.TLabel'
        )
        status_label.pack(side=tk.RIGHT)
        
        # Project description
        desc_frame = ttk.Frame(self)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(
            desc_frame,
            text=proyecto['descripcion'] or "Sin descripción",
            style='CardDesc.TLabel',
            wraplength=400
        ).pack(anchor=tk.W)
        
        # Project metadata
        meta_frame = ttk.Frame(self)
        meta_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(
            meta_frame,
            text=f"👥 {proyecto['num_estudiantes']} estudiantes",
            style='CardMeta.TLabel'
        ).pack(side=tk.LEFT, padx=(0,10))
        
        ttk.Label(
            meta_frame,
            text=f"📅 {proyecto['fecha_creacion']}",
            style='CardMeta.TLabel'
        ).pack(side=tk.LEFT)
        
        # Actions
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=(5,10))
        
        if proyecto['estado'] == 'en_proceso':
            ttk.Button(
                action_frame,
                text="✓ Aprobar",
                style='Success.TButton',
                command=lambda: on_approve(proyecto['id_proyecto'])
            ).pack(side=tk.LEFT, padx=(0,5))
            
            ttk.Button(
                action_frame,
                text="✗ Rechazar",
                style='Danger.TButton',
                command=lambda: on_reject(proyecto['id_proyecto'])
            ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="💬 Comentar",
            style='Info.TButton',
            command=lambda: on_comment(proyecto['id_proyecto'])
        ).pack(side=tk.LEFT, padx=5)

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
            
        self.setup_styles()
        self.setup_ui()
        self.load_proyectos()

    def setup_styles(self):
        style = ttk.Style()
        
        # Frame styles
        style.configure('Card.TFrame', background='#ffffff', relief='solid', borderwidth=1)
        style.configure('Header.TFrame', background='#24292e')
        
        # Label styles
        style.configure('CardTitle.TLabel', 
                       font=('Segoe UI', 14, 'bold'),
                       foreground='#24292e',
                       background='#ffffff')
                       
        style.configure('CardDesc.TLabel',
                       font=('Segoe UI', 11),
                       foreground='#57606a',
                       background='#ffffff')
                       
        style.configure('CardMeta.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#57606a',
                       background='#ffffff')
                       
        style.configure('StatusEnProceso.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#0969da',
                       background='#ddf4ff',
                       padding=5)
                       
        style.configure('StatusAprobado.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#1a7f37',
                       background='#dafbe1',
                       padding=5)
                       
        style.configure('StatusRechazado.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#cf222e',
                       background='#ffebe9',
                       padding=5)
        
        # Button styles
        style.configure('Success.TButton',
                       font=('Segoe UI', 10),
                       background='#2da44e',
                       foreground='#ffffff')
                       
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10),
                       background='#cf222e',
                       foreground='#ffffff')
                       
        style.configure('Info.TButton',
                       font=('Segoe UI', 10),
                       background='#0969da',
                       foreground='#ffffff')

    def setup_ui(self):
        # Header
        header = ttk.Frame(self.app.root, style='Header.TFrame')
        header.pack(fill=tk.X, pady=(0,20))
        
        # Logo and title
        ttk.Label(
            header,
            text="ExpoFeria",
            font=('Segoe UI', 20, 'bold'),
            foreground='#ffffff',
            background='#24292e'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # User menu
        user_frame = ttk.Frame(header, style='Header.TFrame')
        user_frame.pack(side=tk.RIGHT, padx=20)
        
        ttk.Label(
            user_frame,
            text=f"👤 {self.usuario['nombre']}",
            font=('Segoe UI', 12),
            foreground='#ffffff',
            background='#24292e'
        ).pack(side=tk.LEFT, padx=(0,10))
        
        ttk.Button(
            user_frame,
            text="Cerrar Sesión",
            command=self.logout
        ).pack(side=tk.LEFT)
        
        # Main content
        main_frame = ttk.Frame(self.app.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0,20))
        
        ttk.Label(
            toolbar,
            text="Proyectos",
            font=('Segoe UI', 24, 'bold')
        ).pack(side=tk.LEFT)
        
        # Filter buttons
        self.filter_var = tk.StringVar(value='todos')
        
        for text, value in [
            ('Todos', 'todos'),
            ('En Proceso', 'en_proceso'),
            ('Aprobados', 'aprobado'),
            ('Rechazados', 'rechazado')
        ]:
            ttk.Radiobutton(
                toolbar,
                text=text,
                value=value,
                variable=self.filter_var,
                command=self.load_proyectos
            ).pack(side=tk.LEFT, padx=10)
        
        # Projects container with scrollbar
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(container, bg='#f6f8fa')
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.projects_frame = ttk.Frame(self.canvas, style='Projects.TFrame')
        self.projects_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )
        
        self.canvas.create_window((0,0), window=self.projects_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_proyectos(self):
        try:
            # Clear existing projects
            for widget in self.projects_frame.winfo_children():
                widget.destroy()
            
            # Build query based on filter
            filter_value = self.filter_var.get()
            query = """
                SELECT p.*, COUNT(pe.id_estudiante) as num_estudiantes
                FROM proyectos p
                LEFT JOIN proyecto_estudiantes pe ON p.id_proyecto = pe.id_proyecto
                WHERE p.id_profesor_responsable = %s
            """
            
            params = [self.profesor_id]
            
            if filter_value != 'todos':
                query += " AND p.estado = %s"
                params.append(filter_value)
                
            query += " GROUP BY p.id_proyecto ORDER BY p.fecha_creacion DESC"
            
            proyectos = self.db.execute_query(query, tuple(params), fetch_all=True)
            
            for proyecto in proyectos:
                card = ProyectoCard(
                    self.projects_frame,
                    proyecto,
                    self.aprobar_proyecto,
                    self.rechazar_proyecto,
                    self.comentar_proyecto
                )
                card.pack(fill=tk.X, padx=10, pady=5)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {str(e)}")

    def aprobar_proyecto(self, proyecto_id):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea aprobar este proyecto?"):
            try:
                self.db.execute_query(
                    "UPDATE proyectos SET estado = 'aprobado' WHERE id_proyecto = %s",
                    (proyecto_id,),
                    commit=True
                )
                messagebox.showinfo("Éxito", "Proyecto aprobado correctamente")
                self.load_proyectos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al aprobar proyecto: {str(e)}")

    def rechazar_proyecto(self, proyecto_id):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea rechazar este proyecto?"):
            try:
                self.db.execute_query(
                    "UPDATE proyectos SET estado = 'rechazado' WHERE id_proyecto = %s",
                    (proyecto_id,),
                    commit=True
                )
                messagebox.showinfo("Éxito", "Proyecto rechazado correctamente")
                self.load_proyectos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al rechazar proyecto: {str(e)}")

    def comentar_proyecto(self, proyecto_id):
        comentario = tk.Toplevel(self.app.root)
        comentario.title("Comentar Proyecto")
        comentario.geometry("400x300")
        
        ttk.Label(
            comentario,
            text="Añadir Comentario",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        texto = tk.Text(comentario, height=10)
        texto.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        def guardar_comentario():
            contenido = texto.get("1.0", tk.END).strip()
            if contenido:
                try:
                    self.db.execute_query(
                        """
                        INSERT INTO comentarios_proyecto 
                        (id_proyecto, id_profesor, comentario, fecha)
                        VALUES (%s, %s, %s, NOW())
                        """,
                        (proyecto_id, self.profesor_id, contenido),
                        commit=True
                    )
                    messagebox.showinfo("Éxito", "Comentario guardado correctamente")
                    comentario.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al guardar comentario: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "El comentario no puede estar vacío")
        
        ttk.Button(
            comentario,
            text="Guardar Comentario",
            command=guardar_comentario
        ).pack(pady=10)

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

    def logout(self):
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.app.logout()