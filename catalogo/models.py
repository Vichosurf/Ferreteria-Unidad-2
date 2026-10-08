from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models


class ConfiguracionSitio(models.Model):
    color_fondo = models.CharField(
        'color de fondo',
        max_length=7,
        default='#f3f5f7',
        validators=[
            RegexValidator(
                regex=r'^#[0-9a-fA-F]{6}$',
                message='Ingresa un color hexadecimal, por ejemplo #f3f5f7.',
            ),
        ],
    )

    class Meta:
        verbose_name = 'configuración del sitio'
        verbose_name_plural = 'configuración del sitio'

    def __str__(self):
        return f'Fondo del catálogo: {self.color_fondo}'


class Producto(models.Model):
    CATEGORIAS = [
        ('Herramientas manuales', 'Herramientas manuales'),
        ('Herramientas eléctricas', 'Herramientas eléctricas'),
        ('Fijaciones', 'Fijaciones'),
        ('Pinturas', 'Pinturas'),
        ('Electricidad', 'Electricidad'),
        ('Seguridad', 'Seguridad'),
        ('Construcción', 'Construcción'),
        ('Jardín', 'Jardín'),
    ]

    nombre = models.CharField('nombre', max_length=100)
    categoria = models.CharField('categoría', max_length=50, choices=CATEGORIAS)
    precio = models.PositiveIntegerField(
        'precio en pesos chilenos',
        validators=[MinValueValidator(1000), MaxValueValidator(150000)],
    )
    stock = models.PositiveSmallIntegerField(
        'unidades en stock',
        validators=[MinValueValidator(0), MaxValueValidator(50)],
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre


class ConsultaCliente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultas_ferreteria',
        verbose_name='cliente',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultas',
        verbose_name='producto de interés',
    )
    mensaje = models.TextField('consulta')
    creada_en = models.DateTimeField('fecha de envío', auto_now_add=True)

    class Meta:
        ordering = ['-creada_en']
        verbose_name = 'consulta de cliente'
        verbose_name_plural = 'consultas de clientes'

    def __str__(self):
        return f'Consulta de {self.usuario}'


class Compra(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compras_ferreteria',
        verbose_name='cliente',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='compras',
        verbose_name='producto',
    )
    nombre_producto = models.CharField('producto comprado', max_length=100)
    precio_unitario = models.PositiveIntegerField('precio unitario')
    cantidad = models.PositiveSmallIntegerField('cantidad')
    creada_en = models.DateTimeField('fecha de compra', auto_now_add=True)

    class Meta:
        ordering = ['-creada_en']
        verbose_name = 'compra'
        verbose_name_plural = 'compras'

    @property
    def total(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f'{self.nombre_producto} x {self.cantidad} ({self.usuario})'


class AvisoCliente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avisos_ferreteria',
        verbose_name='cliente',
    )
    mensaje = models.CharField('notificación', max_length=240)
    creado_en = models.DateTimeField('fecha', auto_now_add=True)
    leido = models.BooleanField('leído', default=False)

    class Meta:
        ordering = ['-creado_en']
        verbose_name = 'notificación de cliente'
        verbose_name_plural = 'notificaciones de clientes'

    def __str__(self):
        return f'{self.usuario}: {self.mensaje}'
