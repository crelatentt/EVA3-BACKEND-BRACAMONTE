from django import forms
from .models import Pedido, ImagenPedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_contacto', 'producto', 'descripcion', 'plataforma_origen', 'estado_pago', 'fecha_necesita']
        widgets = {"fecha_necesita": forms.DateInput(attrs={"type": "date"})}

class ImagenPedidoForm(forms.ModelForm):
    class Meta:
        model = ImagenPedido
        fields = ['imagen']