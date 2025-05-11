import tkinter as tk
from tkinter import ttk, messagebox
from hashlib import sha256
import os

class LoginWindow:
    def __init__(self, root, db, on_success_callback):
        self.root = root
        self.db = db
        self.on_success = on_success_callback
        
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Configure root window
        self.root.title("Expoferia - Iniciar Sesión")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#ffffff')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with two columns
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Left column (login form)
        left_frame = ttk.Frame(main_container, style='Left.TFrame')
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Center the login form
        form_container = ttk.Frame(left_frame, style='Form.TFrame')
        form_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo and branding
        ttk.Label(
            form_container,
            text="Expoferia",
            style='Logo.TLabel'
        ).pack(anchor=tk.CENTER, pady=(0, 10))
        
        ttk.Label(
            form_container,
            text="Inicia sesión para continuar",
            style='Subtitle.TLabel'
        ).pack(anchor=tk.CENTER, pady=(0, 40))
        
        # Login form
        form_frame = ttk.Frame(form_container, style='Form.TFrame')
        form_frame.pack(fill=tk.X, pady=20)
        
        # Email field
        self.email_var = tk.StringVar()
        email_frame = self.create_input_field(
            form_frame,
            "Email",
            self.email_var,
            'example@email.com'
        )
        email_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Password field
        self.password_var = tk.StringVar()
        password_frame = self.create_input_field(
            form_frame,
            "Contraseña",
            self.password_var,
            '••••••••',
            True
        )
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Remember me checkbox
        remember_frame = ttk.Frame(form_frame, style='Form.TFrame')
        remember_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(
            remember_frame,
            text="Recordarme",
            variable=self.remember_var,
            style='Modern.TCheckbutton'
        ).pack(side=tk.LEFT)
        
        # Login button
        login_button = tk.Button(
            form_frame,
            text="Iniciar Sesión",
            command=self.login,
            font=('Helvetica', 12, 'bold'),
            bg='#4361ee',
            fg='white',
            activebackground='#364fc7',
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            pady=12
        )
        login_button.pack(fill=tk.X, pady=(0, 20))
        
        # Add hover effect
        login_button.bind('<Enter>', lambda e: login_button.configure(bg='#364fc7'))
        login_button.bind('<Leave>', lambda e: login_button.configure(bg='#4361ee'))
        
        # Register link
        register_frame = ttk.Frame(form_frame, style='Form.TFrame')
        register_frame.pack(fill=tk.X)
        
        ttk.Label(
            register_frame,
            text="¿No tienes una cuenta?",
            style='Link.TLabel'
        ).pack(side=tk.LEFT)
        
        register_link = ttk.Label(
            register_frame,
            text="Regístrate",
            style='LinkButton.TLabel',
            cursor='hand2'
        )
        register_link.pack(side=tk.LEFT, padx=5)
        register_link.bind('<Button-1>', lambda e: self.show_register())
        
        # Right column (decorative gradient)
        right_frame = ttk.Frame(main_container, style='Right.TFrame')
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        canvas = tk.Canvas(
            right_frame,
            width=600,
            height=700,
            highlightthickness=0
        )
        canvas.pack(expand=True, fill=tk.BOTH)
        
        # Create modern gradient effect
        self.create_gradient(canvas)
        
    def create_input_field(self, parent, label_text, var, placeholder, is_password=False):
        frame = ttk.Frame(parent, style='Form.TFrame')
        
        ttk.Label(
            frame,
            text=label_text,
            style='InputLabel.TLabel'
        ).pack(anchor=tk.W)
        
        entry = ttk.Entry(
            frame,
            textvariable=var,
            font=('Helvetica', 12),
            style='Modern.TEntry'
        )
        
        if is_password:
            entry.configure(show="•")
            
        entry.pack(fill=tk.X, pady=(5, 0))
        
        # Add placeholder
        if not var.get():
            entry.insert(0, placeholder)
            entry.configure(foreground='#adb5bd')
            
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(foreground='#212529')
                if is_password:
                    entry.configure(show="•")
                    
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(foreground='#adb5bd')
                if is_password:
                    entry.configure(show="")
                    
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return frame
        
    def create_gradient(self, canvas):
        width = 600
        height = 700
        
        # Create base gradient
        for i in range(height):
            r = int(67 + (i/height)*30)
            g = int(97 + (i/height)*30)
            b = int(238 - (i/height)*30)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)
            
        # Add decorative circles
        for _ in range(10):
            x = width * 0.2 + (width * 0.6 * ((_ * 127) % 100) / 100)
            y = height * 0.2 + (height * 0.6 * ((_ * 163) % 100) / 100)
            size = 20 + (_ * 17) % 40
            
            canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill='#ffffff',
                stipple='gray50',
                width=0
            )
        
    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        # Check for placeholder text
        if email == 'example@email.com':
            email = ''
        if password == '••••••••':
            password = ''
        
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