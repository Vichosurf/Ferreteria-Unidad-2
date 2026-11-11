# Documento de uso de IA

## Parte 1: Registro de consultas

### 1. Carro de compras

- **Prompt:** “Agregue un carro de supermercado en el navbar para crear una lista de productos, mostrar el detalle del carro y habilitar el botón Pagar cuando la lista esté lista.”
- **Resumen de la respuesta:** Se creó un carro basado en sesión con agregar, actualizar, quitar, total y pago de demostración. También se agregó el ícono del carro al navbar.
- **Uso y adaptación:** Cambié el flujo para que el catálogo agregara productos al carro en vez de comprar inmediatamente. Conservé la compra directa anterior para no romper funcionalidades existentes y agregué pruebas del nuevo flujo.

### 2. Reserva y devolución de stock

- **Prompt:** “Cuando agregue una unidad al carro debe restarse del stock y, si quito el producto o reduzco la cantidad, debe volver al stock original.”
- **Resumen de la respuesta:** La reserva se descuenta al agregar, se devuelve al quitar o reducir y el pago no vuelve a descontar las unidades.
- **Uso y adaptación:** Revisé una primera condición de stock que podía contar dos veces las unidades ya reservadas y la corregí para comparar solo contra el stock restante. Agregué transacciones y pruebas para agregar, quitar, pagar y devolver stock.

### 3. Tema visual para administradores

- **Prompt:** “Cuando inicie sesión como administrador, cambie el fondo a cyan y use azul oscuro en footer, navbar y botones, mezclado con morado oscuro.”
- **Resumen de la respuesta:** Se agregó una clase visual para usuarios administradores con fondo cyan, navbar y footer en degradado azul oscuro–morado, y botones con la misma combinación.
- **Uso y adaptación:** Apliqué el tema únicamente cuando `user.is_staff` está autenticado y verifiqué en las pruebas que la plantilla incluya la clase `tema-administrador`.

### 4. Reemplazo del logo

- **Prompt:** “Reemplace la imagen naranja con la letra F por la imagen proporcionada y use un fondo celeste.”
- **Resumen de la respuesta:** Se agregó la imagen del logo a los archivos estáticos y se reemplazó la F del navbar y del footer.
- **Uso y adaptación:** Ajusté el tamaño, el recorte y el fondo celeste con CSS para que el logo se vea correctamente en ambas ubicaciones. No cambié el contenido de los productos ni la estructura de la navegación.

### 5. Productos guardados, notificaciones e historial

- **Prompt:** “Agregue productos guardados en el navbar, cambie avisos por notificaciones con un ícono, deje avisos en el footer y muestre el historial de compras como tarjetas.”
- **Resumen de la respuesta:** Se agregó el guardado de productos por usuario, una vista para consultarlos y quitarlos, el acceso visual a notificaciones, avisos en el footer y tarjetas para cada compra del historial.
- **Uso y adaptación:** Revisé el modelo existente de avisos, agregué el modelo `ProductoGuardado` con restricción para evitar duplicados, incorporé migración y probé los flujos de guardar, quitar, notificar y mostrar compras.

## Parte 2: Explicación personal del proceso

Usé la IA como apoyo para avanzar en mi catálogo sin dejar de revisar cada cambio.
Primero le pedí orientación para organizar la navegación y separar las opciones de clientes y administradores.
La propuesta inicial me sirvió como base, pero tuve que corregir enlaces y comprobar las rutas en Django.
También solicité ayuda para asociar las imágenes con el nombre exacto de cada producto.
Revisé el fixture y confirmé que “Newer Hammer” no correspondía a un registro existente.
Para el CRUD utilicé la orientación sobre formularios, vistas y confirmación antes de eliminar.
Después pedí apoyo para construir los reportes usando consultas del ORM.
La respuesta me ayudó a usar `annotate`, `Count`, `Avg`, `Sum`, `filter` y `order_by` en las vistas.
Comprobé que los resultados de los reportes coincidieran con los datos guardados en la base de datos.
Para el carro solicité una solución basada en sesiones y revisé especialmente la reserva de stock.
Tuve que corregir la lógica para devolver unidades al quitar productos o reducir cantidades.
También verifiqué que el pago no descontara nuevamente el stock que ya estaba reservado.
En el formulario de clientes revisé las validaciones, el correo válido, el mensaje mínimo y el token CSRF.
Los cambios visuales del administrador y el nuevo logo los adapté después de probar las plantillas.
Las respuestas que funcionaron directamente fueron algunas estructuras de vistas y consultas, pero revisé todas las rutas.
Aprendí que la IA sirve como guía, pero debo probar, entender el ORM y comprobar que cada función cumpla la pauta.
En la última mejora pedí una forma de guardar productos y mostrar mejor las notificaciones y el historial.
La propuesta me sirvió como base, pero adapté el modelo para evitar productos guardados duplicados por usuario.
