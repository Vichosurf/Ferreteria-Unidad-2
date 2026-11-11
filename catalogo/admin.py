from django import forms
from django.contrib import admin, messages
from django.db import models

from .models import (
    AvisoCliente,
    AvisoGlobal,
    Compra,
    ConfiguracionSitio,
    ConsultaCliente,
    Producto,
    ProductoGuardado,
)

admin.site.site_header = 'Ferretería Vega · Administración'
admin.site.site_title = 'Administración | Ferretería Vega'
admin.site.index_title = 'Panel de administración'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)
    list_per_page = 25


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ('color_fondo',)
    fields = ('color_fondo',)
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'type': 'color'})},
    }

    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsultaCliente)
class ConsultaClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'producto', 'creada_en')
    search_fields = ('nombre', 'correo', 'usuario__username', 'mensaje')
    list_filter = ('creada_en',)
    readonly_fields = ('usuario', 'creada_en')


@admin.register(ProductoGuardado)
class ProductoGuardadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'creado_en')
    search_fields = ('usuario__username', 'producto__nombre')
    readonly_fields = ('usuario', 'producto', 'creado_en')


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'nombre_producto',
        'cantidad',
        'precio_unitario',
        'creada_en',
    )
    search_fields = ('usuario__username', 'nombre_producto')
    list_filter = ('creada_en',)
    readonly_fields = (
        'usuario',
        'producto',
        'nombre_producto',
        'precio_unitario',
        'cantidad',
        'creada_en',
    )

    def has_add_permission(self, request):
        return False


@admin.register(AvisoCliente)
class AvisoClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'creado_en', 'leido')
    search_fields = ('usuario__username', 'mensaje')
    list_filter = ('leido', 'creado_en')
    readonly_fields = ('usuario', 'mensaje', 'creado_en')


@admin.register(AvisoGlobal)
class AvisoGlobalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'creado_en')
    search_fields = ('titulo', 'mensaje')
    list_filter = ('activo', 'creado_en')
    fields = ('titulo', 'mensaje', 'activo', 'creado_en')
    readonly_fields = ('creado_en',)

    def save_model(self, request, obj, form, change):
        if obj.activo:
            AvisoGlobal.objects.filter(activo=True).exclude(
                pk=obj.pk,
            ).update(activo=False)
        super().save_model(request, obj, form, change)
