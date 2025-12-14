from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('solicitar/', views.formulario_pedido, name='formulario_pedido'),
    path('solicitud/<uuid:token>/', views.pedido_confirmacion, name='pedido_confirmacion'),
    path('seguimiento/<uuid:token>/', views.seguimiento, name='seguimiento'),
    path('api/insumos/', views.lista_insumos.as_view()),
    path('api/insumos/<int:pk>/', views.detalle_insumos.as_view()),
    path('api/pedidos/', views.lista_pedidos.as_view()),
    path('api/pedidos/<int:pk>/', views.detalle_pedido.as_view()),
    path('api/pedidos/filtrar/', views.filtro_pedidos.as_view()),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reporte_sistema/', views.reporte_sistema, name='reporte_sistema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)