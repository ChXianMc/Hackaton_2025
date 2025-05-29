from argon2 import PasswordHasher
import re

# Configuración del hasher (global al módulo)
_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=4,
    hash_len=32
)

def validar_contraseña(contraseña: str) -> bool:
    """
    Valida que la contraseña cumpla con:
    - Mínimo 8 caracteres
    - Al menos 1 mayúscula
    - Al menos 1 minúscula
    - Al menos 1 número
    """
    return (len(contraseña) >= 8 and
            re.search(r"[A-Z]", contraseña) and
            re.search(r"[a-z]", contraseña) and
            re.search(r"\d", contraseña))

def crear_hash_seguro(contraseña: str) -> str:
   
    if not validar_contraseña(contraseña):
        raise ValueError(
            "La contraseña debe tener: 8+ caracteres, "
            "1 mayúscula, 1 minúscula y 1 número"
        )
    return _hasher.hash(contraseña)

def verificar_contraseña(hash_guardado: str, contraseña: str) -> bool:
    """Verifica si una contraseña coincide con su hash almacenado"""
    try:
        return _hasher.verify(hash_guardado, contraseña)
    except:
        return False