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
        self.window.title("Inicio de Sesión")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.grab_set()  # Hacer modal
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Título
        ttk.Label(main_frame, text="Inicio de Sesión", style='Title.TLabel').pack(pady=10)
        
        # Formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20, expand=True)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Ingresar", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Centrar ventana
        self.center_window()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        try:
            # Obtener usuario de la base de datos
            query = "SELECT * FROM usuarios WHERE email = %s"
            usuario = self.db.execute_query(query, (email,), fetch_one=True)
            
            if not usuario:
                messagebox.showerror("Error", "Credenciales incorrectas")
                return
                
            # Verificar contraseña (en una implementación real usaríamos bcrypt o similar)
            hashed_password = sha256(password.encode()).hexdigest()
            # NOTA: En producción usar un método seguro como bcrypt o PBKDF2
            # Esto es solo para propósitos demostrativos
            
            if usuario['contraseña_hash'] == hashed_password:
                self.on_success(usuario)
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")