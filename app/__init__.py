from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configurar login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Registrar blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from app.profesor import profesor as profesor_blueprint
    app.register_blueprint(profesor_blueprint, url_prefix='/profesor')
    
    from app.estudiante import estudiante as estudiante_blueprint
    app.register_blueprint(estudiante_blueprint, url_prefix='/estudiante')
    
    # Registrar manejadores de errores
    from app.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)
    
    return app