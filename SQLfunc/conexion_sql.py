import sqlite3

def crear_tabla(tabla:str):

    conexion = sqlite3.connect("scraper.db")
    cursor = conexion.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS "+tabla+" ("
                   +"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   +"titulo TEXT, "
                   +"precio INT, "
                   +"link TEXT);")
    
    conexion.commit()

def ingresar_dato(precio: int, nombre: str, link: str, tabla: str):

    conexion = sqlite3.connect("scraper.db")
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO "+tabla+" (titulo, precio, link) VALUES (?, ?, ?);", (nombre,precio,link))

    conexion.commit()
    conexion.close()

    pass

def verificar_existencia(nombre: str, link: str, tabla: str):

    conexion = sqlite3.connect("scraper.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM "+tabla+" WHERE titulo = ? AND link = ?", (nombre, link))
    producto_existente = cursor.fetchone()

    if producto_existente is None:
        return True
    else:
        return False
    