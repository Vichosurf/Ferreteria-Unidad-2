from .models import ConfiguracionSitio


def configuracion_sitio(request):
    configuracion = ConfiguracionSitio.objects.filter(pk=1).first()
    avisos_pendientes = 0
    if request.user.is_authenticated:
        avisos_pendientes = request.user.avisos_ferreteria.filter(
            leido=False,
        ).count()
    return {
        'configuracion': configuracion,
        'avisos_pendientes': avisos_pendientes,
        'idioma_actual': request.session.get('idioma', 'es'),
        'tema_actual': request.session.get('tema', 'light'),
    }
