from django import forms
from .models import Pedido, ImagenPedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_contacto', 'producto', 'descripcion', 'fecha_necesita']
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_necesita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ImagenPedidoForm(forms.ModelForm):
    class Meta:
        model = ImagenPedido
        fields = ['imagen']

        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }