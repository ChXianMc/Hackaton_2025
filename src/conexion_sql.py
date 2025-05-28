import pyodbc
from tabulate import tabulate  # Para formato de tabla más bonito (opcional)

def conectar_sql_server():
    
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  
        "DATABASE=Hackathon2025;"   
        "Trusted_Connection=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexión exitosa a SQL Server")
        return conn
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None

def mostrar_tabla(nombre_tabla, conexion):
    
    try:
        cursor = conexion.cursor()
        
        # Obtener datos de la tabla
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        registros = cursor.fetchall()
        
        # Obtener nombres de columnas
        columnas = [column[0] for column in cursor.description]
        
        # Mostrar tabla con formato (usando tabulate)
        print(f"\nContenido de la tabla '{nombre_tabla}':")
        print(tabulate(registros, headers=columnas, tablefmt="grid"))
        print(registros[0][1])
        return registros
        
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return []


if __name__ == "__main__":
    
    conexion = conectar_sql_server()
    
    if conexion:
        try:
            tabla = "Usuarios"  
            registros = mostrar_tabla(tabla, conexion)
            
            
            if registros:
                print(f"\nEstadísticas:")
                print(f"- Cantidad total de registros: {len(registros)}")
                print(f"- Cantidad de columnas: {len(registros[0]) if registros else 0}")
            else:
                print("\nLa tabla está vacía o no existe")
                
        finally:
            
            conexion.close()
            print("\nConexión cerrada")