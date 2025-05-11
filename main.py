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
        self.root.configure(bg='#ffffff')
        
        # Configurar la conexión a la base de datos
        self.db = DatabaseConnection(**DB_CONFIG)
        
        # Estilo personalizado
        self.setup_styles()
        
        # Mostrar ventana de login
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos generales
        style.configure('Main.TFrame', background='#ffffff')
        style.configure('Left.TFrame', background='#ffffff')
        style.configure('Right.TFrame', background='#ffffff')
        style.configure('Form.TFrame', background='#ffffff')
        
        # Estilos de texto
        style.configure('Logo.TLabel',
                       font=('Helvetica', 32, 'bold'),
                       foreground='#4361ee',
                       background='#ffffff')
                       
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 16),
                       foreground='#6c757d',
                       background='#ffffff')
                       
        style.configure('InputLabel.TLabel',
                       font=('Helvetica', 12),
                       foreground='#495057',
                       background='#ffffff')
                       
        style.configure('Link.TLabel',
                       font=('Helvetica', 12),
                       foreground='#6c757d',
                       background='#ffffff')
                       
        style.configure('LinkButton.TLabel',
                       font=('Helvetica', 12),
                       foreground='#4361ee',
                       background='#ffffff')
        
        # Estilos de entrada
        style.configure('Modern.TEntry',
                       fieldbackground='#ffffff',
                       borderwidth=1,
                       relief='solid',
                       padding=10)
        
        # Estilos de checkbox
        style.configure('Modern.TCheckbutton',
                       font=('Helvetica', 12),
                       background='#ffffff')
        
        # Estilos para la vista de datos
        style.configure('Treeview',
                       font=('Helvetica', 10),
                       rowheight=25,
                       background='#ffffff',
                       fieldbackground='#ffffff')
                       
        style.configure('Treeview.Heading',
                       font=('Helvetica', 10, 'bold'))
                       
        style.map('Treeview',
                 background=[('selected', '#4361ee')])

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