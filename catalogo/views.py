from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.deletion import ProtectedError
from django.db import transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import ConsultaClienteForm, ProductoForm, RegistroClienteForm
from .models import AvisoCliente, Compra, ConfiguracionSitio, Producto


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
    return render(
        request,
        'catalogo/catalogo.html',
        {
            'productos': productos,
            'busqueda': busqueda,
            'categoria_seleccionada': categoria,
            'categorias': Producto.CATEGORIAS,
            'resumen': resumen,
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
    return render(
        request,
        'catalogo/detalle_producto.html',
        {'producto': producto},
    )


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


class CrearConsultaView(LoginRequiredMixin, CreateView):
    form_class = ConsultaClienteForm
    template_name = 'catalogo/consulta.html'
    success_url = reverse_lazy('consulta_enviada')

    def get_initial(self):
        initial = super().get_initial()
        producto_id = self.request.GET.get('producto', '')
        if producto_id.isdigit():
            initial['producto'] = int(producto_id)
        return initial

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        if self.request.session.get('notificaciones_activas', True):
            AvisoCliente.objects.create(
                usuario=self.request.user,
                mensaje='Tu consulta fue recibida correctamente.',
            )
        return response


@login_required
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
