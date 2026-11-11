from .models import AvisoGlobal, ConfiguracionSitio


def configuracion_sitio(request):
    configuracion = ConfiguracionSitio.objects.filter(pk=1).first()
    aviso_global = AvisoGlobal.objects.filter(activo=True).first()
    avisos_pendientes = 0
    if request.user.is_authenticated:
        avisos_pendientes = request.user.avisos_ferreteria.filter(
            leido=False,
        ).count()
    return {
        'configuracion': configuracion,
        'aviso_global': aviso_global,
        'avisos_pendientes': avisos_pendientes,
        'carrito_cantidad': sum(
            int(cantidad)
            for cantidad in request.session.get('carrito', {}).values()
            if str(cantidad).isdigit()
        ),
        'idioma_actual': request.session.get('idioma', 'es'),
        'tema_actual': request.session.get('tema', 'light'),
    }
