from conexion_sql import mostrar_tabla,conectar_sql_server,usuario
nombre = "fabian"
email = "fabian8590@gmail.com"

conexion = conectar_sql_server()
registros = mostrar_tabla("Usuarios",conexion) 
user = usuario("Usuarios",conexion,nombre,email)

print(f"\nCantidad total de registros: {len(registros)}")