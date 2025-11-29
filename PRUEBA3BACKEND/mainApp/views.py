from django.shortcuts import render
from mainApp.models import Producto, Categoria

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
