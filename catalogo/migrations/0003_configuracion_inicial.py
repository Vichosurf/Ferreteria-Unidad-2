from django.db import migrations


def crear_configuracion_inicial(apps, schema_editor):
    configuracion = apps.get_model('catalogo', 'ConfiguracionSitio')
    configuracion.objects.using(schema_editor.connection.alias).get_or_create(
        pk=1,
        defaults={'color_fondo': '#f3f5f7'},
    )


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_configuracionsitio_consultacliente'),
    ]

    operations = [
        migrations.RunPython(
            crear_configuracion_inicial,
            migrations.RunPython.noop,
        ),
    ]
