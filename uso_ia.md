# Registro de uso de IA

## Parte 1: Consultas, respuestas y ajustes

Usé un asistente de IA como apoyo puntual durante el desarrollo. Revisé el código propuesto, lo adapté al proyecto y comprobé los cambios. El historial de GitHub conserva los commits de las etapas; este documento describe las consultas relevantes y el resultado que quedó en esta entrega.

### 1. Modelo y base de datos

- **Prompt:** “Continúa con la etapa 1” junto con la pauta que pide un modelo para la variante Ferretería, conexión a base de datos y migraciones.
- **Resumen de la respuesta:** Se preparó el modelo `Producto` con nombre, categoría, precio y stock, además de una migración inicial.
- **Ajustes y comprobación:** Se conservó el commit de la etapa 0 y se creó `etapa-1-modelo` como commit separado. Se verificaron las migraciones y la creación y lectura de un producto en SQLite temporal.

### 2. Django Admin

- **Prompt:** “Continúa con la etapa 2” y la pauta que solicita registrar el modelo, mostrar al menos tres campos y configurar búsqueda o filtro.
- **Resumen de la respuesta:** Se añadió el registro de `Producto` en Django Admin con columnas, búsqueda y filtro por categoría.
- **Ajustes y comprobación:** Se mantuvo intacta la etapa 1. En una base temporal se probaron el acceso al administrador y las acciones de alta, edición, búsqueda y eliminación.

### 3. Fixture de productos

- **Prompt de poblamiento indicado en la pauta:** “Genera una fixture JSON de Django para el modelo `catalogo.Producto` con 40 productos de ferretería chilenos realistas. Campos: nombre, categoria, precio (int, 1000 a 150000), stock (int, 0 a 50). Formato: lista de objetos con model, pk y fields, lista para cargar con loaddata.”
- **Resumen de la respuesta:** Se prepararon 40 registros en formato de fixture de Django, con nombres y categorías de ferretería.
- **Ajustes y comprobación:** Se corrigió el precio del perno hexagonal a $1.890 para que respete el mínimo de $1.000 validado por el modelo. Se comprobó la cantidad, los rangos de precio y stock y la carga mediante `loaddata` en una base temporal y luego en la base local.

### 4. Catálogo desde la base de datos

- **Prompt:** “Ahora la etapa 3, no cambies nada el commit etapa 2 ya que lo pusiste”, junto con el requisito de reemplazar la lista estática por una consulta ORM.
- **Resumen de la respuesta:** Se conectó la página principal a los productos guardados y se creó una presentación en tarjetas.
- **Ajustes y comprobación:** Se dejó la consulta en `catalogo/views.py`, la presentación en el template y la ruta principal en `config/urls.py`. Las tarjetas usan símbolos ilustrativos por categoría, no fotografías reales. La respuesta HTTP y los productos renderizados se comprobaron tras cargar la fixture.

### 5. Documentación de entrega

- **Prompt:** “Ahora entrega-final, no cambies el commit etapa 3 ni los anteriores”.
- **Resumen de la respuesta:** Se prepararon esta guía de instalación y el registro de uso para acompañar el repositorio.
- **Ajustes y comprobación:** La documentación describe solo lo que está presente en el código de esta entrega. No se añadieron credenciales al repositorio; cada usuario crea su propio superusuario con Django.

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
Finalmente documenté los comandos para instalar, iniciar y revisar el proyecto.
