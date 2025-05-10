from database.database_connection import DatabaseConnection
from config import DB_CONFIG

class Proyecto:
    def __init__(self, db):
        self.db = db

    def crear_proyecto(self, titulo, descripcion, profesor_id, area_conocimiento=None):
        query = """
        INSERT INTO proyectos (titulo, descripcion, id_profesor_responsable, fecha_creacion, area_conocimiento, estado)
        VALUES (%s, %s, %s, CURDATE(), %s, 'en_proceso')
        """
        return self.db.execute_query(
            query, 
            (titulo, descripcion, profesor_id, area_conocimiento), 
            commit=True
        )

    def actualizar_proyecto(self, proyecto_id, titulo=None, descripcion=None, area_conocimiento=None, estado=None):
        updates = []
        params = []
        
        if titulo is not None:
            updates.append("titulo = %s")
            params.append(titulo)
        if descripcion is not None:
            updates.append("descripcion = %s")
            params.append(descripcion)
        if area_conocimiento is not None:
            updates.append("area_conocimiento = %s")
            params.append(area_conocimiento)
        if estado is not None:
            updates.append("estado = %s")
            params.append(estado)
        
        if not updates:
            return False
            
        params.append(proyecto_id)
        
        query = f"UPDATE proyectos SET {', '.join(updates)} WHERE id_proyecto = %s"
        return self.db.execute_query(query, tuple(params), commit=True)

    def obtener_proyecto_por_id(self, proyecto_id):
        query = "SELECT * FROM proyectos WHERE id_proyecto = %s"
        return self.db.execute_query(query, (proyecto_id,), fetch_one=True)