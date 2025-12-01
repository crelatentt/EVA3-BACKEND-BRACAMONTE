from django.shortcuts import render, redirect, get_object_or_404
from mainApp.models import Producto, Categoria, Pedido, ImagenPedido
from .forms import PedidoForm, ImagenPedidoForm
from django.core.exceptions import ValidationError

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

        
