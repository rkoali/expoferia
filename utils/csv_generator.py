import csv
from datetime import datetime

class CSVGenerator:
    def generar_reporte_proyectos(self, proyectos, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Título', 'Estado', 'Fecha Creación', 'Núm. Estudiantes'])
            
            for proyecto in proyectos:
                writer.writerow([
                    proyecto['id_proyecto'],
                    proyecto['titulo'],
                    proyecto['estado'],
                    proyecto['fecha_creacion'],
                    proyecto['num_estudiantes']
                ])
    
    def generar_reporte_estudiantes(self, estudiantes, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nombre', 'Apellido', 'Carrera', 'Semestre', 'Núm. Proyectos'])
            
            for estudiante in estudiantes:
                writer.writerow([
                    estudiante['id_estudiante'],
                    estudiante['nombre'],
                    estudiante['apellido'],
                    estudiante['carrera'],
                    estudiante['semestre'],
                    estudiante['num_proyectos']
                ])
    
    def generar_reporte_estudiantes_proyecto(self, estudiantes, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nombre', 'Apellido', 'Carrera', 'Rol en Proyecto', 'Fecha Incorporación'])
            
            for estudiante in estudiantes:
                writer.writerow([
                    estudiante['id_estudiante'],
                    estudiante['nombre'],
                    estudiante['apellido'],
                    estudiante['carrera'],
                    estudiante['rol_en_proyecto'],
                    estudiante['fecha_incorporacion']
                ])