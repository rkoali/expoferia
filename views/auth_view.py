import tkinter as tk
from tkinter import ttk, messagebox
from hashlib import sha256
import os

class LoginWindow:
    def __init__(self, root, db, on_success_callback):
        self.root = root
        self.db = db
        self.on_success = on_success_callback
        
        self.window = tk.Toplevel(root)
        self.window.title("Expoferia - Iniciar Sesión")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        # Configurar el color de fondo
        self.window.configure(bg='#f0f2f5')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal con diseño de dos columnas
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Frame izquierdo (formulario)
        left_frame = ttk.Frame(main_frame, padding=40)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Logo y título
        ttk.Label(
            left_frame, 
            text="Expoferia", 
            font=('Helvetica', 24, 'bold'),
            foreground='#1a73e8'
        ).pack(pady=(0, 20))
        
        ttk.Label(
            left_frame,
            text="Inicia sesión para continuar",
            font=('Helvetica', 14),
            foreground='#5f6368'
        ).pack(pady=(0, 30))
        
        # Frame del formulario
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill=tk.X, pady=20)
        
        # Estilo personalizado para los campos
        style = ttk.Style()
        style.configure(
            'Custom.TEntry',
            fieldbackground='white',
            borderwidth=1,
            relief='solid'
        )
        
        # Campo de email
        self.email_var = tk.StringVar()
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            email_frame,
            text="Email",
            font=('Helvetica', 10),
            foreground='#5f6368'
        ).pack(anchor=tk.W)
        
        self.email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            width=40,
            style='Custom.TEntry'
        )
        self.email_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Campo de contraseña
        self.password_var = tk.StringVar()
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            password_frame,
            text="Contraseña",
            font=('Helvetica', 10),
            foreground='#5f6368'
        ).pack(anchor=tk.W)
        
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="•",
            width=40,
            style='Custom.TEntry'
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Checkbox "Recordarme"
        self.remember_var = tk.BooleanVar()
        remember_frame = ttk.Frame(form_frame)
        remember_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(
            remember_frame,
            text="Recordarme",
            variable=self.remember_var
        ).pack(side=tk.LEFT)
        
        # Botón de inicio de sesión
        button_style = ttk.Style()
        button_style.configure(
            'Custom.TButton',
            background='#1a73e8',
            foreground='white',
            padding=10
        )
        
        ttk.Button(
            form_frame,
            text="Iniciar Sesión",
            style='Custom.TButton',
            command=self.login
        ).pack(fill=tk.X, pady=20)
        
        # Enlace para registro
        register_frame = ttk.Frame(form_frame)
        register_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            register_frame,
            text="¿No tienes una cuenta?",
            foreground='#5f6368'
        ).pack(side=tk.LEFT)
        
        register_link = ttk.Label(
            register_frame,
            text="Regístrate",
            foreground='#1a73e8',
            cursor='hand2'
        )
        register_link.pack(side=tk.LEFT, padx=5)
        register_link.bind('<Button-1>', lambda e: self.show_register())
        
        # Frame derecho (imagen decorativa)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # Aquí podrías agregar una imagen decorativa
        # Por ahora usamos un degradado simple
        canvas = tk.Canvas(
            right_frame,
            width=400,
            height=600,
            bg='#e8f0fe',
            highlightthickness=0
        )
        canvas.pack(expand=True, fill=tk.BOTH)
        
        # Crear un degradado simple
        for i in range(600):
            color = '#{:02x}{:02x}{:02x}'.format(
                int(232 - (i/600)*50),
                int(240 - (i/600)*50),
                int(254 - (i/600)*50)
            )
            canvas.create_line(0, i, 400, i, fill=color)
        
        self.center_window()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror(
                "Error",
                "Por favor complete todos los campos",
                parent=self.window
            )
            return
            
        try:
            query = "SELECT * FROM usuarios WHERE email = %s"
            usuario = self.db.execute_query(query, (email,), fetch_one=True)
            
            if not usuario:
                messagebox.showerror(
                    "Error",
                    "Credenciales incorrectas",
                    parent=self.window
                )
                return
                
            hashed_password = sha256(password.encode()).hexdigest()
            
            if usuario['contraseña_hash'] == hashed_password:
                if self.remember_var.get():
                    # Aquí implementaríamos la lógica para recordar al usuario
                    pass
                    
                self.on_success(usuario)
                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Credenciales incorrectas",
                    parent=self.window
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al iniciar sesión: {str(e)}",
                parent=self.window
            )
    
    def show_register(self):
        self.window.destroy()
        from views.usuario_form import UsuarioForm
        UsuarioForm(self.root, self.db)