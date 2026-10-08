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

Preparé el proyecto Django para trabajar con la variante de ferretería.
Definí un producto con nombre, categoría, precio y stock.
Configuré SQLite y generé la migración inicial del modelo.
Registré el modelo en Django Admin para administrar el catálogo.
Configuré columnas visibles, búsqueda y filtro por categoría.
Preparé una fixture con 40 productos de ejemplo para poblar la base de datos.
Revisé que los precios y las cantidades respetaran los rangos del modelo.
Cargué la fixture con el comando de Django y verifiqué los registros.
Conecté la página principal con una consulta al ORM.
Organicé los productos en tarjetas con su categoría, precio y stock.
Probé la carga y la página principal usando una base SQLite temporal.
También recuperé las funciones de cuenta, consultas, compras de demostración,
historial, notificaciones y preferencias, y comprobé la suite de pruebas.
Finalmente documenté los comandos para instalar, iniciar y revisar el proyecto.
