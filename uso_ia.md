# Registro de uso de IA

## Parte 1: Consultas, respuestas y ajustes



### 1. Fixture de productos

- **Prompt de poblamiento indicado en la pauta:** “Genera una fixture JSON de Django para el modelo `catalogo.Producto` con 40 productos de ferretería chilenos realistas. Campos: nombre, categoria, precio (int, 1000 a 150000), stock (int, 0 a 50). Formato: lista de objetos con model, pk y fields, lista para cargar con loaddata.”
- **Resumen de la respuesta:** Se prepararon 40 registros en formato de fixture de Django, con nombres y categorías de ferretería.
- **Ajustes y comprobación:** Se corrigió el precio del perno hexagonal a $1.890 para que respete el mínimo de $1.000 validado por el modelo. Se comprobó la cantidad, los rangos de precio y stock y la carga mediante `loaddata` en una base temporal y luego en la base local.

### 2. Django Admin

- **Prompt:** “Configura Django Admin para gestionar el modelo `Producto`, mostrando al menos tres campos y habilitando búsqueda o filtros.”
- **Resumen de la respuesta:** Se registró `Producto` en el administrador con columnas para nombre, categoría, precio y stock, además de búsqueda y filtro por categoría.
- **Qué usé o modifiqué antes de integrarlo:** Integré la configuración en `catalogo/admin.py` y comprobé el acceso al administrador y las acciones de crear, editar, buscar y eliminar productos con una base de datos temporal.

### 3. Conexión de base de datos

- **Prompt:** “Configura la conexión de este proyecto Django a SQLite y comprueba que pueda guardar y consultar productos.”
- **Resumen de la respuesta:** Se revisó la configuración de la base de datos de Django y se comprobó el acceso al modelo mediante el ORM.
- **Qué usé o modifiqué antes de integrarlo:** Mantuve SQLite como base de datos en `config/settings.py`. Probé las migraciones y la creación y lectura de un producto con una base temporal para no depender de los datos locales.

### 4. Configuración del proyecto

- **Prompt:** “Configura Django para que la aplicación de catálogo y sus páginas funcionen con el idioma y la zona horaria de Chile.”
- **Resumen de la respuesta:** Se revisaron los ajustes del proyecto relacionados con la aplicación, el idioma, la hora local y las páginas disponibles.
- **Qué usé o modifiqué antes de integrarlo:** La aplicación quedó incluida en `INSTALLED_APPS`, el idioma se configuró como `es-cl` y la zona horaria como `America/Santiago` en `config/settings.py`. También verifiqué las rutas y páginas integradas con las comprobaciones y pruebas del proyecto.


## Parte 2: Explicación del proceso

Primero preparé el proyecto Django para el catálogo de una ferretería.
Definí el producto con nombre, categoría, precio y stock, y comprobé sus migraciones.
Configuré SQLite en los ajustes del proyecto para guardar los productos.
Registré el modelo en Django Admin para poder gestionar el catálogo.
Dejé visibles el nombre, la categoría, el precio y el stock de cada producto.
También configuré la búsqueda y el filtro por categoría para encontrar productos.
Preparé una fixture con 40 productos de ferretería en el formato que acepta Django.
Revisé los campos, los precios y las cantidades antes de cargar los registros.
Ajusté el precio del perno hexagonal para respetar el mínimo definido para los productos.
Cargué la fixture con `loaddata` y comprobé que los productos aparecieran en la base de datos.
Configuré el idioma del proyecto en español de Chile y la zona horaria de Santiago.
Finalmente probé el administrador, la carga de datos y la consulta del catálogo desde la aplicación.
