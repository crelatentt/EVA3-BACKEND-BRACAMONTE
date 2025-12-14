from django.shortcuts import render, redirect, get_object_or_404
from mainApp.models import Producto, Categoria, Pedido, ImagenPedido, Insumo
from .forms import PedidoForm, ImagenPedidoForm
from django.core.exceptions import ValidationError
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import InsumoSerializer, PedidoSerializer
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PedidoFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    error_mensaje = None
    if request.method == 'POST': 
        token_buscar = request.POST.get('token_seguimiento')
        try:
            Pedido.objects.get(token=token_buscar)
            return redirect('seguimiento', token=token_buscar)
        except Pedido.DoesNotExist:
            error_mensaje = "Token no encontrado. Por favor, verifique e intente nuevamente."
        except ValidationError:
            error_mensaje = "Token inválido. Por favor, verifique e intente nuevamente."
        
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    buscar = request.GET.get("q")

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if buscar:
        productos = productos.filter(nombre__istartswith=buscar)

    data = {
        'productos': productos,
        'categorias': categorias,
        'categoria_sel': categoria_id,
        'buscar': buscar,
        'error_seguimiento': error_mensaje
    }
    return render(request, 'home.html', data)

def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    data = {
        'producto': producto
    }
    return render(request, 'detalle_producto.html', data)

def formulario_pedido(request):
    form = PedidoForm()
    imagen_form = ImagenPedidoForm()

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        imagen_form = ImagenPedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save()
            pedido.plataforma_origen = "WEB"
            pedido.estado_pago = "PENDIENTE"
            pedido.estado_pedido = "SOLICITADO"
            pedido.save()
            if request.FILES.get('imagen'):
                ImagenPedido.objects.create(
                    pedido=pedido,
                    imagen=request.FILES.get('imagen')
                )
            data = {
                'pedido': pedido,
                'token': pedido.obtener_token(),
                'url_seguimiento': pedido.obtener_token(),
            }
            return render(request, 'pedido_confirmacion.html', data)
    data = {
        'form': form,
        'imagen_form': imagen_form,
    }
    return render(request, 'formulario_pedido.html', data)

def pedido_confirmacion(request, token):
    pedido = None
    data = {
        'pedido': pedido,
    }
    return render(request, 'pedido_confirmacion.html', data)

def seguimiento(request, token):
    try:
        pedido = Pedido.objects.get(token=token)
    except Pedido.DoesNotExist:
        pedido = None

    imagenes = ImagenPedido.objects.filter(pedido=pedido)

    data = {
        'pedido': pedido,
        'imagenes': imagenes
    }
    return render(request, 'seguimiento.html', data)

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

@login_required
def reporte_sistema(request):
    pedidos_filtrados = Pedido.objects.all()
    estado_seleccionado = request.GET.get('estado')
    lista_estados_choices = Pedido.estados_pedido
    plataforma_seleccionada = request.GET.get('plataforma')
    
    if estado_seleccionado and estado_seleccionado != 'TODOS':
        pedidos_filtrados = pedidos_filtrados.filter(estado_pedido=estado_seleccionado)
    
    reporte_por_estado = pedidos_filtrados.values('estado_pedido').annotate(cantidad=Count('id')).order_by('-cantidad')

    reporte_por_plataforma = pedidos_filtrados.values('plataforma_origen').annotate(cantidad=Count('id')).order_by('-cantidad')

    reporte_productos_solicitados = pedidos_filtrados.filter(producto__isnull=False).values('producto__nombre' ).annotate(cantidad=Count('producto')).order_by('-cantidad')[:10] 
    
    data = {
        'reporte_por_estado': reporte_por_estado,
        'reporte_por_plataforma': reporte_por_plataforma,
        'reporte_productos_solicitados': reporte_productos_solicitados,
        'estado_seleccionado': estado_seleccionado,
        'estados': lista_estados_choices,
        'plataforma_seleccionada' : plataforma_seleccionada,
    }

    return render(request, 'reporte_sistema.html', data)

class lista_insumos(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class detalle_insumos(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class lista_pedidos(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class detalle_pedido(mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get(self, request, *args, **kwargs):
        pedido = self.get_object()
        serializer = self.get_serializer(pedido)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class filtro_pedidos(generics.ListAPIView):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all().order_by('-fecha_creacion')
    filter_backends = [DjangoFilterBackend] 
    filterset_class = PedidoFilter

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        limite_resultados_str = self.request.query_params.get('limite')
        
        if limite_resultados_str:
            try:
                limite = int(limite_resultados_str)
                queryset = queryset[:limite] 
            except ValueError:
                pass
                
        return queryset


