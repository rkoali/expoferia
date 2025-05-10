import re

class Validators:
    @staticmethod
    def validar_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    @staticmethod
    def validar_password(password):
        # Al menos 8 caracteres, una mayúscula, una minúscula y un número
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True
        
    @staticmethod
    def validar_fecha(fecha_str):
        try:
            from datetime import datetime
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False