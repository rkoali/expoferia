import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from models.profesor import Profesor
from models.estudiante import Estudiante

class UsuarioEditForm:
    def __init__(self, parent, db, usuario_id, on_save_callback=None):
        self.parent = parent
        self.db = db
        self.usuario_id = usuario_id
        self.on_save = on_save_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Editar Usuario")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.usuario_model = Usuario(db)
        self.profesor_model = Profesor(db)
        self.estudiante_model = Estudiante(db)
        
        # Obtener datos del usuario
        self.usuario = self.usuario_model.obtener_usuario_por_id(usuario_id)
        if not self.usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            self.window.destroy()
            return
            
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(main_frame, text="Editar Usuario", style='Title.TLabel').pack(pady=5)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10, fill=tk.X)
        
        # Campos básicos
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.nombre_entry = ttk.Entry(form_frame, width=40)
        self.nombre_entry.insert(0, self.usuario['nombre'])
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.apellido_entry = ttk.Entry(form_frame, width=40)
        self.apellido_entry.insert(0, self.usuario['apellido'])
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.insert(0, self.usuario['email'])
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Rol:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.rol_label = ttk.Label(form_frame, text=self.usuario['rol'], width=37)
        self.rol_label.grid(row=3, column=1, padx=5, pady=5)
        
        # Campos específicos de rol
        self.rol_fields_frame = ttk.Frame(main_frame)
        self.rol_fields_frame.pack(fill=tk.X, pady=10)
        
        if self.usuario['rol'] == 'profesor':
            profesor = self.profesor_model.obtener_profesor_por_usuario(self.usuario_id)
            if profesor:
                ttk.Label(self.rol_fields_frame, text="Departamento:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
                self.departamento_entry = ttk.Entry(self.rol_fields_frame, width=40)
                self.departamento_entry.insert(0, profesor['departamento'])
                self.departamento_entry.grid(row=0, column=1, padx=5, pady=5)
                
                ttk.Label(self.rol_fields_frame, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
                self.telefono_entry = ttk.Entry(self.rol_fields_frame, width=40)
                self.telefono_entry.insert(0, profesor['telefono'] or "")
                self.telefono_entry.grid(row=1, column=1, padx=5, pady=5)
                
        elif self.usuario['rol'] == 'estudiante':
            estudiante = self.estudiante_model.obtener_estudiante_por_usuario(self.usuario_id)
            if estudiante:
                ttk.Label(self.rol_fields_frame, text="Carrera:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
                self.carrera_entry = ttk.Entry(self.rol_fields_frame, width=40)
                self.carrera_entry.insert(0, estudiante['carrera'])
                self.carrera_entry.grid(row=0, column=1, padx=5, pady=5)
                
                ttk.Label(self.rol_fields_frame, text="Semestre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
                self.semestre_entry = ttk.Entry(self.rol_fields_frame, width=40)
                self.semestre_entry.insert(0, str(estudiante['semestre']))
                self.semestre_entry.grid(row=1, column=1, padx=5, pady=5)
                
                ttk.Label(self.rol_fields_frame, text="Matrícula:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
                self.matricula_entry = ttk.Entry(self.rol_fields_frame, width=40)
                self.matricula_entry.insert(0, estudiante['matricula'])
                self.matricula_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guardar Cambios", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
    def guardar(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        email = self.email_entry.get()
        
        # Validaciones básicas
        if not all([nombre, apellido, email]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        try:
            # Actualizar usuario
            self.usuario_model.actualizar_usuario(
                usuario_id=self.usuario_id,
                nombre=nombre,
                apellido=apellido,
                email=email
            )
            
            # Actualizar registro específico según rol
            if self.usuario['rol'] == 'profesor':
                departamento = self.departamento_entry.get()
                telefono = self.telefono_entry.get()
                
                if not departamento:
                    messagebox.showerror("Error", "El departamento es obligatorio")
                    return
                    
                self.profesor_model.actualizar_profesor(
                    usuario_id=self.usuario_id,
                    departamento=departamento,
                    telefono=telefono
                )
                
            elif self.usuario['rol'] == 'estudiante':
                carrera = self.carrera_entry.get()
                semestre = self.semestre_entry.get()
                matricula = self.matricula_entry.get()
                
                if not all([carrera, semestre, matricula]):
                    messagebox.showerror("Error", "Todos los campos de estudiante son obligatorios")
                    return
                    
                self.estudiante_model.actualizar_estudiante(
                    usuario_id=self.usuario_id,
                    carrera=carrera,
                    semestre=int(semestre),
                    matricula=matricula
                )
            
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            
            if self.on_save:
                self.on_save()
                
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {str(e)}")