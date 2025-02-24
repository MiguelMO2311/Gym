import pyodbc

connection_string = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=gym;'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
    'Encrypt=no;'
)

try:
    conn = pyodbc.connect(connection_string)
    print("Conexión exitosa")
    conn.close()
except pyodbc.Error as ex:
    print("Error al conectar a la base de datos:", ex)
