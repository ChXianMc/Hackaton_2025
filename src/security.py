from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,      # Iteraciones
    memory_cost=65536, # 64MB de RAM
    parallelism=4     # Hilos
)

# Hash (longitud ~90 chars, pero más seguro)
hash_arg = ph.hash("MiClave123")
print(f"Hash Argon2: {hash_arg}")

# Verificación
try:
    ph.verify(hash_arg, "MiClave123")  # True/False
    print("todo chido my brou")
except:
    print("Contraseña incorrecta")