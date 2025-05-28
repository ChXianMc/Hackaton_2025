from conexion_sql import mostrar_tabla

# Esta versión asume que mostrar_tabla() ya imprime la tabla
registros = mostrar_tabla("Usuarios") 

# Y adicionalmente muestra el conteo
print(f"\nCantidad total de registros: {len(registros)}")