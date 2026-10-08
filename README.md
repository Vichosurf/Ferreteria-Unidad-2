# Catálogo Online - Ferretería

Aplicación web desarrollada con Django para administrar y consultar un catálogo
de productos de ferretería. El proyecto usa SQLite, Django ORM y Django Admin.

## Requisitos

- Python 3.12 o una versión compatible con Django indicada en `requirements.txt`.
- Git para clonar el repositorio.

## Instalación en Windows

Abre PowerShell en la carpeta donde quieras guardar el proyecto y ejecuta:

```powershell
git clone https://github.com/Vichosurf/Ferreteria-Unidad-2.git
cd Ferreteria-Unidad-2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata productos
python manage.py createsuperuser
python manage.py runserver
```

Si PowerShell bloquea la activación del entorno virtual, puedes ejecutar los
comandos de instalación y Django usando directamente
`.venv\Scripts\python.exe`.

Abre <http://127.0.0.1:8000/> para ver la aplicación y
<http://127.0.0.1:8000/admin/> para entrar al panel administrativo.

## Funcionalidades

- El catálogo está disponible en `/comprar/`. Se puede explorar como invitado,
  buscar productos, filtrar por categoría y abrir el detalle de cada producto.
- Las personas pueden crear una cuenta e iniciar o cerrar sesión. La portada
  ofrece acceso al catálogo y a la consulta de productos.
- Para registrar una compra de demostración hay que iniciar sesión o crear una
  cuenta. No se procesa ningún pago; una compra válida descuenta unidades del
  stock y se guarda en el historial del usuario.
- El formulario de consultas se encuentra en `/consultas/nueva/` y requiere
  iniciar sesión. El usuario puede revisar sus compras y notificaciones desde
  las páginas de su cuenta.
- El panel Django Admin permite administrar productos y revisar consultas,
  compras y notificaciones. La configuración del sitio permite cambiar el color
  de fondo.
- Las preferencias de idioma, tema y notificaciones se guardan en la sesión del
  navegador. El reloj se muestra según la zona horaria de Santiago.

El superusuario es local a cada instalación. Créalo con
`python manage.py createsuperuser`; no se incluyen credenciales en el repositorio.

## Productos iniciales

La fixture `catalogo/fixtures/productos.json` contiene los 40 productos de la
variante A. Se carga con:

```powershell
python manage.py loaddata productos
```

Existe también una fixture opcional con cinco productos adicionales:

```powershell
python manage.py loaddata productos_adicionales
```

## Pruebas y verificaciones

Ejecuta las pruebas de la aplicación:

```powershell
python manage.py test catalogo
```

Comprueba la configuración y que no falten migraciones:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```
