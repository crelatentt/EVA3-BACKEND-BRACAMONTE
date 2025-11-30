from django.shortcuts import render
from mainApp.models import Producto, Categoria, Pedido, ImagenPedido
from .forms import PedidoForm, ImagenPedidoForm

def home(request):
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
        'buscar': buscar
    }
    return render(request, 'home.html', data)

def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    data = {
        'producto': producto
    }
    return render(request, 'detalle_producto.html', data)

def formulario_pedido(request):
    producto_id = request.GET.get('producto')
    producto = None

    if producto_id:
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            producto = None

    if request.method == 'POST':
        nombre = request.POST.get('cliente_nombre')
        contacto = request.POST.get('cliente_contacto')
        producto_id = request.POST.get('producto')
        descripcion = request.POST.get('descripcion')
        fecha_necesita = request.POST.get('fecha_necesita')

        pedido = Pedido.objects.create(
            cliente_nombre=nombre,
            cliente_contacto=contacto,
            producto_id=producto_id,
            descripcion=descripcion,
            plataforma_origen="WEB",
            estado_pago="PENDIENTE",
            fecha_necesita=fecha_necesita,
            estado_pedido = "SOLICITADO",
        )

        imagen = request.FILES.get('imagen')
        if imagen:
            ImagenPedido.objects.create(
                pedido=pedido,
                imagen=imagen
            )

        data = {
            "pedido": pedido,
            "token": pedido.obtener_token(),
            "url_seguimiento": pedido.obtener_token()
        }

        return render(request, 'pedido_confirmacion.html', data)

    data = {
        'producto_select': producto,
        'productos': Producto.objects.all()
    }

    return render(request, 'formulario_pedido.html', data)

def pedido_confirmacion(request, token):
    try:
        pedido = Pedido.objects.get(token=token)
    except Pedido.DoesNotExist:
        pedido = None

    data = {
        'pedido': pedido
    }

    return render(request, 'pedido_confirmacion.html', data)

def seguimiento(request, token):
    try:
        pedido = Pedido.objects.get(token=token)
    except Pedido.DoesNotExist:
        pedido = None

    data = {
        'pedido': pedido
    }

    return render(request, 'seguimiento.html', data)

        
