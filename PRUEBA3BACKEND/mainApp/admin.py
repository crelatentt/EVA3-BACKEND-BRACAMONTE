from django.contrib import admin
from .models import Categoria, Producto, Insumo, Pedido
from django.utils.html import format_html

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ["nombre"]

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio_base", "producto_destacado", "mostrar_imagen1", "mostrar_imagen2", "mostrar_imagen3")
    list_filter = ("categoria", "producto_destacado")

    def mostrar_imagen1(self,obj):
        if obj.foto_1:
            return format_html('<img src="{}" width="100" height="100" />', obj.foto_1.url)
        return "Sin foto"
    
    def mostrar_imagen2(self,obj):
        if obj.foto_2:
            return format_html('<img src="{}" width="100" height="100" />', obj.foto_2.url)
        return "Sin foto"
    
    def mostrar_imagen3(self,obj):
        if obj.foto_3:
            return format_html('<img src="{}" width="100" height="100" />', obj.foto_3.url)
        return "Sin foto"
    
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "cantidad_dispo", "unidad", "marca", "color")
    search_fields = ("nombre", "tipo", "marca")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente_nombre", "producto", "estado_pedido", "estado_pago", "plataforma_origen", "fecha_creacion", "mostrar_token")
    list_filter = ("estado_pedido", "estado_pago", "plataforma_origen", "fecha_creacion")
    search_fields = ("cliente_nombre", "cliente_contacto", "descripcion", "token")
    readonly_fields = ("token", "fecha_creacion")

    def mostrar_token(self, obj):
        return str(obj.token)[:8] + "..."
    mostrar_token.short_description = "Token"