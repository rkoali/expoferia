from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column('contraseña_hash', db.String(255), nullable=False)
    rol = db.Column(db.Enum('administrador', 'profesor', 'estudiante'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    profesor = db.relationship('Profesor', backref='user', uselist=False)
    estudiante = db.relationship('Estudiante', backref='user', uselist=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_id(self):
        return str(self.id)
        
    @property
    def is_active(self):
        return self.activo
        
    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))