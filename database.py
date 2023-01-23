import psycopg2

def abrirConexion():
 try:
    conexion= psycopg2.connect(
    host = 'localhost',
    database = 'usersdb',
    user = 'postgres',
    password  = '1234'
    )
    return conexion
 except:
    print('error al conectarse')
    

def cerrarConexion(conexion):
    conexion.close() 