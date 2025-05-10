from database.database_connection import DatabaseConnection
from config import DB_CONFIG
import hashlib

class Usuario:
    def __init__(self, db):
        self.db = db

    def crear_usuario(self, nombre, apellido, email, password, rol):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, contraseña_hash, rol)
        VALUES (%s, %s, %s, %s, %s)
        """
        hashed_password = self._hash_password(password)
        return self.db.execute_query(query, (nombre, apellido, email, hashed_password, rol), commit=True)

    def obtener_usuario_por_id(self, usuario_id):
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        return self.db.execute_query(query, (usuario_id,), fetch_one=True)

    def actualizar_usuario(self, usuario_id, nombre, apellido, email):
        query = """
        UPDATE usuarios 
        SET nombre = %s, apellido = %s, email = %s
        WHERE id_usuario = %s
        """
        return self.db.execute_query(query, (nombre, apellido, email, usuario_id), commit=True)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()