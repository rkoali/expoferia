import tkinter as tk
from tkinter import ttk, messagebox
from database.database_connection import DatabaseConnection
from views.auth_view import LoginWindow
from config import DB_CONFIG, config

class ExpoferiaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(config['default'].APP_NAME)
        self.root.geometry("1200x700")
        self.root.configure(bg='#f8f9fa')
        
        # Configurar la conexión a la base de datos
        self.db = DatabaseConnection(**DB_CONFIG)
        
        # Estilo personalizado
        self.setup_styles()
        
        # Mostrar ventana de login
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores y fuentes
        style.configure('TFrame', background='#f8f9fa')
        style.configure('TLabel', background='#f8f9fa', font=('Helvetica', 10))
        style.configure('TButton', 
                       font=('Helvetica', 10), 
                       padding=10,
                       background='#4361ee',
                       foreground='white')
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        
        style.map('TButton',
                  foreground=[('active', 'white'), ('!active', 'white')],
                  background=[('active', '#364fc7'), ('!active', '#4361ee')])
        
        style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#4361ee')])

    def show_login(self):
        LoginWindow(self.root, self.db, self.on_login_success)

    def on_login_success(self, usuario):
        self.usuario_actual = usuario
        
        # Mostrar la interfaz según el rol
        if usuario['rol'] == 'administrador':
            from views.admin_view import AdminDashboard
            self.dashboard = AdminDashboard(self, usuario)
        elif usuario['rol'] == 'profesor':
            from views.profesor_view import ProfesorDashboard
            self.dashboard = ProfesorDashboard(self, usuario)
        else:
            from views.estudiante_view import EstudianteDashboard
            self.dashboard = EstudianteDashboard(self, usuario)

    def logout(self):
        if hasattr(self, 'dashboard'):
            self.dashboard.destroy()
        self.usuario_actual = None
        self.show_login()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ExpoferiaApp()
    app.run()