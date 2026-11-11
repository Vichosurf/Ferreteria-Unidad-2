# Documento de uso de IA

## Parte 1: Registro de consultas

### 1. Navegación, cuenta y administración

- **Prompt:** “Cambie el navbar: deje agregar producto en el footer, muestre agregar unidades para administradores dentro del catálogo, quite ayuda, configuración y contacto del navbar, y deje esas opciones dentro de Mi cuenta cuando corresponda.”
- **Resumen de la respuesta:** Se reorganizó la navegación, se diferenciaron las opciones para visitantes, clientes y administradores, y se conservaron los reportes solo para personal autorizado.
- **Uso y adaptación:** Revisé visualmente el resultado y ajusté los enlaces para que Mi cuenta mostrara perfil, historial, configuración y cierre de sesión. También dejé la administración y agregar producto en el footer.

### 2. Carro de compras

- **Prompt:** “Agregue un carro de supermercado en el navbar para crear una lista de productos, mostrar el detalle del carro y habilitar el botón Pagar cuando la lista esté lista.”
- **Resumen de la respuesta:** Se creó un carro basado en sesión con agregar, actualizar, quitar, total y pago de demostración. También se agregó el ícono del carro al navbar.
- **Uso y adaptación:** Cambié el flujo para que el catálogo agregara productos al carro en vez de comprar inmediatamente. Conservé la compra directa anterior para no romper funcionalidades existentes y agregué pruebas del nuevo flujo.

### 3. Reserva y devolución de stock

- **Prompt:** “Cuando agregue una unidad al carro debe restarse del stock y, si quito el producto o reduzco la cantidad, debe volver al stock original.”
- **Resumen de la respuesta:** La reserva se descuenta al agregar, se devuelve al quitar o reducir y el pago no vuelve a descontar las unidades.
- **Uso y adaptación:** Revisé una primera condición de stock que podía contar dos veces las unidades ya reservadas y la corregí para comparar solo contra el stock restante. Agregué transacciones y pruebas para agregar, quitar, pagar y devolver stock.

### 4. Tema visual para administradores

- **Prompt:** “Cuando inicie sesión como administrador, cambie el fondo a cyan y use azul oscuro en footer, navbar y botones, mezclado con morado oscuro.”
- **Resumen de la respuesta:** Se agregó una clase visual para usuarios administradores con fondo cyan, navbar y footer en degradado azul oscuro–morado, y botones con la misma combinación.
- **Uso y adaptación:** Apliqué el tema únicamente cuando `user.is_staff` está autenticado y verifiqué en las pruebas que la plantilla incluya la clase `tema-administrador`.

### 5. Reemplazo del logo

- **Prompt:** “Reemplace la imagen naranja con la letra F por la imagen proporcionada y use un fondo celeste.”
- **Resumen de la respuesta:** Se agregó la imagen del logo a los archivos estáticos y se reemplazó la F del navbar y del footer.
- **Uso y adaptación:** Ajusté el tamaño, el recorte y el fondo celeste con CSS para que el logo se vea correctamente en ambas ubicaciones. No cambié el contenido de los productos ni la estructura de la navegación.

## Parte 2: Explicación personal del proceso

Usé la IA como apoyo para mejorar la interfaz y agregar funciones sin perder lo que ya estaba construido.
Primero le pedí revisar la navegación para separar las opciones de clientes, visitantes y administradores.
La propuesta del navbar y del footer me sirvió como base, pero revisé los enlaces y corregí los que no abrían correctamente.
Después solicité ayuda para agregar las imágenes y aprendí a relacionarlas con el nombre exacto de cada producto.
Tuve que comprobar el fixture porque “Newer Hammer” no existía y no quise inventar un registro en la base de datos.
Para el carro pedí una solución basada en sesiones que permitiera agregar productos, modificar cantidades y pagar.
La primera implementación no reservaba stock al agregar, por lo que pedí ajustarla al requerimiento de la evaluación.
También corregí la lógica para que el pago no descontara nuevamente las unidades ya reservadas.
Con las pruebas confirmé que quitar un producto o reducir su cantidad devuelve el stock disponible.
Luego pedí apoyo para crear páginas reales de ayuda y términos, en lugar de usar solamente enlaces internos del footer.
Adapté los textos para explicar de forma clara que la empresa es una ferretería y que el pago es demostrativo.
Para la cuenta de administrador solicité un cambio visual y revisé que el tema solo se aplicara a usuarios autorizados.
El fondo cyan y los colores azul y morado se implementaron con clases CSS dentro de la plantilla base.
Finalmente reemplacé la letra F naranja por la imagen del logo y ajusté su tamaño para navbar y footer.
La IA me entregó una orientación inicial, pero yo tuve que probar, corregir rutas y revisar el comportamiento con Django.
Aprendí que no basta con copiar una respuesta: debo entender cómo se relacionan las sesiones, el ORM, las plantillas y las pruebas.
