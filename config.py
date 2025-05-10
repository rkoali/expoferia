# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'expoferia_db',
    'pool_name': 'expoferia_pool',
    'pool_size': 5
}

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Sistema de Gestión - Expoferia de Ingeniería',
    'geometry': '1200x700',
    'theme': 'clam'
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'password_hash_method': 'sha256',  # En producción usar 'bcrypt'
    'session_timeout': 3600  # 1 hora en segundos
}