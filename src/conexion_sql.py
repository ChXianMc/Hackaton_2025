import pyodbc


connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  
    "DATABASE=Hackathon2025;"   
    "Trusted_Connection=yes;"  
)

try:
    # Establecer conexión
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    
    #cursor.execute("SELECT @@VERSION AS 'SQL Server Version';")
    #version = cursor.fetchone()[0]  

   # print("✅ Versión de SQL Server:")
   # print(version)

except pyodbc.Error as ex:
    print(f"❌ Error al conectar o ejecutar la consulta: {ex}")

finally:
    # Cerrar conexión
    if 'connection' in locals():
        connection.close()