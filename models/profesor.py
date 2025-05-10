from models.usuario import Usuario

class Profesor:
    def __init__(self, db):
        self.db = db

    def crear_profesor(self, usuario_id, departamento, telefono=None):
        query = """
        INSERT INTO profesores (id_usuario, departamento, telefono)
        VALUES (%s, %s, %s)
        """
        return self.db.execute_query(query, (usuario_id, departamento, telefono), commit=True)

    def actualizar_profesor(self, usuario_id, departamento, telefono=None):
        query = """
        UPDATE profesores 
        SET departamento = %s, telefono = %s
        WHERE id_usuario = %s
        """
        return self.db.execute_query(query, (departamento, telefono, usuario_id), commit=True)

    def obtener_profesor_por_usuario(self, usuario_id):
        query = "SELECT * FROM profesores WHERE id_usuario = %s"
        return self.db.execute_query(query, (usuario_id,), fetch_one=True)

    def obtener_todos(self):
        query = """
        SELECT p.*, u.nombre, u.apellido 
        FROM profesores p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        """
        return self.db.execute_query(query, fetch_all=True)