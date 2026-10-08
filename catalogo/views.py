from django.shortcuts import render

from .models import Producto


ICONOS_CATEGORIA = {
    'Herramientas manuales': '🔨',
    'Herramientas eléctricas': '🛠️',
    'Fijaciones': '🔩',
    'Pinturas': '🎨',
    'Electricidad': '💡',
    'Seguridad': '🦺',
    'Construcción': '🧱',
    'Jardín': '🌱',
}


def inicio(request):
    productos = Producto.objects.all()
    for producto in productos:
        producto.icono = ICONOS_CATEGORIA.get(producto.categoria, '🔧')

    return render(request, 'catalogo/inicio.html', {'productos': productos})
