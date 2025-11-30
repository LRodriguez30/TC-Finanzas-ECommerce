# helpers.py
import bcrypt

def encriptar_contraseña(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando bcrypt.
    Devuelve el hash como string para almacenar en la base de datos.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verificar_contraseña(password: str, hashed: str) -> bool:
    """
    Verifica si la contraseña ingresada coincide con el hash almacenado.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))