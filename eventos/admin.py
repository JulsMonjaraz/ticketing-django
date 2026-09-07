from django.contrib import admin
from .models import Evento, Entrada, Cupon

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'precio', 'activo')
    list_filter = ('activo', 'fecha')
    search_fields = ('nombre', 'lugar')

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('codigo_unico', 'evento', 'comprador', 'fecha_compra', 'usada')
    list_filter = ('usada', 'evento')

@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descuento', 'evento', 'usos_maximos', 'usos_actuales')