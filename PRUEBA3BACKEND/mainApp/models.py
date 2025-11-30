from django.db import models
import uuid

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    producto_destacado = models.BooleanField(default=False)
    precio_base = models.PositiveIntegerField()
    foto_1 = models.ImageField(upload_to='media/', blank=True)
    foto_2 = models.ImageField(upload_to='media/', blank=True)
    foto_3 = models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return self.nombre
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=150)
    cantidad_dispo = models.PositiveIntegerField(default=0)
    unidad = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    estados_pedido = [
    ("SOLICITADO", "Solicitado"),
    ("APROBADO", "Aprobado"),
    ("EN_PROCESO", "En proceso"),
    ("REALIZADA", "Realizada"),
    ("ENTREGADA", "Entregada"),
    ("FINALIZADA", "Finalizada"),
    ("CANCELADA", "Cancelada"),
]
    
    plataformas = [
        ("FACEBOOK", "Facebook"),
        ("INSTAGRAM", "Instagram"),
        ("WHATSAPP", "WhatsApp"),
        ("PRESENCIAL", "Presencial"),
        ("WEB", "Página Web"),
        ("OTRA", "Otra"),
    ]

    estados_pago = [
        ("PENDIENTE", "Pendiente"),
        ("PARCIAL", "Parcial"),
        ("PAGADO", "Pagado"),
    ]

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    cliente_nombre = models.CharField(max_length=150)
    cliente_contacto = models.CharField(max_length=150)  #coso para contactar al cliente xd osea email tlf etc
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField()
    estado_pedido = models.CharField(max_length=20, choices= estados_pedido, default="SOLICITADO")
    estado_pago = models.CharField(max_length=20, choices= estados_pago, default="PENDIENTE")
    plataforma_origen = models.CharField(max_length=20, choices=plataformas)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_necesita = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"

    def obtener_token(self):
        return f"/seguimiento/{self.token}/"
    
class ImagenPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='media/')

