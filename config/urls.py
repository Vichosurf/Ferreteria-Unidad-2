"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalogo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'productos/<int:producto_id>/',
        views.detalle_producto,
        name='detalle_producto',
    ),
    path('', views.inicio, name='inicio'),
    path('comprar/', views.catalogo, name='catalogo'),
    path(
        'productos/<int:producto_id>/comprar/',
        views.comprar_producto,
        name='comprar_producto',
    ),
    path('cuenta/registro/', views.registro, name='registro'),
    path(
        'cuenta/iniciar-sesion/',
        views.IniciarSesionView.as_view(),
        name='iniciar_sesion',
    ),
    path(
        'cuenta/cerrar-sesion/',
        views.CerrarSesionView.as_view(),
        name='cerrar_sesion',
    ),
    path('consultas/nueva/', views.CrearConsultaView.as_view(), name='consulta'),
    path(
        'consultas/enviada/',
        views.consulta_enviada,
        name='consulta_enviada',
    ),
    path('mi-cuenta/historial/', views.historial, name='historial'),
    path(
        'mi-cuenta/notificaciones/',
        views.notificaciones,
        name='notificaciones',
    ),
    path(
        'mi-cuenta/configuracion/',
        views.configuracion,
        name='configuracion',
    ),
]
