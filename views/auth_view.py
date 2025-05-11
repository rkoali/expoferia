import tkinter as tk
from tkinter import ttk, messagebox
from hashlib import sha256
import os

class LoginWindow:
    def __init__(self, root, db, on_success_callback):
        self.root = root
        self.db = db
        self.on_success = on_success_callback
        
        # Configure root window instead of creating a new one
        self.root.title("Expoferia - Iniciar Sesión")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # Configure the color scheme
        self.root.configure(bg='#f8f9fa')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with two columns
        main_container = ttk.Frame(self.root)
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Left column (login form)
        left_frame = ttk.Frame(main_container, padding=40)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Logo and branding
        logo_frame = ttk.Frame(left_frame)
        logo_frame.pack(fill=tk.X, pady=(0, 40))
        
        ttk.Label(
            logo_frame,
            text="Expoferia",
            font=('Helvetica', 32, 'bold'),
            foreground='#4361ee'
        ).pack(anchor=tk.W)
        
        ttk.Label(
            logo_frame,
            text="Inicia sesión para continuar",
            font=('Helvetica', 16),
            foreground='#6c757d'
        ).pack(anchor=tk.W)
        
        # Login form
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill=tk.X, pady=20)
        
        # Email field
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            email_frame,
            text="Email",
            font=('Helvetica', 12),
            foreground='#495057'
        ).pack(anchor=tk.W)
        
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            font=('Helvetica', 12),
            width=40
        )
        email_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Password field
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            password_frame,
            text="Contraseña",
            font=('Helvetica', 12),
            foreground='#495057'
        ).pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="•",
            font=('Helvetica', 12),
            width=40
        )
        password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Remember me checkbox
        remember_frame = ttk.Frame(form_frame)
        remember_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(
            remember_frame,
            text="Recordarme",
            variable=self.remember_var,
            style='Modern.TCheckbutton'
        ).pack(side=tk.LEFT)
        
        # Login button
        style = ttk.Style()
        style.configure(
            'Modern.TButton',
            font=('Helvetica', 12),
            padding=10
        )
        
        ttk.Button(
            form_frame,
            text="Iniciar Sesión",
            style='Modern.TButton',
            command=self.login
        ).pack(fill=tk.X, pady=(0, 20))
        
        # Register link
        register_frame = ttk.Frame(form_frame)
        register_frame.pack(fill=tk.X)
        
        ttk.Label(
            register_frame,
            text="¿No tienes una cuenta?",
            font=('Helvetica', 12),
            foreground='#6c757d'
        ).pack(side=tk.LEFT)
        
        register_link = ttk.Label(
            register_frame,
            text="Regístrate",
            font=('Helvetica', 12),
            foreground='#4361ee',
            cursor='hand2'
        )
        register_link.pack(side=tk.LEFT, padx=5)
        register_link.bind('<Button-1>', lambda e: self.show_register())
        
        # Right column (decorative)
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # Create decorative gradient canvas
        canvas = tk.Canvas(
            right_frame,
            width=600,
            height=700,
            highlightthickness=0,
            bg='#4361ee'
        )
        canvas.pack(expand=True, fill=tk.BOTH)
        
        # Create gradient effect
        for i in range(700):
            color = '#{:02x}{:02x}{:02x}'.format(
                int(67 + (i/700)*30),
                int(97 + (i/700)*30),
                int(238 - (i/700)*30)
            )
            canvas.create_line(0, i, 600, i, fill=color)
        
        # Configure styles
        style = ttk.Style()
        style.configure('Modern.TCheckbutton', font=('Helvetica', 12))
        style.configure('TEntry', padding=10)
        
        # Set initial focus
        email_entry.focus_set()
        
    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror(
                "Error",
                "Por favor complete todos los campos",
                parent=self.root
            )
            return
            
        try:
            query = "SELECT * FROM usuarios WHERE email = %s"
            usuario = self.db.execute_query(query, (email,), fetch_one=True)
            
            if not usuario:
                messagebox.showerror(
                    "Error",
                    "Credenciales incorrectas",
                    parent=self.root
                )
                return
                
            hashed_password = sha256(password.encode()).hexdigest()
            
            if usuario['contraseña_hash'] == hashed_password:
                if self.remember_var.get():
                    # Implementar lógica para recordar usuario
                    pass
                    
                self.on_success(usuario)
            else:
                messagebox.showerror(
                    "Error",
                    "Credenciales incorrectas",
                    parent=self.root
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al iniciar sesión: {str(e)}",
                parent=self.root
            )
    
    def show_register(self):
        from views.usuario_form import UsuarioForm
        UsuarioForm(self.root, self.db)