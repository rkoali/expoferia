import tkinter as tk
from tkinter import ttk, messagebox
from utils.pdf_generator import PDFGenerator
from utils.csv_generator import CSVGenerator
from database.database_connection import DatabaseConnection
from config import DB_CONFIG

class ReportesWindow:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("Generador de Reportes")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(main_frame, text="Generador de Reportes", style='Title.TLabel').pack(pady=10)
        
        # Frame para selección de reporte
        report_frame = ttk.LabelFrame(main_frame, text="Seleccionar Reporte", padding=10)
        report_frame.pack(fill=tk.X, pady=10)
        
        self.reporte_var = tk.StringVar()
        reportes = [
            ("Proyectos por docente", "proyectos_docente"),
            ("Estudiantes participantes", "estudiantes_participantes"),
            ("Proyectos por área", "proyectos_area"),
            ("Estudiantes por proyecto", "estudiantes_proyecto")
        ]
        
        for text, mode in reportes:
            ttk.Radiobutton(
                report_frame, 
                text=text, 
                variable=self.reporte_var,
                value=mode
            ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Frame para parámetros
        self.param_frame = ttk.LabelFrame(main_frame, text="Parámetros", padding=10)
        self.param_frame.pack(fill=tk.X, pady=10)
        
        # Frame para formato de salida
        format_frame = ttk.LabelFrame(main_frame, text="Formato de Salida", padding=10)
        format_frame.pack(fill=tk.X, pady=10)
        
        self.format_var = tk.StringVar(value="pdf")
        ttk.Radiobutton(format_frame, text="PDF", variable=self.format_var, value="pdf").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(format_frame, text="CSV", variable=self.format_var, value="csv").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(format_frame, text="Ambos", variable=self.format_var, value="ambos").pack(side=tk.LEFT, padx=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Generar Reporte", command=self.generar_reporte).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=10)
        
        # Configurar parámetros dinámicos
        self.reporte_var.trace('w', self.actualizar_parametros)
        self.reporte_var.set("proyectos_docente")
        
    def actualizar_parametros(self, *args):
        # Limpiar frame de parámetros
        for widget in self.param_frame.winfo_children():
            widget.destroy()
            
        tipo_reporte = self.reporte_var.get()
        
        if tipo_reporte == "proyectos_docente":
            ttk.Label(self.param_frame, text="ID del Profesor:").pack(anchor=tk.W, padx=5, pady=2)
            self.param_entry = ttk.Entry(self.param_frame)
            self.param_entry.pack(fill=tk.X, padx=5, pady=5)
            
        elif tipo_reporte == "estudiantes_proyecto":
            ttk.Label(self.param_frame, text="ID del Proyecto:").pack(anchor=tk.W, padx=5, pady=2)
            self.param_entry = ttk.Entry(self.param_frame)
            self.param_entry.pack(fill=tk.X, padx=5, pady=5)
            
        elif tipo_reporte == "proyectos_area":
            ttk.Label(self.param_frame, text="Área de Conocimiento:").pack(anchor=tk.W, padx=5, pady=2)
            self.param_entry = ttk.Entry(self.param_frame)
            self.param_entry.pack(fill=tk.X, padx=5, pady=5)
            
    def generar_reporte(self):
        tipo_reporte = self.reporte_var.get()
        formato = self.format_var.get()
        
        try:
            if tipo_reporte == "proyectos_docente":
                profesor_id = int(self.param_entry.get())
                self.generar_reporte_proyectos_docente(profesor_id, formato)
                
            elif tipo_reporte == "estudiantes_participantes":
                self.generar_reporte_estudiantes_participantes(formato)
                
            elif tipo_reporte == "proyectos_area":
                area = self.param_entry.get()
                self.generar_reporte_proyectos_area(area, formato)
                
            elif tipo_reporte == "estudiantes_proyecto":
                proyecto_id = int(self.param_entry.get())
                self.generar_reporte_estudiantes_proyecto(proyecto_id, formato)
                
            messagebox.showinfo("Éxito", "Reporte generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            
    def generar_reporte_proyectos_docente(self, profesor_id, formato):
        query = """
        SELECT p.id_proyecto, p.titulo, p.estado, p.fecha_creacion, 
               COUNT(pe.id_estudiante) as num_estudiantes
        FROM proyectos p
        LEFT JOIN proyecto_estudiantes pe ON p.id_proyecto = pe.id_proyecto
        WHERE p.id_profesor_responsable = %s
        GROUP BY p.id_proyecto
        """
        resultados = self.db.execute_query(query, (profesor_id,), fetch_all=True)
        
        if formato in ["pdf", "ambos"]:
            pdf = PDFGenerator()
            pdf.generar_reporte_proyectos(
                resultados,
                f"reporte_proyectos_docente_{profesor_id}.pdf"
            )
            
        if formato in ["csv", "ambos"]:
            csv = CSVGenerator()
            csv.generar_reporte_proyectos(
                resultados,
                f"reporte_proyectos_docente_{profesor_id}.csv"
            )
    
    def generar_reporte_estudiantes_participantes(self, formato):
        query = """
        SELECT e.id_estudiante, u.nombre, u.apellido, e.carrera, e.semestre,
               COUNT(pe.id_proyecto) as num_proyectos
        FROM estudiantes e
        JOIN usuarios u ON e.id_usuario = u.id_usuario
        LEFT JOIN proyecto_estudiantes pe ON e.id_estudiante = pe.id_estudiante
        GROUP BY e.id_estudiante
        """
        resultados = self.db.execute_query(query, fetch_all=True)
        
        if formato in ["pdf", "ambos"]:
            pdf = PDFGenerator()
            pdf.generar_reporte_estudiantes(
                resultados,
                "reporte_estudiantes_participantes.pdf"
            )
            
        if formato in ["csv", "ambos"]:
            csv = CSVGenerator()
            csv.generar_reporte_estudiantes(
                resultados,
                "reporte_estudiantes_participantes.csv"
            )
    
    def generar_reporte_proyectos_area(self, area, formato):
        query = """
        SELECT p.id_proyecto, p.titulo, p.estado, p.fecha_creacion,
               CONCAT(u.nombre, ' ', u.apellido) as profesor,
               COUNT(pe.id_estudiante) as num_estudiantes
        FROM proyectos p
        JOIN profesores pr ON p.id_profesor_responsable = pr.id_profesor
        JOIN usuarios u ON pr.id_usuario = u.id_usuario
        LEFT JOIN proyecto_estudiantes pe ON p.id_proyecto = pe.id_proyecto
        WHERE p.area_conocimiento = %s
        GROUP BY p.id_proyecto
        """
        resultados = self.db.execute_query(query, (area,), fetch_all=True)
        
        if formato in ["pdf", "ambos"]:
            pdf = PDFGenerator()
            pdf.generar_reporte_proyectos(
                resultados,
                f"reporte_proyectos_area_{area}.pdf"
            )
            
        if formato in ["csv", "ambos"]:
            csv = CSVGenerator()
            csv.generar_reporte_proyectos(
                resultados,
                f"reporte_proyectos_area_{area}.csv"
            )
    
    def generar_reporte_estudiantes_proyecto(self, proyecto_id, formato):
        query = """
        SELECT e.id_estudiante, u.nombre, u.apellido, e.carrera, e.semestre,
               pe.rol_en_proyecto, pe.fecha_incorporacion
        FROM proyecto_estudiantes pe
        JOIN estudiantes e ON pe.id_estudiante = e.id_estudiante
        JOIN usuarios u ON e.id_usuario = u.id_usuario
        WHERE pe.id_proyecto = %s
        """
        resultados = self.db.execute_query(query, (proyecto_id,), fetch_all=True)
        
        if formato in ["pdf", "ambos"]:
            pdf = PDFGenerator()
            pdf.generar_reporte_estudiantes_proyecto(
                resultados,
                f"reporte_estudiantes_proyecto_{proyecto_id}.pdf"
            )
            
        if formato in ["csv", "ambos"]:
            csv = CSVGenerator()
            csv.generar_reporte_estudiantes_proyecto(
                resultados,
                f"reporte_estudiantes_proyecto_{proyecto_id}.csv"
            )