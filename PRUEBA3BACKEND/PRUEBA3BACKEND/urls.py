from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('solicitar/', views.formulario_pedido, name='formulario_pedido'),
    path('solicitud/<uuid:token>/', views.pedido_confirmacion, name='pedido_confirmacion'),
    path('seguimiento/<uuid:token>/', views.seguimiento, name='seguimiento'),
    path('reporte_sistema/', views.reporte_sistema, name='reporte_sistema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)