import json
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.db import transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import (
    AvisoGlobalForm,
    ConsultaClienteForm,
    ProductoForm,
    RegistroClienteForm,
)
from .models import (
    AvisoCliente,
    AvisoGlobal,
    Compra,
    ConfiguracionSitio,
    Producto,
    ProductoGuardado,
)


def inicio(request):
    return render(request, 'catalogo/inicio.html')


def catalogo(request):
    productos = Producto.objects.all()
    busqueda = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda)
            | Q(categoria__icontains=busqueda)
        )
    if categoria:
        productos = productos.filter(categoria=categoria)

    resumen = Producto.objects.aggregate(
        total=Count('pk'),
        con_stock=Count('pk', filter=Q(stock__gt=0)),
        unidades=Sum('stock'),
    )
    productos_guardados_ids = set()
    if request.user.is_authenticated:
        productos_guardados_ids = set(
            ProductoGuardado.objects.filter(
                usuario=request.user,
                producto_id__in=productos.values('pk'),
            ).values_list('producto_id', flat=True)
        )
    return render(
        request,
        'catalogo/catalogo.html',
        {
            'productos': productos,
            'busqueda': busqueda,
            'categoria_seleccionada': categoria,
            'categorias': Producto.CATEGORIAS,
            'resumen': resumen,
            'productos_guardados_ids': productos_guardados_ids,
        },
    )


@login_required
def panel_administracion(request):
    if not request.user.is_staff:
        raise PermissionDenied

    aviso_form = AvisoGlobalForm()
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'publicar_aviso':
            aviso_form = AvisoGlobalForm(request.POST)
            if aviso_form.is_valid():
                with transaction.atomic():
                    AvisoGlobal.objects.filter(activo=True).update(
                        activo=False,
                    )
                    aviso_form.save()
                messages.success(
                    request,
                    'El aviso se publicó para todos los visitantes.',
                )
                return redirect('panel_administracion')
        elif accion == 'restaurar_catalogo':
            with transaction.atomic():
                restaurados = 0
                directorio_fixtures = (
                    Path(__file__).resolve().parent / 'fixtures'
                )
                for nombre_fixture in (
                    'productos.json',
                    'productos_adicionales.json',
                ):
                    contenido = (
                        directorio_fixtures / nombre_fixture
                    ).read_text(encoding='utf-8')
                    for dato in json.loads(contenido):
                        _, creado = Producto.objects.get_or_create(
                            pk=dato['pk'],
                            defaults=dato['fields'],
                        )
                        restaurados += creado
            messages.success(
                request,
                f'Se restauraron {restaurados} productos faltantes. '
                'Los productos que ya existían no se modificaron.',
            )
            return redirect('panel_administracion')
        else:
            return HttpResponseBadRequest('La acción solicitada no es válida.')

    return render(
        request,
        'catalogo/panel_administracion.html',
        {
            'productos': Producto.objects.all(),
            'aviso_form': aviso_form,
            'aviso_global': AvisoGlobal.objects.filter(activo=True).first(),
        },
    )


def reporte_resumen_categorias(request):
    resumenes = (
        Producto.objects.values('categoria')
        .annotate(
            cantidad=Count('pk'),
            precio_promedio=Avg('precio'),
            stock_total=Sum('stock'),
        )
        .order_by('categoria')
    )
    return render(
        request,
        'catalogo/reporte_resumen_categorias.html',
        {'resumenes': resumenes},
    )


def reporte_stock_critico(request):
    umbral = 5
    productos = Producto.objects.filter(stock__lte=umbral).order_by(
        'stock',
        'nombre',
    )
    return render(
        request,
        'catalogo/reporte_stock_critico.html',
        {'productos': productos, 'umbral': umbral},
    )


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    visitados = request.session.get('productos_visitados', [])
    visitados = [str(pk) for pk in visitados if str(pk) != str(producto.pk)]
    visitados.insert(0, str(producto.pk))
    visitados = visitados[:3]
    request.session['productos_visitados'] = visitados
    productos_visitados = list(
        Producto.objects.filter(pk__in=visitados)
    )
    productos_por_id = {str(item.pk): item for item in productos_visitados}
    producto_guardado = request.user.is_authenticated and ProductoGuardado.objects.filter(
        usuario=request.user,
        producto=producto,
    ).exists()
    return render(
        request,
        'catalogo/detalle_producto.html',
        {
            'producto': producto,
            'productos_visitados': [
                productos_por_id[pk]
                for pk in visitados
                if pk in productos_por_id
            ],
            'producto_guardado': producto_guardado,
        },
    )


@login_required
def guardar_producto(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=producto_id)
        guardado, creado = ProductoGuardado.objects.get_or_create(
            usuario=request.user,
            producto=producto,
        )
        if creado:
            messages.success(request, f'{producto.nombre} se guardó para tu próxima compra.')
        else:
            messages.info(request, f'{producto.nombre} ya estaba en tus productos guardados.')
    return redirect(request.POST.get('next') or 'catalogo')


@login_required
def quitar_producto_guardado(request, producto_id):
    if request.method == 'POST':
        ProductoGuardado.objects.filter(
            usuario=request.user,
            producto_id=producto_id,
        ).delete()
        messages.success(request, 'Producto quitado de tus productos guardados.')
    return redirect(request.POST.get('next') or 'productos_guardados')


@login_required
def productos_guardados(request):
    guardados = ProductoGuardado.objects.select_related('producto').filter(
        usuario=request.user,
    )
    return render(
        request,
        'catalogo/productos_guardados.html',
        {'guardados': guardados},
    )


def _carrito_items(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(pk__in=carrito.keys())
    productos_por_id = {str(producto.pk): producto for producto in productos}
    items = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = productos_por_id.get(str(producto_id))
        if producto is None:
            continue
        cantidad = int(cantidad)
        subtotal = producto.precio * cantidad
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
            'max_quantity': producto.stock + cantidad,
        })
        total += subtotal
    return items, total


def carrito(request):
    items, total = _carrito_items(request)
    return render(
        request,
        'catalogo/carrito.html',
        {'items': items, 'total': total},
    )


@transaction.atomic
def agregar_al_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('detalle_producto', producto_id=producto_id)

    producto = get_object_or_404(Producto, pk=producto_id)
    try:
        cantidad = int(request.POST.get('cantidad', '1'))
    except (TypeError, ValueError):
        cantidad = 0
    carrito = request.session.get('carrito', {})
    cantidad_actual = int(carrito.get(str(producto.pk), 0))
    if cantidad < 1:
        messages.error(request, 'Ingresa una cantidad válida.')
    elif cantidad > producto.stock:
        messages.error(
            request,
            f'Solo puedes agregar hasta {producto.stock} unidades de {producto.nombre}.',
        )
    else:
        reservado = Producto.objects.filter(
            pk=producto.pk,
            stock__gte=cantidad,
        ).update(stock=F('stock') - cantidad)
        if not reservado:
            messages.error(request, 'El stock cambió; intenta nuevamente.')
        else:
            carrito[str(producto.pk)] = cantidad_actual + cantidad
            request.session['carrito'] = carrito
            messages.success(request, f'{producto.nombre} se agregó al carro.')
    return redirect(request.POST.get('next') or 'catalogo')


@transaction.atomic
def actualizar_carrito(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        for producto_id, valor in request.POST.items():
            if not producto_id.startswith('producto_'):
                continue
            producto_id = producto_id.removeprefix('producto_')
            try:
                cantidad = int(valor)
            except (TypeError, ValueError):
                continue
            producto = Producto.objects.filter(pk=producto_id).first()
            cantidad_anterior = int(carrito.get(producto_id, 0))
            if producto is None or cantidad <= 0:
                if producto is not None and cantidad_anterior:
                    Producto.objects.filter(pk=producto.pk).update(
                        stock=F('stock') + cantidad_anterior,
                    )
                carrito.pop(producto_id, None)
            elif cantidad > cantidad_anterior:
                diferencia = cantidad - cantidad_anterior
                reservado = Producto.objects.filter(
                    pk=producto.pk,
                    stock__gte=diferencia,
                ).update(stock=F('stock') - diferencia)
                if reservado:
                    carrito[producto_id] = cantidad
                else:
                    messages.error(
                        request,
                        f'No hay stock suficiente para aumentar {producto.nombre}.',
                    )
            else:
                Producto.objects.filter(pk=producto.pk).update(
                    stock=F('stock') + (cantidad_anterior - cantidad),
                )
                carrito[producto_id] = cantidad
        request.session['carrito'] = carrito
        messages.success(request, 'Carro actualizado.')
    return redirect('carrito')


@transaction.atomic
def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        cantidad = int(carrito.pop(str(producto_id), 0))
        if cantidad:
            Producto.objects.filter(pk=producto_id).update(
                stock=F('stock') + cantidad,
            )
        request.session['carrito'] = carrito
        messages.success(request, 'Producto quitado del carro.')
    return redirect('carrito')


@login_required
@transaction.atomic
def pagar_carrito(request):
    if request.method != 'POST':
        return redirect('carrito')
    items, _ = _carrito_items(request)
    if not items:
        messages.error(request, 'Tu carro está vacío.')
        return redirect('carrito')
    for item in items:
        Compra.objects.create(
            usuario=request.user,
            producto=item['producto'],
            nombre_producto=item['producto'].nombre,
            precio_unitario=item['producto'].precio,
            cantidad=item['cantidad'],
        )
        if request.session.get('notificaciones_activas', True):
            AvisoCliente.objects.create(
                usuario=request.user,
                mensaje=(
                    f'Compra registrada: {item["cantidad"]} x {item["producto"].nombre}. '
                    'Este pedido es de demostración y no tiene pago real.'
                ),
            )
    request.session['carrito'] = {}
    messages.success(request, 'Pago de demostración realizado; no se efectuó ningún cobro.')
    return redirect('historial')


def ayuda(request):
    return render(request, 'catalogo/ayuda.html')


def terminos(request):
    return render(request, 'catalogo/terminos.html')


class GestionProductosStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CrearProductoView(GestionProductosStaffMixin, CreateView):
    form_class = ProductoForm
    template_name = 'catalogo/producto_formulario.html'
    success_url = reverse_lazy('catalogo')
    extra_context = {'titulo': 'Agregar producto'}


class EditarProductoView(GestionProductosStaffMixin, UpdateView):
    form_class = ProductoForm
    model = Producto
    pk_url_kwarg = 'producto_id'
    template_name = 'catalogo/producto_formulario.html'
    success_url = reverse_lazy('catalogo')
    extra_context = {'titulo': 'Editar producto'}


class EliminarProductoView(GestionProductosStaffMixin, DeleteView):
    model = Producto
    pk_url_kwarg = 'producto_id'
    template_name = 'catalogo/producto_confirmar_eliminacion.html'
    success_url = reverse_lazy('catalogo')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                'No se puede eliminar este producto porque tiene compras asociadas.',
            )
            return redirect(self.success_url)


@login_required
@transaction.atomic
def comprar_producto(request, producto_id):
    if request.method != 'POST':
        return redirect('detalle_producto', producto_id=producto_id)

    producto = get_object_or_404(Producto, pk=producto_id)
    try:
        cantidad = int(request.POST.get('cantidad', '1'))
    except (TypeError, ValueError):
        messages.error(request, 'Ingresa una cantidad válida.')
        return redirect('detalle_producto', producto_id=producto_id)

    if cantidad < 1:
        messages.error(request, 'La cantidad debe ser al menos 1.')
    elif producto.stock < cantidad:
        messages.error(
            request,
            f'Solo quedan {producto.stock} unidades de {producto.nombre}.',
        )
    else:
        stock_actualizado = Producto.objects.filter(
            pk=producto.pk,
            stock__gte=cantidad,
        ).update(stock=F('stock') - cantidad)
        if not stock_actualizado:
            messages.error(
                request,
                'El stock cambió y ya no alcanza para esa cantidad. Inténtalo nuevamente.',
            )
            return redirect('detalle_producto', producto_id=producto_id)
        Compra.objects.create(
            usuario=request.user,
            producto=producto,
            nombre_producto=producto.nombre,
            precio_unitario=producto.precio,
            cantidad=cantidad,
        )
        if request.session.get('notificaciones_activas', True):
            AvisoCliente.objects.create(
                usuario=request.user,
                mensaje=(
                    f'Compra registrada: {cantidad} x {producto.nombre}. '
                    'Este pedido es de demostración y no tiene pago real.'
                ),
            )
        messages.success(
            request,
            'Compra de demostración registrada; no se realizó ningún cobro.',
        )
        return redirect('historial')

    return redirect('detalle_producto', producto_id=producto_id)


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('consulta')
    else:
        form = RegistroClienteForm()

    return render(request, 'catalogo/registro.html', {'form': form})


class IniciarSesionView(LoginView):
    template_name = 'catalogo/iniciar_sesion.html'
    redirect_authenticated_user = True


class CerrarSesionView(LogoutView):
    next_page = reverse_lazy('inicio')


class CrearConsultaView(CreateView):
    form_class = ConsultaClienteForm
    template_name = 'catalogo/consulta.html'
    success_url = reverse_lazy('consulta_enviada')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST' and self.request.user.is_authenticated:
            data = self.request.POST.copy()
            data.setdefault(
                'nombre',
                self.request.user.get_full_name() or self.request.user.username,
            )
            data.setdefault(
                'correo',
                self.request.user.email or (
                    f'{self.request.user.username}@ejemplo.com'
                ),
            )
            kwargs['data'] = data
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['nombre'] = self.request.user.get_full_name() or self.request.user.username
            initial['correo'] = self.request.user.email
        producto_id = self.request.GET.get('producto', '')
        if producto_id.isdigit():
            initial['producto'] = int(producto_id)
        return initial

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.usuario = self.request.user
        response = super().form_valid(form)
        if self.request.session.get('notificaciones_activas', True):
            AvisoCliente.objects.create(
                usuario=self.request.user,
                mensaje='Tu consulta fue recibida correctamente.',
            )
        return response


def consulta_enviada(request):
    return render(request, 'catalogo/consulta_enviada.html')


@login_required
def historial(request):
    return render(
        request,
        'catalogo/historial.html',
        {
            'compras': Compra.objects.filter(usuario=request.user),
            'consultas': request.user.consultas_ferreteria.all(),
        },
    )


@login_required
def notificaciones(request):
    avisos = AvisoCliente.objects.filter(usuario=request.user)
    if request.method == 'POST':
        avisos.filter(leido=False).update(leido=True)
        return redirect('notificaciones')
    return render(
        request,
        'catalogo/notificaciones.html',
        {'avisos': avisos},
    )


def configuracion(request):
    if request.method == 'POST':
        idioma = request.POST.get('idioma', 'es')
        tema = request.POST.get('tema', 'light')
        if idioma not in {'es', 'en'} or tema not in {'light', 'dark'}:
            messages.error(request, 'La configuración seleccionada no es válida.')
            return redirect('configuracion')
        request.session['idioma'] = idioma
        request.session['tema'] = tema
        request.session['notificaciones_activas'] = (
            request.POST.get('notificaciones') == 'on'
        )
        messages.success(request, 'Preferencias guardadas.')
        return redirect('configuracion')

    return render(
        request,
        'catalogo/configuracion.html',
        {
            'idioma': request.session.get('idioma', 'es'),
            'tema': request.session.get('tema', 'light'),
            'notificaciones_activas': request.session.get(
                'notificaciones_activas',
                True,
            ),
        },
    )
