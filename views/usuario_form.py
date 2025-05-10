import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from models.profesor import Profesor
from models.estudiante import Estudiante

class UsuarioForm:
    def __init__(self, parent, db, on_save_callback=None):
        self.parent = parent
        self.db = db
        self.on_save = on_save_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Usuario")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.usuario_model = Usuario(db)
        self.profesor_model = Profesor(db)
        self.estudiante_model = Estudiante(db)
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(main_frame, text="Nuevo Usuario", style='Title.TLabel').pack(pady=5)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, fill=tk.X)
        
        # Campos básicos
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.nombre_entry = ttk.Entry(form_frame, width=40)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.apellido_entry = ttk.Entry(form_frame, width=40)
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(form_frame, width=40, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Confirmar Contraseña:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.confirm_password_entry = ttk.Entry(form_frame, width=40, show="*")
        self.confirm_password_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Rol:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.rol_combo = ttk.Combobox(form_frame, values=['administrador', 'profesor', 'estudiante'], width=37)
        self.rol_combo.grid(row=5, column=1, padx=5, pady=5)
        self.rol_combo.current(2)
        self.rol_combo.bind("<<ComboboxSelected>>", self._actualizar_campos_rol)
        
        # Frame para campos específicos de rol
        self.rol_fields_frame = ttk.Frame(main_frame)
        self.rol_fields_frame.pack(fill=tk.X, pady=10)
        self._actualizar_campos_rol()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
    def _actualizar_campos_rol(self, event=None):
        # Limpiar frame de campos de rol
        for widget in self.rol_fields_frame.winfo_children():
            widget.destroy()
        
        rol = self.rol_combo.get()
        
        if rol == 'profesor':
            ttk.Label(self.rol_fields_frame, text="Departamento:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
            self.departamento_entry = ttk.Entry(self.rol_fields_frame, width=40)
            self.departamento_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.rol_fields_frame, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
            self.telefono_entry = ttk.Entry(self.rol_fields_frame, width=40)
            self.telefono_entry.grid(row=1, column=1, padx=5, pady=5)
            
        elif rol == 'estudiante':
            ttk.Label(self.rol_fields_frame, text="Carrera:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
            self.carrera_entry = ttk.Entry(self.rol_fields_frame, width=40)
            self.carrera_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.rol_fields_frame, text="Semestre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
            self.semestre_entry = ttk.Entry(self.rol_fields_frame, width=40)
            self.semestre_entry.grid(row=1, column=1, padx=5, pady=5)
            
            ttk.Label(self.rol_fields_frame, text="Matrícula:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
            self.matricula_entry = ttk.Entry(self.rol_fields_frame, width=40)
            self.matricula_entry.grid(row=2, column=1, padx=5, pady=5)
        
    def guardar(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        rol = self.rol_combo.get()
        
        # Validaciones básicas
        if not all([nombre, apellido, email, password, confirm_password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        try:
            # Crear usuario
            usuario_id = self.usuario_model.crear_usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                password=password,
                rol=rol
            )
            
            # Crear registro específico según rol
            if rol == 'profesor':
                departamento = self.departamento_entry.get()
                telefono = self.telefono_entry.get()
                
                if not departamento:
                    messagebox.showerror("Error", "El departamento es obligatorio")
                    return
                    
                self.profesor_model.crear_profesor(
                    usuario_id=usuario_id,
                    departamento=departamento,
                    telefono=telefono
                )
                
            elif rol == 'estudiante':
                carrera = self.carrera_entry.get()
                semestre = self.semestre_entry.get()
                matricula = self.matricula_entry.get()
                
                if not all([carrera, semestre, matricula]):
                    messagebox.showerror("Error", "Todos los campos de estudiante son obligatorios")
                    return
                    
                self.estudiante_model.crear_estudiante(
                    usuario_id=usuario_id,
                    carrera=carrera,
                    semestre=int(semestre),
                    matricula=matricula
                )
            
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
            
            if self.on_save:
                self.on_save()
                
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")