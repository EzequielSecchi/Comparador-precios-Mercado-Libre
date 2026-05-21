import requests
import urllib.robotparser
import sys
from bs4 import BeautifulSoup
from SQLfunc.conexion_sql import crear_tabla
from SQLfunc.conexion_sql import ingresar_dato
from SQLfunc.conexion_sql import verificar_existencia

url = "https://listado.mercadolibre.com.ar/mouse"
nombre_tabla = "mouses"

headers = {
    "User-Agent": "comparador-precios-script/1.0 ("+url+")"
}

print("Analizando permisos de la pagina...")

url_robots = "https://listado.mercadolibre.com.ar/robots.txt"
respuesta_robots = requests.get(url_robots, headers=headers)

guardia = urllib.robotparser.RobotFileParser()

guardia.set_url(url_robots)
guardia.parse(respuesta_robots.text.splitlines())

mi_user_agent = "*"

if guardia.can_fetch(mi_user_agent, url):
    print("¡Luz verde! El robots.txt PERMITE extraer datos de esta URL.")
else:
    print("¡ALTO! El robots.txt PROHÍBE entrar a esta URL. Cancelando operación.")
    sys.exit("Terminando programa...")

print("Conectando...")
try:
    respuesta = requests.get(url, headers=headers, timeout=10)
    respuesta.raise_for_status()

except requests.exceptions.Timeout:
    print("Error: Tiempo agotado para conectarse a: ", url)
except requests.exceptions.HTTPError as e:
    print("Error HTTP:", e)
except requests.exceptions.RequestException as e:
    print("Error, peticion no valida:", e)
except KeyboardInterrupt:
    print("Cancelado")
else:
    print("OK:", respuesta.status_code)
    soup = BeautifulSoup(respuesta.text, "html.parser")
    print("Título:", soup.title.string.strip() if soup.title else "(sin título)") # type: ignore

    cajas_productos = soup.select('.ui-search-result__wrapper')

    print("Buscando productos...")

    print(f"\nSe encontraron {len(cajas_productos)} productos en total")

#    if len(cajas_productos) > 0:
#        primera_caja = cajas_productos[0]

#        print(primera_caja.prettify())

    lista_productos = []

    print("Imprimiendo y subiendo a base de datos de sqlite3...")

    for caja in cajas_productos:

        titulo = caja.select_one('.poly-component__title')
        precio = caja.select_one('.andes-money-amount__fraction')
        link = caja.select_one('.poly-component__link')

        if titulo and precio and link:

            titulo_text = titulo.text.strip()
            precio_text = precio.text.strip()
            link_text = link.get('href')



            print(f"Producto: {titulo_text}")
            print(f"Precio: $ {precio_text}")
            print("-" * 30)

            precio_sin_punto = precio_text.replace(".","")
            try:
                precio_entero = int(precio_sin_punto)
            except ValueError:
                precio_entero = 0
            
            lista_productos.append({"titulo": titulo_text,
                                    "precio": precio_entero,
                                    "link": link_text})

    i = len(lista_productos)
    for j in range(i):
        for k in range(0, i-j-1):
            
            if(lista_productos[k]["precio"]>lista_productos[k+1]["precio"]):
                aux = lista_productos[k]
                lista_productos[k] = lista_productos[k+1]
                lista_productos[k+1] = aux
    
    crear_tabla(nombre_tabla)

    for lista in lista_productos:
        if verificar_existencia(lista["titulo"], lista["link"], nombre_tabla) is True:
            ingresar_dato(lista["precio"], lista["titulo"], lista["link"], nombre_tabla)
