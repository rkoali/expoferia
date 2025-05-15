import mysql.connector
from mysql.connector import Error
import hashlib

class DatabaseCreator:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin"
            )
            self.cursor = self.connection.cursor()
            print("✓ Conexión a MySQL exitosa")
        except Error as e:
            print(f"✗ Error al conectar a MySQL: {e}")
            raise

    def create_database(self):
        try:
            # Crear la base de datos si no existe
            self.cursor.execute("DROP DATABASE IF EXISTS expoferia_db")
            self.cursor.execute("CREATE DATABASE expoferia_db")
            print("✓ Base de datos 'expoferia_db' creada")
            
            # Usar la base de datos
            self.cursor.execute("USE expoferia_db")
            print("✓ Usando base de datos 'expoferia_db'")
            
            # Crear todas las tablas
            self._create_tables()
            
            # Insertar datos iniciales
            self._insert_initial_data()
            
            print("✓ Base de datos configurada exitosamente")
            
        except Error as e:
            print(f"✗ Error al configurar la base de datos: {e}")
            raise
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("✓ Conexión a MySQL cerrada")

    def _create_tables(self):
        tables = [
            """
            CREATE TABLE usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellido VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                contraseña_hash VARCHAR(255) NOT NULL,
                rol ENUM('administrador', 'profesor', 'estudiante') NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE profesores (
                id_profesor INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT UNIQUE NOT NULL,
                departamento VARCHAR(50) NOT NULL,
                telefono VARCHAR(15),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE estudiantes (
                id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT UNIQUE NOT NULL,
                carrera VARCHAR(50) NOT NULL,
                semestre INT NOT NULL,
                matricula VARCHAR(20) UNIQUE NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE proyectos (
                id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(100) NOT NULL,
                descripcion TEXT,
                id_profesor_responsable INT NOT NULL,
                fecha_creacion DATE NOT NULL,
                estado ENUM('en_proceso', 'completado', 'aprobado', 'rechazado') DEFAULT 'en_proceso',
                area_conocimiento VARCHAR(50),
                FOREIGN KEY (id_profesor_responsable) REFERENCES profesores(id_profesor)
            )
            """,
            """
            CREATE TABLE proyecto_estudiantes (
                id_proyecto INT NOT NULL,
                id_estudiante INT NOT NULL,
                rol_en_proyecto VARCHAR(50) NOT NULL,
                fecha_incorporacion DATE NOT NULL,
                PRIMARY KEY (id_proyecto, id_estudiante),
                FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
                FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE comentarios_proyecto (
                id_comentario INT AUTO_INCREMENT PRIMARY KEY,
                id_proyecto INT NOT NULL,
                id_profesor INT NOT NULL,
                comentario TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
                FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE eventos (
                id_evento INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                fecha_inicio DATETIME NOT NULL,
                fecha_fin DATETIME NOT NULL,
                tipo ENUM('inscripcion', 'evaluacion', 'feria', 'reunion', 'otro') NOT NULL,
                ubicacion VARCHAR(100),
                responsable INT,
                FOREIGN KEY (responsable) REFERENCES profesores(id_profesor)
            )
            """,
            """
            CREATE TABLE reportes (
                id_reporte INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                descripcion TEXT,
                parametros TEXT,
                formato_salida ENUM('pdf', 'csv', 'ambos') DEFAULT 'pdf'
            )
            """,
            """
            CREATE TABLE log_actividad (
                id_log INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL,
                accion VARCHAR(50) NOT NULL,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                detalles TEXT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            )
            """,
            """
            CREATE TABLE configuraciones (
                id_config INT AUTO_INCREMENT PRIMARY KEY,
                clave VARCHAR(50) UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                descripcion TEXT
            )
            """
        ]
        
        print("\nCreando tablas...")
        for i, table in enumerate(tables, 1):
            try:
                self.cursor.execute(table)
                print(f"✓ Tabla {i} creada exitosamente")
            except Error as e:
                print(f"✗ Error al crear tabla {i}: {e}")
                raise

        # Crear procedimientos almacenados
        self._create_stored_procedures()

    def _create_stored_procedures(self):
        procedures = [
            """
            CREATE PROCEDURE cambiar_contrasena(
                IN p_id_usuario INT,
                IN p_nueva_contrasena VARCHAR(255))
            BEGIN
                DECLARE salt VARCHAR(64);
                DECLARE hashed_password VARCHAR(255);
                
                SET salt = SHA2(UUID(), 256);
                SET hashed_password = SHA2(CONCAT(salt, p_nueva_contrasena), 512);
                
                UPDATE usuarios 
                SET contraseña_hash = CONCAT(salt, hashed_password)
                WHERE id_usuario = p_id_usuario;
                
                INSERT INTO log_actividad (id_usuario, accion, detalles)
                VALUES (p_id_usuario, 'cambio_contrasena', 'Usuario cambió su contraseña');
            END
            """,
            """
            CREATE PROCEDURE generar_reporte_proyectos_docente(IN p_id_profesor INT)
            BEGIN
                SELECT 
                    p.id_proyecto,
                    p.titulo,
                    p.estado,
                    p.fecha_creacion,
                    COUNT(pe.id_estudiante) AS num_estudiantes
                FROM 
                    proyectos p
                LEFT JOIN 
                    proyecto_estudiantes pe ON p.id_proyecto = pe.id_proyecto
                WHERE 
                    p.id_profesor_responsable = p_id_profesor
                GROUP BY 
                    p.id_proyecto;
            END
            """
        ]
        
        print("\nCreando procedimientos almacenados...")
        for i, procedure in enumerate(procedures, 1):
            try:
                self.cursor.execute(procedure)
                print(f"✓ Procedimiento {i} creado exitosamente")
            except Error as e:
                print(f"✗ Error al crear procedimiento {i}: {e}")
                raise

    def _hash_password(self, password):
        """Genera un hash SHA-256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _insert_initial_data(self):
        print("\nInsertando datos iniciales...")
        
        try:
            # 1. Insertar usuarios primero
            usuarios = [
                ("Admin", "Sistema", "admin@expoferia.edu", self._hash_password("admin123"), "administrador"),
                ("Vivelib", "Rojas", "vrojas@expoferia.edu", self._hash_password("profesor123"), "profesor"),
                ("Carlos", "Mendoza", "cmendoza@expoferia.edu", self._hash_password("profesor456"), "profesor"),
                ("María", "González", "mgonzalez@expoferia.edu", self._hash_password("profesor789"), "profesor"),
                ("Estudiante1", "Apellido1", "est1@expoferia.edu", self._hash_password("estudiante1"), "estudiante"),
                ("Estudiante2", "Apellido2", "est2@expoferia.edu", self._hash_password("estudiante2"), "estudiante"),
                ("Estudiante3", "Apellido3", "est3@expoferia.edu", self._hash_password("estudiante3"), "estudiante"),
                ("Estudiante4", "Apellido4", "est4@expoferia.edu", self._hash_password("estudiante4"), "estudiante"),
                ("Estudiante5", "Apellido5", "est5@expoferia.edu", self._hash_password("estudiante5"), "estudiante"),
                ("Estudiante6", "Apellido6", "est6@expoferia.edu", self._hash_password("estudiante6"), "estudiante"),
                ("Estudiante7", "Apellido7", "est7@expoferia.edu", self._hash_password("estudiante7"), "estudiante"),
                ("Estudiante8", "Apellido8", "est8@expoferia.edu", self._hash_password("estudiante8"), "estudiante"),
                ("Estudiante9", "Apellido9", "est9@expoferia.edu", self._hash_password("estudiante9"), "estudiante"),
                ("Estudiante10", "Apellido10", "est10@expoferia.edu", self._hash_password("estudiante10"), "estudiante")
            ]
            
            print("Insertando usuarios...")
            user_ids = {}
            for usuario in usuarios:
                query = "INSERT INTO usuarios (nombre, apellido, email, contraseña_hash, rol) VALUES (%s, %s, %s, %s, %s)"
                self.cursor.execute(query, usuario)
                user_ids[usuario[2]] = self.cursor.lastrowid  # Guardar ID por email
            
            self.connection.commit()
            print(f"✓ {len(usuarios)} usuarios insertados")

            # 2. Insertar profesores (depende de usuarios)
            profesores = [
                (user_ids["vrojas@expoferia.edu"], "Sistemas", "1234567890"),
                (user_ids["cmendoza@expoferia.edu"], "Industrial", "2345678901"),
                (user_ids["mgonzalez@expoferia.edu"], "Civil", "3456789012")
            ]
            
            print("Insertando profesores...")
            profesor_ids = []
            for profesor in profesores:
                query = "INSERT INTO profesores (id_usuario, departamento, telefono) VALUES (%s, %s, %s)"
                self.cursor.execute(query, profesor)
                profesor_ids.append(self.cursor.lastrowid)
            
            self.connection.commit()
            print(f"✓ {len(profesores)} profesores insertados")

            # 3. Insertar estudiantes (depende de usuarios)
            estudiantes = [
                (user_ids["est1@expoferia.edu"], "Ing. Sistemas", 5, "2020-001"),
                (user_ids["est2@expoferia.edu"], "Ing. Sistemas", 5, "2020-002"),
                (user_ids["est3@expoferia.edu"], "Ing. Industrial", 6, "2020-003"),
                (user_ids["est4@expoferia.edu"], "Ing. Industrial", 6, "2020-004"),
                (user_ids["est5@expoferia.edu"], "Ing. Civil", 7, "2020-005"),
                (user_ids["est6@expoferia.edu"], "Ing. Civil", 7, "2020-006"),
                (user_ids["est7@expoferia.edu"], "Ing. Sistemas", 8, "2019-001"),
                (user_ids["est8@expoferia.edu"], "Ing. Sistemas", 8, "2019-002"),
                (user_ids["est9@expoferia.edu"], "Ing. Industrial", 9, "2019-003"),
                (user_ids["est10@expoferia.edu"], "Ing. Civil", 9, "2019-004")
            ]
            
            print("Insertando estudiantes...")
            estudiante_ids = {}
            for i, estudiante in enumerate(estudiantes, 1):
                query = "INSERT INTO estudiantes (id_usuario, carrera, semestre, matricula) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, estudiante)
                estudiante_ids[f"est{i}@expoferia.edu"] = self.cursor.lastrowid
            
            self.connection.commit()
            print(f"✓ {len(estudiantes)} estudiantes insertados")

            # 4. Insertar proyectos (depende de profesores)
            proyectos = [
                ("Sistema de Gestión Académica", "Plataforma para gestión de calificaciones", profesor_ids[0], "2023-01-15", "aprobado", "Desarrollo Software"),
                ("Robot Autónomo", "Robot para limpieza de áreas comunes", profesor_ids[1], "2023-02-20", "en_proceso", "Robótica"),
                ("Análisis de Estructuras", "Estudio de estructuras en edificios antiguos", profesor_ids[2], "2023-03-10", "completado", "Ingeniería Civil"),
                ("App para Gestión de Inventarios", "Aplicación móvil para control de inventarios", profesor_ids[0], "2023-04-05", "aprobado", "Desarrollo Móvil"),
                ("Energías Renovables", "Sistema de aprovechamiento de energía solar", profesor_ids[1], "2023-05-12", "en_proceso", "Energías Alternativas"),
                ("Redes Neuronales", "Modelo predictivo usando IA", profesor_ids[0], "2023-06-18", "rechazado", "Inteligencia Artificial"),
                ("Diseño de Puentes", "Nuevos modelos para puentes peatonales", profesor_ids[2], "2023-07-22", "completado", "Ingeniería Civil"),
                ("Sistema de Riego Automático", "Control inteligente de riego para jardines", profesor_ids[1], "2023-08-30", "aprobado", "Automatización"),
                ("Realidad Virtual", "Aplicación educativa con VR", profesor_ids[0], "2023-09-14", "en_proceso", "Tecnología Educativa"),
                ("Análisis de Datos", "Herramientas para big data", profesor_ids[0], "2023-10-08", "completado", "Ciencia de Datos")
            ]
            
            print("Insertando proyectos...")
            proyecto_ids = []
            for proyecto in proyectos:
                query = """
                INSERT INTO proyectos (titulo, descripcion, id_profesor_responsable, fecha_creacion, estado, area_conocimiento)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, proyecto)
                proyecto_ids.append(self.cursor.lastrowid)
            
            self.connection.commit()
            print(f"✓ {len(proyectos)} proyectos insertados")

            # 5. Insertar estudiantes en proyectos (depende de proyectos y estudiantes)
            proyecto_estudiantes = [
                (proyecto_ids[0], estudiante_ids["est1@expoferia.edu"], "Desarrollador Backend", "2023-01-20"),
                (proyecto_ids[0], estudiante_ids["est2@expoferia.edu"], "Desarrollador Frontend", "2023-01-20"),
                (proyecto_ids[1], estudiante_ids["est3@expoferia.edu"], "Diseñador Mecánico", "2023-02-25"),
                (proyecto_ids[1], estudiante_ids["est4@expoferia.edu"], "Programador", "2023-02-25"),
                (proyecto_ids[2], estudiante_ids["est5@expoferia.edu"], "Investigador", "2023-03-15"),
                (proyecto_ids[2], estudiante_ids["est6@expoferia.edu"], "Asistente", "2023-03-15"),
                (proyecto_ids[3], estudiante_ids["est7@expoferia.edu"], "Líder de Proyecto", "2023-04-10"),
                (proyecto_ids[3], estudiante_ids["est8@expoferia.edu"], "Desarrollador", "2023-04-10"),
                (proyecto_ids[4], estudiante_ids["est9@expoferia.edu"], "Investigador", "2023-05-20"),
                (proyecto_ids[4], estudiante_ids["est10@expoferia.edu"], "Asistente", "2023-05-20"),
                (proyecto_ids[5], estudiante_ids["est1@expoferia.edu"], "Analista de Datos", "2023-06-20"),
                (proyecto_ids[6], estudiante_ids["est2@expoferia.edu"], "Diseñador", "2023-07-25"),
                (proyecto_ids[6], estudiante_ids["est3@expoferia.edu"], "Ingeniero", "2023-07-25"),
                (proyecto_ids[7], estudiante_ids["est4@expoferia.edu"], "Programador", "2023-08-05"),
                (proyecto_ids[7], estudiante_ids["est5@expoferia.edu"], "Electrónico", "2023-08-05"),
                (proyecto_ids[8], estudiante_ids["est6@expoferia.edu"], "Diseñador VR", "2023-09-18"),
                (proyecto_ids[8], estudiante_ids["est7@expoferia.edu"], "Desarrollador", "2023-09-18"),
                (proyecto_ids[9], estudiante_ids["est8@expoferia.edu"], "Analista", "2023-10-10"),
                (proyecto_ids[9], estudiante_ids["est9@expoferia.edu"], "Estadístico", "2023-10-10"),
                (proyecto_ids[9], estudiante_ids["est10@expoferia.edu"], "Investigador", "2023-10-10")
            ]
            
            print("Asignando estudiantes a proyectos...")
            for pe in proyecto_estudiantes:
                query = """
                INSERT INTO proyecto_estudiantes (id_proyecto, id_estudiante, rol_en_proyecto, fecha_incorporacion)
                VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query, pe)
            
            self.connection.commit()
            print(f"✓ {len(proyecto_estudiantes)} asignaciones creadas")

            # 6. Insertar eventos (depende de profesores)
            eventos = [
                ("Inscripción de Proyectos", "Período para registrar nuevos proyectos", "2023-11-01 08:00:00", "2023-11-15 17:00:00", "inscripcion", "Edificio A, Sala 101", profesor_ids[0]),
                ("Evaluación de Proyectos", "Revisión por el comité evaluador", "2023-11-20 09:00:00", "2023-11-25 16:00:00", "evaluacion", "Edificio B, Sala 201", profesor_ids[1]),
                ("Expoferia 2023", "Presentación de proyectos a la comunidad", "2023-12-05 10:00:00", "2023-12-07 18:00:00", "feria", "Auditorio Principal", profesor_ids[0]),
                ("Reunión Informativa", "Explicación de requisitos y procesos", "2023-10-25 14:00:00", "2023-10-25 16:00:00", "reunion", "Edificio C, Sala 301", profesor_ids[0])
            ]
            
            print("Insertando eventos...")
            for evento in eventos:
                query = """
                INSERT INTO eventos (nombre, descripcion, fecha_inicio, fecha_fin, tipo, ubicacion, responsable)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, evento)
            
            self.connection.commit()
            print(f"✓ {len(eventos)} eventos insertados")

            # 7. Insertar reportes
            reportes = [
                ("Proyectos por docente", "Listado de proyectos por profesor responsable", "id_profesor", "pdf"),
                ("Estudiantes participantes", "Listado de todos los estudiantes en proyectos", None, "csv"),
                ("Proyectos por área", "Proyectos agrupados por área de conocimiento", "area_conocimiento", "ambos"),
                ("Estudiantes por proyecto", "Listado de estudiantes en un proyecto específico", "id_proyecto", "pdf")
            ]
            
            print("Insertando reportes...")
            for reporte in reportes:
                query = """
                INSERT INTO reportes (nombre, descripcion, parametros, formato_salida)
                VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query, reporte)
            
            self.connection.commit()
            print(f"✓ {len(reportes)} reportes insertados")

            # 8. Insertar configuraciones
            configuraciones = [
                ("dias_inscripcion", "15", "Días de duración del período de inscripción"),
                ("max_estudiantes_proyecto", "5", "Máximo de estudiantes por proyecto"),
                ("correo_admin", "admin@expoferia.edu", "Correo del administrador para notificaciones")
            ]
            
            print("Insertando configuraciones...")
            for config in configuraciones:
                query = """
                INSERT INTO configuraciones (clave, valor, descripcion)
                VALUES (%s, %s, %s)
                """
                self.cursor.execute(query, config)
            
            self.connection.commit()
            print(f"✓ {len(configuraciones)} configuraciones insertadas")

            print("\n✓ Todos los datos iniciales fueron insertados correctamente")
            
        except Error as e:
            self.connection.rollback()
            print(f"✗ Error al insertar datos iniciales: {e}")
            raise

if __name__ == "__main__":
    try:
        print("\n=== INICIANDO CREACIÓN DE BASE DE DATOS ===")
        creator = DatabaseCreator()
        creator.create_database()
        print("\n=== PROCESO COMPLETADO EXITOSAMENTE ===")
    except Exception as e:
        print(f"\n=== ERROR DURANTE LA CREACIÓN: {e} ===")