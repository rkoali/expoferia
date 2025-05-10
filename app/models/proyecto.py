from app import db
from datetime import datetime

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id = db.Column('id_proyecto', db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    id_profesor_responsable = db.Column(db.Integer, db.ForeignKey('profesores.id_profesor'), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    estado = db.Column(db.Enum('en_proceso', 'completado', 'aprobado', 'rechazado'), default='en_proceso')
    area_conocimiento = db.Column(db.String(50))
    
    # Relaciones
    profesor = db.relationship('Profesor', backref='proyectos')
    estudiantes = db.relationship('Estudiante', 
                                secondary='proyecto_estudiantes',
                                backref=db.backref('proyectos', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Proyecto {self.titulo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'profesor': f"{self.profesor.user.nombre} {self.profesor.user.apellido}",
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d'),
            'estado': self.estado,
            'area_conocimiento': self.area_conocimiento
        }