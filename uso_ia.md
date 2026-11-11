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

### 5. Preparación del entorno de la etapa 0

- **Prompt:** “Instala dependencias, migra y carga el poblamiento; verifica que el listado se muestra desde la BD.”
- **Resumen de la respuesta:** Se instalaron las dependencias de `requirements.txt`, se comprobaron las migraciones, se cargaron los 40 productos de la fixture y se verificó la portada mediante una prueba y una solicitud HTTP.
- **Qué usé o modifiqué antes de integrarlo:** Usé el entorno virtual existente. La fixture quedó cargada en la base local; había además un producto previo, por lo que la consulta ORM devolvió 41 productos. La portada respondió HTTP 200 y mostró los 41 productos de la base de datos. La prueba `test_portada_muestra_productos_de_la_base_de_datos` pasó.

### 6. CRUD web del catálogo

- **Prompt:** “Implemente las operaciones desde el sitio: crear con formulario, editar y eliminar con confirmación; tras cada operación redirija al listado principal.”
- **Resumen de la respuesta:** Se agregó un formulario basado en el modelo `Producto` y vistas para crear, editar y eliminar, accesibles desde el catálogo.
- **Qué usé o modifiqué antes de integrarlo:** Restringí la gestión a personal autenticado; añadí confirmación antes de eliminar y un aviso cuando existen compras asociadas que impiden borrar el producto. Las operaciones correctas regresan al listado, donde el cambio se consulta desde la base de datos. Agregué pruebas para el flujo, los permisos y la restricción de borrado.


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
Para la etapa 0 instalé las dependencias, ejecuté las migraciones y cargué la fixture.
Verifiqué con una prueba y una solicitud a la portada que los productos se muestran desde SQLite.
Implementé el alta, edición y eliminación con confirmación desde las páginas del catálogo.
Las vistas guardan los cambios en la base de datos y redirigen al listado principal.

### 7. Reportes con ORM

- **Prompt:** “Crea dos reportes Django para el catálogo: un resumen agrupado por categoría con cantidad, precio promedio y stock total; y un listado de productos con stock crítico filtrado y ordenado con el ORM. Agrega templates y enlaces de navegación.”
- **Resumen de la respuesta:** Se implementaron dos vistas con `values`, `annotate`, `Count`, `Avg`, `Sum`, `filter` y `order_by`, además de sus templates y rutas.
- **Qué usé o modifiqué antes de integrarlo:** Adapté los reportes a los campos existentes de `Producto`. El primer reporte agrupa por categoría y el segundo considera stock crítico de hasta 5 unidades. Agregué pruebas para verificar los cálculos, el filtro y el ordenamiento desde la base de datos.
