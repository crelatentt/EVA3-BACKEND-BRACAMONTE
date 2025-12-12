from django.shortcuts import render, redirect, get_object_or_404
from mainApp.models import Producto, Categoria, Pedido, ImagenPedido
from .forms import PedidoForm, ImagenPedidoForm
from django.core.exceptions import ValidationError
from django.db import models
import datetime
from django.db.models import Count

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

        
