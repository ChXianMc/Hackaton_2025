from conexion_sql import mostrar_tabla,conectar_sql_server,register,inicio

conexion = conectar_sql_server()
contraseña = input("Ingresa tu contraseña: ")
email = input("Ingrese su email mi rey:")
#nombre = input("nombre\n")
#email= input("Email:\n")
#registros = mostrar_tabla("Usuarios",conexion) 
#user = register("Usuarios",conexion,nombre,email,contraseña)
inicio(email,contraseña,conexion)

#print(f"\nCantidad total de registros: {len(registros)}")