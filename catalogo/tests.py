from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import ConfiguracionSitio, ConsultaCliente, Producto


class CatalogoTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Martillo de prueba',
            categoria='Herramientas manuales',
            precio=5990,
            stock=12,
        )
        self.producto_agotado = Producto.objects.create(
            nombre='Pintura agotada',
            categoria='Pinturas',
            precio=12000,
            stock=0,
        )

    def test_portada_muestra_productos_de_la_base_de_datos(self):
        response = self.client.get(reverse('catalogo'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.nombre)
        self.assertContains(response, 'productos disponibles')
        self.assertContains(response, 'Agotado')
        self.assertTemplateUsed(response, 'catalogo/catalogo.html')

    def test_invitado_puede_explorar_tarjetas_sin_comprar(self):
        response = self.client.get(reverse('catalogo'))

        self.assertContains(response, 'Explora el catálogo')
        self.assertContains(response, 'Iniciar sesión para comprar')
        self.assertContains(response, 'catalogo/images/productos.svg#manuales')
        self.assertNotContains(response, 'name="cantidad"')
        self.assertContains(
            response,
            reverse('detalle_producto', args=[self.producto.pk]),
        )

        respuesta_compra = self.client.post(
            reverse('comprar_producto', args=[self.producto.pk]),
            {'cantidad': 1},
        )
        self.assertEqual(respuesta_compra.status_code, 302)
        self.assertIn(reverse('iniciar_sesion'), respuesta_compra.url)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 12)

    def test_cliente_autenticado_puede_comprar_desde_tarjeta(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_catalogo',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        response = self.client.get(reverse('catalogo'))

        self.assertContains(response, 'Encuentra lo que necesitas')
        self.assertContains(response, 'name="cantidad"')
        self.assertContains(
            response,
            reverse('comprar_producto', args=[self.producto.pk]),
        )

    def test_inicio_ofrece_consultar_o_comprar(self):
        response = self.client.get(reverse('inicio'))
        self.assertContains(response, 'Enviar una consulta')
        self.assertContains(response, 'Continuar como invitado')
        self.assertTemplateUsed(response, 'catalogo/inicio.html')

    def test_busqueda_filtro_y_detalle_producto(self):
        respuesta = self.client.get(reverse('catalogo'), {'q': 'Martillo'})
        self.assertContains(respuesta, self.producto.nombre)
        self.assertNotContains(respuesta, self.producto_agotado.nombre)

        respuesta = self.client.get(
            reverse('catalogo'),
            {'categoria': 'Pinturas'},
        )
        self.assertContains(respuesta, self.producto_agotado.nombre)
        self.assertContains(
            self.client.get(
                reverse('detalle_producto', args=[self.producto.pk])
            ),
            self.producto.nombre,
        )
        self.assertEqual(
            self.client.get(
                reverse('detalle_producto', args=[9999])
            ).status_code,
            404,
        )

    def test_admin_permite_crear_editar_y_eliminar_productos(self):
        usuario = get_user_model().objects.create_superuser(
            username='admin_prueba',
            email='admin@example.com',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        lista_admin = reverse('admin:catalogo_producto_changelist')
        self.assertEqual(self.client.get(lista_admin).status_code, 200)

        agregar = reverse('admin:catalogo_producto_add')
        respuesta = self.client.post(agregar, {
            'nombre': 'Taladro de prueba',
            'categoria': 'Herramientas eléctricas',
            'precio': 45000,
            'stock': 6,
            '_save': 'Guardar',
        })
        self.assertEqual(respuesta.status_code, 302)
        producto = Producto.objects.get(nombre='Taladro de prueba')
        self.assertContains(
            self.client.get(reverse('catalogo')),
            'Taladro de prueba',
        )

        editar = reverse('admin:catalogo_producto_change', args=[producto.pk])
        respuesta = self.client.post(editar, {
            'nombre': 'Taladro actualizado',
            'categoria': 'Herramientas eléctricas',
            'precio': 48000,
            'stock': 4,
            '_save': 'Guardar',
        })
        self.assertEqual(respuesta.status_code, 302)
        producto.refresh_from_db()
        self.assertEqual(producto.precio, 48000)

        eliminar = reverse('admin:catalogo_producto_delete', args=[producto.pk])
        respuesta = self.client.post(eliminar, {'post': 'yes'})
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())
        respuesta = self.client.get(reverse('catalogo'))
        self.assertNotIn(producto, respuesta.context['productos'])

    def test_cliente_se_registra_inicia_sesion_y_envia_consulta(self):
        respuesta = self.client.post(reverse('registro'), {
            'username': 'cliente_es2',
            'email': 'cliente@example.com',
            'password1': 'Clave-segura-para-prueba-2026!',
            'password2': 'Clave-segura-para-prueba-2026!',
        })

        self.assertRedirects(respuesta, reverse('consulta'))
        self.assertTrue(respuesta.wsgi_request.user.is_authenticated)

        respuesta = self.client.post(reverse('consulta'), {
            'producto': self.producto.pk,
            'mensaje': '¿Tienen despacho en la comuna?',
        })
        self.assertRedirects(respuesta, reverse('consulta_enviada'))
        consulta = ConsultaCliente.objects.get()
        self.assertEqual(consulta.usuario.username, 'cliente_es2')
        self.assertEqual(consulta.producto, self.producto)
        respuesta = self.client.get(
            reverse('consulta'),
            {'producto': self.producto.pk},
        )
        self.assertEqual(
            respuesta.context['form']['producto'].value(),
            self.producto.pk,
        )

    def test_consulta_exige_iniciar_sesion(self):
        respuesta = self.client.get(reverse('consulta'))

        self.assertRedirects(
            respuesta,
            f'{reverse("iniciar_sesion")}?next={reverse("consulta")}',
        )
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_cerrar_sesion_redirige_al_inicio(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_cierre',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        respuesta = self.client.post(reverse('cerrar_sesion'))

        self.assertRedirects(respuesta, reverse('inicio'))
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)

    def test_admin_puede_cambiar_color_de_fondo(self):
        self.assertTrue(ConfiguracionSitio.objects.filter(pk=1).exists())
        usuario = get_user_model().objects.create_superuser(
            username='admin_color',
            email='admin-color@example.com',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        editar = reverse(
            'admin:catalogo_configuracionsitio_change',
            args=[1],
        )
        respuesta = self.client.post(editar, {
            'color_fondo': '#123456',
            '_save': 'Guardar',
        })

        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(
            ConfiguracionSitio.objects.get(pk=1).color_fondo,
            '#123456',
        )
        respuesta = self.client.get(reverse('catalogo'))
        self.assertContains(respuesta, '#123456')

    def test_compra_demo_descuenta_stock_y_guarda_historial_y_aviso(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_compra',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        respuesta = self.client.post(
            reverse('comprar_producto', args=[self.producto.pk]),
            {'cantidad': 2},
        )

        self.assertRedirects(respuesta, reverse('historial'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        compra = usuario.compras_ferreteria.get()
        self.assertEqual(compra.cantidad, 2)
        self.assertEqual(compra.total, 11980)
        self.assertContains(self.client.get(reverse('historial')), 'Martillo de prueba')
        self.assertContains(
            self.client.get(reverse('notificaciones')),
            'Compra registrada',
        )

    def test_no_permite_comprar_mas_stock_disponible(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_sin_stock',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        self.client.post(
            reverse('comprar_producto', args=[self.producto.pk]),
            {'cantidad': 99},
        )

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 12)
        self.assertFalse(usuario.compras_ferreteria.exists())

    def test_configuracion_guarda_idioma_tema_y_notificaciones(self):
        respuesta = self.client.post(
            reverse('configuracion'),
            {'idioma': 'en', 'tema': 'dark', 'notificaciones': 'on'},
        )

        self.assertRedirects(respuesta, reverse('configuracion'))
        pagina = self.client.get(reverse('configuracion'))
        self.assertEqual(pagina.wsgi_request.session['idioma'], 'en')
        self.assertEqual(pagina.wsgi_request.session['tema'], 'dark')
        self.assertTrue(
            pagina.wsgi_request.session['notificaciones_activas'],
        )
        self.assertContains(pagina, '<html lang="en">', html=False)
        self.assertContains(pagina, 'tema-oscuro')

    def test_fixture_principal_y_adicional(self):
        call_command('loaddata', 'productos', verbosity=0)
        self.assertEqual(Producto.objects.count(), 40)

        call_command('loaddata', 'productos_adicionales', verbosity=0)
        self.assertEqual(Producto.objects.count(), 45)
        self.assertTrue(
            Producto.objects.filter(
                nombre='Extensión eléctrica reforzada 10 m',
            ).exists(),
        )
