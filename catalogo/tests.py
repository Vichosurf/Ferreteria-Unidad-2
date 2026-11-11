from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import (
    Compra,
    ConfiguracionSitio,
    ConsultaCliente,
    AvisoGlobal,
    Producto,
    ProductoGuardado,
)


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

    def test_alargador_muestra_su_imagen_especifica(self):
        alargador = Producto.objects.create(
            nombre='Alargador eléctrico 5 metros',
            categoria='Electricidad',
            precio=8990,
            stock=10,
        )

        respuesta = self.client.get(
            reverse('detalle_producto', args=[alargador.pk]),
        )

        self.assertContains(respuesta, 'catalogo/images/alargador-electrico-5m.png')
        self.assertContains(respuesta, 'Alargador eléctrico de 5 metros')

    def test_productos_adicionales_muestran_sus_imagenes_especificas(self):
        productos = (
            (
                'Alicate universal 8 pulgadas',
                'catalogo/images/alicate-universal-8-pulgadas.png',
            ),
            (
                'Ampolleta LED luz cálida 9 W',
                'catalogo/images/ampolleta-led-luz-calida-9w.png',
            ),
            (
                'Atornillador inalámbrico 12 V',
                'catalogo/images/atornillador-inalambrico-12v.png',
            ),
            (
                'Tornillo para madera 2 pulgadas, caja 100 unidades',
                'catalogo/images/tornillo-madera-2-pulgadas.png',
            ),
            (
                'Tijera de podar 8 pulgadas',
                'catalogo/images/tijera-podar-8-pulgadas.png',
            ),
            (
                'Tarugo nylon 8 mm, bolsa 50 unidades',
                'catalogo/images/tarugo-nylon-8mm.png',
            ),
            (
                'Taladro percutor 650 W',
                'catalogo/images/taladro-percutor-650w.png',
            ),
            (
                'Sierra circular 7 1/4 pulgadas',
                'catalogo/images/sierra-circular-7-1-4-pulgadas.png',
            ),
            (
                'Set de destornilladores 6 piezas',
                'catalogo/images/set-destornilladores-6-piezas.png',
            ),
            (
                'Set de brocas para madera 8 piezas',
                'catalogo/images/set-brocas-madera-8-piezas.png',
            ),
            (
                'Serrucho carpintero 20 pulgadas',
                'catalogo/images/serrucho-carpintero-20-pulgadas.png',
            ),
            (
                'Rodillo antigota 18 cm',
                'catalogo/images/rodillo-antigota-18cm.png',
            ),
            (
                'Plancha yeso cartón 10 mm',
                'catalogo/images/plancha-yeso-carton-10mm.png',
            ),
            (
                'Pistola de silicona eléctrica',
                'catalogo/images/pistola-silicona-electrica.png',
            ),
            (
                'Pintura látex interior blanco 1 galón',
                'catalogo/images/pintura-latex-interior-blanco-1-galon.png',
            ),
            (
                'Perno hexagonal galvanizado 3/8 pulgada',
                'catalogo/images/perno-hexagonal-galvanizado-3-8-pulgada.png',
            ),
            (
                'Bisagra zincada 3 pulgadas, par',
                'catalogo/images/bisagra-zincada-3-pulgadas-par.png',
            ),
            (
                'Pala jardín mango de madera',
                'catalogo/images/pala-jardin-mango-madera.png',
            ),
            (
                'Nivel de aluminio 60 cm',
                'catalogo/images/nivel-aluminio-60cm.png',
            ),
            (
                'Mascarilla respiratoria con filtro',
                'catalogo/images/mascarilla-respiratoria-filtro.png',
            ),
            (
                'Broca para concreto 8 mm',
                'catalogo/images/broca-concreto-8mm.png',
            ),
            (
                'Brocha profesional 2 pulgadas',
                'catalogo/images/brocha-profesional-2-pulgadas.png',
            ),
            (
                'Candado de bronce 40 mm',
                'catalogo/images/candado-bronce-40mm.png',
            ),
            (
                'Martillo de carpintero 16 oz',
                'catalogo/images/martillo-carpintero-16oz.png',
            ),
            (
                'Casco de seguridad blanco',
                'catalogo/images/casco-seguridad-blanco.png',
            ),
            (
                'Cemento corriente 25 kg',
                'catalogo/images/cemento-corriente-25kg.png',
            ),
            (
                'Cinta aisladora negra 20 metros',
                'catalogo/images/cinta-aisladora-negra-20m.png',
            ),
            (
                'Cinta métrica 5 metros',
                'catalogo/images/cinta-metrica-5m.png',
            ),
            (
                'Manguera jardín reforzada 15 metros',
                'catalogo/images/manguera-jardin-reforzada-15m.png',
            ),
            (
                'Llave ajustable 10 pulgadas',
                'catalogo/images/llave-ajustable-10-pulgadas.png',
            ),
            (
                'Lijadora orbital 240 W',
                'catalogo/images/lijadora-orbital-240w.png',
            ),
            (
                'Lija para madera grano 120, paquete',
                'catalogo/images/lija-madera-grano-120-paquete.png',
            ),
            (
                'Lentes de seguridad transparentes',
                'catalogo/images/lentes-seguridad-transparentes.png',
            ),
            (
                'Interruptor simple embutido',
                'catalogo/images/interruptor-simple-embutido.png',
            ),
            (
                'Guantes de cabritilla reforzados',
                'catalogo/images/guantes-cabritilla-reforzados.png',
            ),
            (
                'Clavo corriente 2 pulgadas, kilo',
                'catalogo/images/clavo-corriente-2-pulgadas-kilo.png',
            ),
            (
                'Esmalte al agua azul 1 galón',
                'catalogo/images/esmalte-agua-azul-1-galon.png',
            ),
            (
                'Esmeril angular 4 1/2 pulgadas',
                'catalogo/images/esmeril-angular-4-1-2-pulgadas.png',
            ),
            (
                'Formón para madera 25 mm',
                'catalogo/images/formon-madera-25mm.png',
            ),
        )
        for nombre, imagen in productos:
            producto = Producto.objects.create(
                nombre=nombre,
                categoria='Electricidad',
                precio=8990,
                stock=10,
            )
            respuesta = self.client.get(
                reverse('detalle_producto', args=[producto.pk]),
            )
            self.assertContains(respuesta, imagen)

    def test_invitado_puede_explorar_tarjetas_sin_comprar(self):
        response = self.client.get(reverse('catalogo'))

        self.assertContains(response, 'Todo Material que necesitas para tu hogar')
        self.assertContains(response, 'Iniciar sesión para comprar')
        self.assertContains(response, 'catalogo/images/productos.svg#manuales')
        self.assertNotContains(response, 'name="cantidad"')
        self.assertContains(
            response,
            reverse('detalle_producto', args=[self.producto.pk]),
        )
        self.assertNotContains(response, 'Acceso administrador')
        self.assertNotContains(
            response,
            reverse('reporte_resumen_categorias'),
        )
        self.assertNotContains(
            response,
            reverse('reporte_stock_critico'),
        )

        respuesta_compra = self.client.post(
            reverse('comprar_producto', args=[self.producto.pk]),
            {'cantidad': 1},
        )
        self.assertEqual(respuesta_compra.status_code, 302)
        self.assertIn(reverse('iniciar_sesion'), respuesta_compra.url)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 12)

    def test_staff_ve_agregar_unidades_en_catalogo_y_accesos_en_footer(self):
        usuario = get_user_model().objects.create_user(
            username='gestor_navbar',
            password='clave-temporal-de-prueba',
            is_staff=True,
        )
        self.client.force_login(usuario)

        respuesta = self.client.get(reverse('catalogo'))

        self.assertContains(respuesta, 'Agregar unidades')
        self.assertContains(respuesta, 'Agregar producto')
        self.assertContains(respuesta, 'Panel de administración')
        self.assertContains(respuesta, reverse('admin:index'))
        self.assertNotContains(respuesta, 'Administración Django')
        self.assertContains(
            respuesta,
            reverse('reporte_resumen_categorias'),
        )
        self.assertContains(
            respuesta,
            reverse('reporte_stock_critico'),
        )
        self.assertNotContains(respuesta, 'Acceso administrador')

    def test_cliente_autenticado_puede_comprar_desde_tarjeta(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_catalogo',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        response = self.client.get(reverse('catalogo'))

        self.assertContains(response, 'Todo Material que necesitas para tu hogar')
        self.assertContains(response, 'Ya iniciaste sesión')
        self.assertContains(response, 'name="cantidad"')
        self.assertContains(
            response,
            reverse('carrito_agregar', args=[self.producto.pk]),
        )

    def test_inicio_muestra_opciones_de_acceso_y_catalogo_para_invitados(self):
        response = self.client.get(reverse('inicio'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Todo para tus proyectos, en un solo lugar')
        self.assertContains(response, 'Iniciar sesión')
        self.assertContains(response, 'Crear cuenta')
        self.assertContains(response, 'Explorar productos sin iniciar sesión')
        self.assertContains(response, 'catalogo/images/logo-ferreteria.png')
        self.assertContains(response, 'No solicitamos datos de pago')
        self.assertContains(response, 'Términos y condiciones')
        self.assertContains(response, 'Nuestra empresa')
        self.assertContains(response, 'Servicio al cliente')
        self.assertNotContains(response, self.producto.nombre)
        self.assertNotContains(response, 'Panel de administración')
        self.assertTemplateUsed(response, 'catalogo/inicio.html')

    def test_panel_de_administracion_solo_se_muestra_a_personal_autenticado(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertNotContains(respuesta, 'Panel de administración')
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)

        usuario = get_user_model().objects.create_user(
            username='cliente_panel',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)
        respuesta = self.client.get(reverse('inicio'))
        self.assertNotContains(respuesta, 'Panel de administración')
        self.assertEqual(
            self.client.get(reverse('panel_administracion')).status_code,
            403,
        )
        self.client.logout()

        administrador = get_user_model().objects.create_user(
            username='admin_panel',
            password='clave-temporal-de-prueba',
            is_staff=True,
        )
        respuesta = self.client.post(reverse('iniciar_sesion'), {
            'username': 'admin_panel',
            'password': 'clave-temporal-de-prueba',
        })
        self.assertRedirects(respuesta, reverse('inicio'))
        self.assertTrue(respuesta.wsgi_request.user.is_staff)
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, 'Panel de administración')
        self.assertContains(respuesta, reverse('admin:index'))
        self.assertEqual(
            self.client.get(reverse('panel_administracion')).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse('admin:index')).status_code,
            200,
        )

    def test_admin_puede_restaurar_productos_del_fixture_sin_sobrescribir(self):
        administrador = get_user_model().objects.create_superuser(
            username='admin_restauracion',
            email='admin-restauracion@example.com',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(administrador)
        url = reverse('panel_administracion')

        self.producto.nombre = 'Producto conservado del catálogo'
        self.producto.save()
        self.producto_agotado.delete()

        respuesta = self.client.post(
            url,
            {'accion': 'restaurar_catalogo'},
            follow=True,
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Se restauraron 54 productos faltantes')
        self.assertEqual(Producto.objects.count(), 55)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto conservado del catálogo')
        self.assertTrue(
            Producto.objects.filter(
                pk=2,
                nombre='Set de destornilladores 6 piezas',
            ).exists(),
        )

        respuesta = self.client.post(
            url,
            {'accion': 'restaurar_catalogo'},
            follow=True,
        )
        self.assertContains(respuesta, 'Se restauraron 0 productos faltantes')
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto conservado del catálogo')

    def test_admin_publica_aviso_visible_a_clientes_y_visitantes(self):
        aviso_anterior = AvisoGlobal.objects.create(
            titulo='Aviso anterior',
            mensaje='Este mensaje dejará de publicarse.',
        )
        administrador = get_user_model().objects.create_superuser(
            username='admin_avisos_globales',
            email='admin-avisos@example.com',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(administrador)

        panel = self.client.get(reverse('panel_administracion'))
        self.assertContains(panel, 'Panel de administración')
        self.assertContains(panel, 'Agregar producto')
        self.assertContains(panel, 'Publicar aviso')
        self.assertContains(panel, 'Recuperar productos faltantes')
        self.assertContains(panel, 'aria-label="Volver a la página de Ferretería Vega"')
        self.assertNotContains(panel, 'Django site admin')
        self.assertNotContains(panel, 'vega-admin-card')
        self.assertEqual(
            self.client.get(reverse('admin:index')).status_code,
            200,
        )

        respuesta = self.client.post(
            reverse('panel_administracion'),
            {
                'accion': 'publicar_aviso',
                'titulo': 'Horario especial',
                'mensaje': 'Este sábado atenderemos hasta las 14:00.',
            },
        )
        self.assertRedirects(
            respuesta,
            reverse('panel_administracion'),
        )
        aviso_anterior.refresh_from_db()
        self.assertFalse(aviso_anterior.activo)
        self.assertTrue(
            AvisoGlobal.objects.get(titulo='Horario especial').activo,
        )

        self.client.logout()
        portada = self.client.get(reverse('inicio'))
        catalogo = self.client.get(reverse('catalogo'))
        self.assertContains(portada, 'Horario especial')
        self.assertContains(
            portada,
            'Este sábado atenderemos hasta las 14:00.',
        )
        self.assertContains(catalogo, 'Horario especial')
        self.assertNotContains(portada, 'Aviso anterior')

        cliente = get_user_model().objects.create_user(
            username='cliente_aviso_global',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(cliente)
        portada_cliente = self.client.get(reverse('inicio'))
        self.assertContains(portada_cliente, 'Horario especial')

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

    def test_detalle_guarda_los_ultimos_tres_productos_en_sesion(self):
        productos = [self.producto]
        for numero in range(2, 5):
            productos.append(Producto.objects.create(
                nombre=f'Producto visitado {numero}',
                categoria='Electricidad',
                precio=3000 + numero,
                stock=numero,
            ))

        for producto in productos:
            self.client.get(reverse('detalle_producto', args=[producto.pk]))

        respuesta = self.client.get(
            reverse('detalle_producto', args=[productos[0].pk]),
        )
        self.assertEqual(
            respuesta.wsgi_request.session['productos_visitados'],
            [str(productos[0].pk), str(productos[3].pk), str(productos[2].pk)],
        )
        self.assertContains(respuesta, 'Últimos productos visitados')

    def test_formulario_consulta_rechaza_correo_y_mensaje_invalidos(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_validacion',
            email='cliente@example.com',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)
        respuesta = self.client.post(reverse('consulta'), {
            'nombre': 'A',
            'correo': 'correo-no-valido',
            'producto': self.producto.pk,
            'mensaje': 'corto',
        })

        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.context['form'].errors['correo'])
        self.assertContains(respuesta, 'al menos 10 caracteres')
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_formulario_consulta_guarda_nombre_correo_y_producto(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_consulta',
            email='cuenta@example.com',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)
        respuesta = self.client.post(reverse('consulta'), {
            'nombre': 'Cliente de prueba',
            'correo': 'contacto@example.com',
            'producto': self.producto.pk,
            'mensaje': '¿Tienen despacho disponible?',
        })

        self.assertRedirects(respuesta, reverse('consulta_enviada'))
        consulta = ConsultaCliente.objects.get()
        self.assertEqual(consulta.nombre, 'Cliente de prueba')
        self.assertEqual(consulta.correo, 'contacto@example.com')
        self.assertEqual(consulta.producto, self.producto)
        self.assertEqual(consulta.usuario, usuario)

    def test_formulario_consulta_requiere_csrf(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_csrf',
            password='clave-temporal-de-prueba',
        )
        cliente = self.client_class(enforce_csrf_checks=True)
        cliente.force_login(usuario)
        respuesta = cliente.post(reverse('consulta'), {
            'nombre': 'Cliente CSRF',
            'correo': 'csrf@example.com',
            'mensaje': 'Mensaje válido para la consulta.',
        })

        self.assertEqual(respuesta.status_code, 403)
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_reporte_resumen_agrupa_y_calcula_con_orm(self):
        Producto.objects.create(
            nombre='Alicate adicional',
            categoria='Herramientas manuales',
            precio=10000,
            stock=8,
        )

        respuesta = self.client.get(reverse('reporte_resumen_categorias'))

        self.assertEqual(respuesta.status_code, 200)
        manuales = next(
            item for item in respuesta.context['resumenes']
            if item['categoria'] == 'Herramientas manuales'
        )
        self.assertEqual(manuales['cantidad'], 2)
        self.assertEqual(manuales['precio_promedio'], 7995)
        self.assertEqual(manuales['stock_total'], 20)

    def test_reporte_stock_critico_filtra_y_ordena_con_orm(self):
        Producto.objects.create(
            nombre='Producto crÃ­tico',
            categoria='Electricidad',
            precio=3500,
            stock=3,
        )
        Producto.objects.create(
            nombre='Producto sobre umbral',
            categoria='Electricidad',
            precio=3500,
            stock=6,
        )

        respuesta = self.client.get(reverse('reporte_stock_critico'))

        self.assertEqual(respuesta.status_code, 200)
        productos = list(respuesta.context['productos'])
        self.assertEqual(
            [producto.nombre for producto in productos],
            ['Pintura agotada', 'Producto crÃ­tico'],
        )
        self.assertNotContains(respuesta, 'Producto sobre umbral')
        self.assertContains(respuesta, '5 unidades o menos')

    def test_staff_crea_edita_y_elimina_producto_desde_el_catalogo(self):
        usuario = get_user_model().objects.create_user(
            username='gestor_catalogo',
            password='clave-temporal-de-prueba',
            is_staff=True,
        )
        self.client.force_login(usuario)
        listado = reverse('catalogo')

        respuesta = self.client.post(reverse('producto_crear'), {
            'nombre': 'Taladro nuevo',
            'categoria': 'Herramientas eléctricas',
            'precio': 45000,
            'stock': 6,
        })
        self.assertRedirects(respuesta, listado)
        producto = Producto.objects.get(nombre='Taladro nuevo')
        self.assertContains(self.client.get(listado), producto.nombre)

        respuesta = self.client.post(
            reverse('producto_editar', args=[producto.pk]),
            {
                'nombre': 'Taladro actualizado',
                'categoria': 'Herramientas eléctricas',
                'precio': 48000,
                'stock': 4,
            },
        )
        self.assertRedirects(respuesta, listado)
        producto.refresh_from_db()
        self.assertEqual(producto.precio, 48000)
        self.assertContains(self.client.get(listado), 'Taladro actualizado')

        url_eliminar = reverse('producto_eliminar', args=[producto.pk])
        respuesta = self.client.get(url_eliminar)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Confirmar eliminación')
        self.assertContains(respuesta, producto.nombre)

        respuesta = self.client.post(url_eliminar)
        self.assertRedirects(respuesta, listado)
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())
        self.assertNotContains(self.client.get(listado), 'Taladro actualizado')

    def test_crud_de_productos_requiere_personal_autorizado(self):
        url_crear = reverse('producto_crear')
        respuesta_invitado = self.client.get(url_crear)
        self.assertRedirects(
            respuesta_invitado,
            f'{reverse("iniciar_sesion")}?next={url_crear}',
        )

        usuario = get_user_model().objects.create_user(
            username='cliente_sin_permisos',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)
        self.assertEqual(self.client.get(url_crear).status_code, 403)
        respuesta = self.client.post(url_crear, {
            'nombre': 'Producto no autorizado',
            'categoria': 'Herramientas eléctricas',
            'precio': 45000,
            'stock': 6,
        })
        self.assertEqual(respuesta.status_code, 403)
        self.assertFalse(
            Producto.objects.filter(nombre='Producto no autorizado').exists(),
        )

    def test_producto_con_compras_no_se_elimina(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_compra_existente',
            password='clave-temporal-de-prueba',
        )
        gestor = get_user_model().objects.create_user(
            username='gestor_compra_existente',
            password='clave-temporal-de-prueba',
            is_staff=True,
        )
        Compra.objects.create(
            usuario=usuario,
            producto=self.producto,
            nombre_producto=self.producto.nombre,
            precio_unitario=self.producto.precio,
            cantidad=1,
        )
        self.client.force_login(gestor)

        respuesta = self.client.post(
            reverse('producto_eliminar', args=[self.producto.pk]),
            follow=True,
        )

        self.assertRedirects(respuesta, reverse('catalogo'))
        self.assertTrue(
            Producto.objects.filter(pk=self.producto.pk).exists(),
        )
        self.assertContains(respuesta, 'compras asociadas')

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

    def test_visitante_puede_abrir_contacto(self):
        respuesta = self.client.get(reverse('consulta'))

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todavía necesitas ayuda')
        self.assertContains(respuesta, 'Contáctanos')
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_carrito_agrega_y_paga_productos(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_carrito',
            password='clave-temporal-de-prueba',
        )
        respuesta = self.client.post(
            reverse('carrito_agregar', args=[self.producto.pk]),
            {'cantidad': 2, 'next': reverse('carrito')},
        )
        self.assertRedirects(respuesta, reverse('carrito'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        carrito = self.client.get(reverse('carrito'))
        self.assertContains(carrito, 'Mi carro de supermercado')
        self.assertContains(carrito, '$11980 CLP')
        self.assertContains(carrito, 'Iniciar sesión para pagar')

        self.client.force_login(usuario)
        respuesta = self.client.post(reverse('carrito_pagar'))
        self.assertRedirects(respuesta, reverse('historial'))
        self.assertEqual(Compra.objects.get(usuario=usuario).cantidad, 2)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        self.assertEqual(self.client.session.get('carrito'), {})

    def test_quitar_del_carrito_devuelve_stock_reservado(self):
        self.client.post(
            reverse('carrito_agregar', args=[self.producto.pk]),
            {'cantidad': 3},
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 9)

        respuesta = self.client.post(
            reverse('carrito_eliminar', args=[self.producto.pk]),
        )
        self.assertRedirects(respuesta, reverse('carrito'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 12)

    def test_paginas_de_ayuda_y_terminos_son_accesibles(self):
        ayuda = self.client.get(reverse('ayuda'))
        terminos = self.client.get(reverse('terminos'))
        self.assertEqual(ayuda.status_code, 200)
        self.assertContains(ayuda, 'Preguntas frecuentes')
        self.assertContains(ayuda, '¿Cómo agrego un producto al carro?')
        self.assertEqual(terminos.status_code, 200)
        self.assertContains(terminos, 'Términos y condiciones')
        self.assertContains(terminos, 'Carro y reserva de stock')

    def test_cerrar_sesion_redirige_al_inicio(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_cierre',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        cuenta = self.client.get(reverse('historial'))
        self.assertContains(cuenta, 'PERFIL')
        self.assertContains(cuenta, 'cliente_cierre')
        self.assertContains(cuenta, 'Mi historial')
        self.assertContains(cuenta, 'Cerrar sesión')
        self.assertContains(cuenta, 'name="csrfmiddlewaretoken"', html=False)
        self.assertContains(cuenta, 'Configuración')

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
        self.assertContains(respuesta, 'tema-administrador')

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

    def test_productos_guardados_se_crean_consultan_y_eliminan(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_guardados',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        respuesta = self.client.post(
            reverse('producto_guardar', args=[self.producto.pk]),
            {'next': reverse('catalogo')},
        )

        self.assertRedirects(respuesta, reverse('catalogo'))
        self.assertTrue(
            ProductoGuardado.objects.filter(
                usuario=usuario,
                producto=self.producto,
            ).exists(),
        )
        pagina = self.client.get(reverse('productos_guardados'))
        self.assertContains(pagina, self.producto.nombre)

        respuesta = self.client.post(
            reverse('producto_guardado_quitar', args=[self.producto.pk]),
        )
        self.assertRedirects(respuesta, reverse('productos_guardados'))
        self.assertFalse(ProductoGuardado.objects.filter(usuario=usuario).exists())

    def test_historial_muestra_compra_en_card(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_historial_card',
            password='clave-temporal-de-prueba',
        )
        Compra.objects.create(
            usuario=usuario,
            producto=self.producto,
            nombre_producto=self.producto.nombre,
            precio_unitario=self.producto.precio,
            cantidad=2,
        )
        self.client.force_login(usuario)

        pagina = self.client.get(reverse('historial'))

        self.assertContains(pagina, 'compra-card')
        self.assertContains(pagina, 'Precio unitario')
        self.assertContains(pagina, 'Total: $11980 CLP')

    def test_navbar_muestra_guardados_y_notificaciones(self):
        usuario = get_user_model().objects.create_user(
            username='cliente_navbar',
            password='clave-temporal-de-prueba',
        )
        self.client.force_login(usuario)

        pagina = self.client.get(reverse('catalogo'))

        self.assertContains(pagina, reverse('productos_guardados'))
        self.assertContains(pagina, 'producto-guardado.png')
        self.assertContains(pagina, reverse('notificaciones'))
        self.assertContains(pagina, 'notificaciones.png')
        self.assertContains(pagina, '>Avisos<', html=False)

    def test_fixture_principal_y_adicional(self):
        call_command('loaddata', 'productos', verbosity=0)
        self.assertEqual(Producto.objects.count(), 40)

        call_command('loaddata', 'productos_adicionales', verbosity=0)
        self.assertEqual(Producto.objects.count(), 55)
        self.assertTrue(
            Producto.objects.filter(
                nombre='Extensión eléctrica reforzada 10 m',
            ).exists(),
        )
