from django.contrib import admin
from django import forms
from django.db import models

from .models import (
    AvisoCliente,
    Compra,
    ConfiguracionSitio,
    ConsultaCliente,
    Producto,
)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)


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
    list_display = ('usuario', 'producto', 'creada_en')
    search_fields = ('usuario__username', 'usuario__email', 'mensaje')
    list_filter = ('creada_en',)
    readonly_fields = ('usuario', 'producto', 'mensaje', 'creada_en')

    def has_add_permission(self, request):
        return False


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
