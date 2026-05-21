# Comparador de precios Mercado Libre

## Introduccion
En este proyecto se utiliza scraping para obtener precio de productos en Mercado Libre, ordenarlos y guardarlos en una base de datos SQLite. La idea es poder comparar precios de un mismo tipo de producto y así encontrar las mejores ofertas.

El programa también verifica robots.txt antes de acceder a la URL, lo cual ayuda a respetar las reglas de acceso definidas por el sitio.

## Funcionamiento del codigo

### Codigo principal
El archivo principal es `index.py`. Su flujo principal es:

1. Definir la `url` de búsqueda en Mercado Libre y el nombre de la tabla SQLite (`nombre_tabla`).
2. Crear un encabezado personalizado `User-Agent` para la petición HTTP.
3. Leer `robots.txt` y comprobar si la URL está permitida usando `urllib.robotparser`.
4. Descargar la página con `requests.get(...)`, usando `timeout=10` para evitar bloqueos indefinidos.
5. Analizar el HTML con `BeautifulSoup`.
6. Buscar cada producto mediante la clase `.ui-search-result__wrapper`.
7. Extraer `titulo`, `precio` y `link` de cada producto.
8. Convertir el precio a entero eliminando puntos.
9. Ordenar la lista de productos por precio de menor a mayor.
10. Crear la tabla SQLite correspondiente y guardar los productos nuevos sin repetidos.

### Base de datos
El código usa SQLite a través del módulo `SQLfunc/conexion_sql.py`.

- `crear_tabla(tabla)` crea una tabla dinámica con el nombre elegido.
- `ingresar_dato(precio, nombre, link, tabla)` inserta un producto en la tabla.
- `verificar_existencia(nombre, link, tabla)` comprueba si un producto ya existe para evitar duplicados.

La base de datos se guarda en el archivo local `scraper.db`.

### ¿Por qué no aparece en phpMyAdmin?
Porque phpMyAdmin administra bases de datos MySQL/MariaDB. Este proyecto usa SQLite, que crea un archivo local (`scraper.db`). Para ver los datos puedes usar:

```bash
sqlite3 scraper.db
```

o un visor de SQLite como `DB Browser for SQLite`.

## Consideraciones importantes

- El scraping está diseñado para Mercado Libre, pero la búsqueda depende de los selectores CSS actuales de la página. Si Mercado Libre cambia su HTML, los selectores pueden dejar de funcionar.
- Se usa `robots.txt` para comprobar permisos antes de extraer datos.
- El ordenamiento actual es por burbuja, se podría mejorar con `sorted(...)` o `.sort(key=lambda x: x["precio"])`.
- Por el momento, la tabla se crea con el nombre que pongas en `nombre_tabla`, por lo que debes usar identificadores válidos.

## Mejoras sugeridas

- Usar `with sqlite3.connect(...) as conexion:` para gestionar automáticamente la conexión.
- Evitar construir SQL con concatenación de strings, especialmente con nombres de tablas dinámicos.
- Usar una ordenación nativa de Python en lugar de bubble sort.
- Añadir un archivo `requirements.txt` con las dependencias.
- Añadir una sección de ejecución y configuración en este README.

## Ejecución
Primero activa tu entorno virtual y asegúrate de tener `requests` y `beautifulsoup4` instalados.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
```

Luego ejecuta:

```bash
.venv/bin/python index.py
```

Si todo funciona, el archivo `scraper.db` se creará y se llenará con los datos de productos scrapeados.
