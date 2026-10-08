# Catálogo de ferretería

Proyecto Django de la variante Ferretería para la Evaluación Sumativa 2. Permite administrar productos con Django Admin y mostrar en la portada el catálogo guardado en SQLite.

## Requisitos

- Python compatible con la versión de Django indicada en `requirements.txt`.
- Git, para clonar el repositorio.

## Instalación y ejecución

Desde la carpeta del proyecto, en PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata catalogo/fixtures/productos.json
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` para ver el catálogo y `http://127.0.0.1:8000/admin/` para administrar los productos con la cuenta de superusuario creada localmente.

La fixture carga 40 productos de ejemplo. Si se vuelve a cargar, Django actualizará los registros con los mismos identificadores primarios. No se incluyen credenciales de administrador en el repositorio.

## Estructura principal

- `catalogo/models.py`: modelo `Producto` y sus campos.
- `catalogo/admin.py`: columnas, búsqueda y filtro del administrador.
- `catalogo/fixtures/productos.json`: datos iniciales de la variante Ferretería.
- `catalogo/views.py`: consulta de productos mediante el ORM.
- `catalogo/templates/catalogo/inicio.html`: tarjetas del catálogo.
- `config/settings.py`: configuración del proyecto y base de datos SQLite.

Las imágenes de las tarjetas son símbolos ilustrativos por categoría; no son fotografías de productos. La aplicación de esta entrega muestra el catálogo y permite administrarlo desde Django Admin.
