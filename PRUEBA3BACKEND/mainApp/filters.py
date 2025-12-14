import django_filters
from .models import Pedido 

class PedidoFilter(django_filters.FilterSet):
    fecha_creacion = django_filters.DateFilter(
        field_name='fecha_creacion', 
        lookup_expr='gte', 
        label='Fecha de Creación'
    )

    limite = django_filters.NumberFilter(method='filter_limite', label='Límite de Resultados')

    class Meta:
        model = Pedido
        fields = ['fecha_creacion', 'estado_pedido', 'limite']

    def filter_limite(self, queryset, name, value):
        return queryset[:value]