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
        self.root.configure(bg='#f0f0f0')
        
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
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        style.map('TButton',
                  foreground=[('active', 'black'), ('!active', 'black')],
                  background=[('active', '#d9d9d9'), ('!active', '#e6e6e6')])
        
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#4a6984')])

    def show_login(self):
        LoginWindow(self.root, self.db, self.on_login_success)

    def on_login_success(self, usuario):
        self.usuario_actual = usuario
        self.root.withdraw()  # Ocultar la ventana principal temporalmente
        
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
        self.root.deiconify()  # Mostrar nuevamente la ventana principal
        self.show_login()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ExpoferiaApp()
    app.run()