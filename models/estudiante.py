from models.usuario import Usuario

class Estudiante:
    def __init__(self, db):
        self.db = db

    def crear_estudiante(self, usuario_id, carrera, semestre, matricula):
        query = """
        INSERT INTO estudiantes (id_usuario, carrera, semestre, matricula)
        VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_query(query, (usuario_id, carrera, semestre, matricula), commit=True)

    def actualizar_estudiante(self, usuario_id, carrera, semestre, matricula):
        query = """
        UPDATE estudiantes 
        SET carrera = %s, semestre = %s, matricula = %s
        WHERE id_usuario = %s
        """
        return self.db.execute_query(query, (carrera, semestre, matricula, usuario_id), commit=True)

    def obtener_estudiante_por_usuario(self, usuario_id):
        query = "SELECT * FROM estudiantes WHERE id_usuario = %s"
        return self.db.execute_query(query, (usuario_id,), fetch_one=True)