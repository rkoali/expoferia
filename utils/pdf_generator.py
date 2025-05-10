from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
    def generate_pdf_report(self, data, report_type, filename):
        """Función unificada para generar diferentes tipos de reportes PDF"""
        if report_type == "proyectos_docente":
            self._generate_projects_report(data, filename)
        elif report_type == "estudiantes_participantes":
            self._generate_students_report(data, filename)
        elif report_type == "estudiantes_proyecto":
            self._generate_project_students_report(data, filename)
        else:
            raise ValueError(f"Tipo de reporte no soportado: {report_type}")

    def _generate_projects_report(self, proyectos, filename):
        self.pdf.add_page()
        self._add_header("Reporte de Proyectos por Docente")
        
        # Encabezados de tabla
        self.pdf.set_font('Arial', 'B', 12)
        self._add_table_row(['ID', 'Título', 'Estado', 'Fecha', 'Estudiantes'], header=True)
        
        # Datos
        self.pdf.set_font('Arial', '', 10)
        for proyecto in proyectos:
            self._add_table_row([
                str(proyecto['id_proyecto']),
                proyecto['titulo'],
                proyecto['estado'],
                str(proyecto['fecha_creacion']),
                str(proyecto.get('num_estudiantes', 0))
            ])
            
        self.pdf.output(filename)

    def _generate_students_report(self, estudiantes, filename):
        self.pdf.add_page()
        self._add_header("Reporte de Estudiantes Participantes")
        
        # Encabezados de tabla
        self.pdf.set_font('Arial', 'B', 12)
        self._add_table_row(['ID', 'Nombre', 'Carrera', 'Semestre', 'Proyectos'], header=True)
        
        # Datos
        self.pdf.set_font('Arial', '', 10)
        for estudiante in estudiantes:
            self._add_table_row([
                str(estudiante['id_estudiante']),
                f"{estudiante['nombre']} {estudiante['apellido']}",
                estudiante['carrera'],
                str(estudiante['semestre']),
                str(estudiante.get('num_proyectos', 0))
            ])
            
        self.pdf.output(filename)

    def _generate_project_students_report(self, estudiantes, filename):
        self.pdf.add_page()
        self._add_header("Reporte de Estudiantes por Proyecto")
        
        # Encabezados de tabla
        self.pdf.set_font('Arial', 'B', 12)
        self._add_table_row(['ID', 'Nombre', 'Carrera', 'Rol', 'Incorporación'], header=True)
        
        # Datos
        self.pdf.set_font('Arial', '', 10)
        for estudiante in estudiantes:
            self._add_table_row([
                str(estudiante['id_estudiante']),
                f"{estudiante['nombre']} {estudiante['apellido']}",
                estudiante['carrera'],
                estudiante['rol_en_proyecto'],
                str(estudiante['fecha_incorporacion'])
            ])
            
        self.pdf.output(filename)

    def _add_header(self, title):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, title, 0, 1, 'C')
        self.pdf.ln(10)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, f'Generado el: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1)
        self.pdf.ln(10)

    def _add_table_row(self, data, header=False, col_widths=None):
        if col_widths is None:
            col_widths = [20, 60, 50, 30, 30]  # Valores por defecto
        
        for i, item in enumerate(data):
            if i < len(col_widths):
                width = col_widths[i]
            else:
                width = 40  # Ancho por defecto si no hay suficiente configuración
            
            if header:
                self.pdf.set_fill_color(200, 220, 255)
                self.pdf.cell(width, 10, str(item), 1, 0, 'C', 1)
            else:
                self.pdf.cell(width, 10, str(item), 1)
        self.pdf.ln()

# Función de conveniencia para compatibilidad con código existente
def generate_pdf_report(data, report_type, filename):
    generator = PDFGenerator()
    generator.generate_pdf_report(data, report_type, filename)