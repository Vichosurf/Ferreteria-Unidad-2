from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
