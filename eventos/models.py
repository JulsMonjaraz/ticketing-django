from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Event Model 
class Evento(models.Model):

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    capacidad = models.PositiveBigIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='eventos/',null=True, blank = True)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    # Special model 
    def __str__(self):
        return self.nombre


    # Calculated property 
    @property
    def entradas_disponibles(self):
        vendidas = self.entrada_set.count()
        return self.capacidad - vendidas

    @property
    def recaudado(self): 
        return sum(entrada.precio_pagado for entrada in self.entrada_set.all())
    

class Entrada(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_unico = models.CharField( max_length=100,unique=True, editable=False)
    qr_code = models.ImageField(upload_to='qrs/', null=True, blank=True)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateField(auto_now_add=True)
    usada = models.BooleanField(default=False)

    def __str__(self):
        return f"Entrada {self.codigo_unico[:8]} - {self.evento.nombre  }"


    
class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.DecimalField(max_digits=5,decimal_places=2)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null = True, blank=True)
    usos_maximos = models.PositiveBigIntegerField(default=1)
    usos_actuales = models.PositiveBigIntegerField(default=0)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo




