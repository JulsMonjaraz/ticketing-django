from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evento, Entrada
import uuid 
import qrcode 
from io import BytesIO
from django.core.files import File
from django.db.models import Sum, Count

def lista_eventos(request):
    eventos = Evento.objects.filter(activo=True).order_by('fecha')
    return render(request, 'eventos/lista.html', {'eventos': eventos})

def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, activo=True )
    return render(request, 'eventos/detalle.html', {'evento':evento})

@login_required
def comprar_entrada(request, pk):
    evento = get_object_or_404(Evento, pk=pk, activo=True)

    if evento.entradas_disponibles <= 0:
        messages.error(request, 'No hay entradas disponibles para este evento.')
        return redirect('eventos:detalle', pk=evento.pk)

    codigo = str(uuid.uuid4()).replace('-', '')[:12].upper()

    entrada = Entrada.objects.create(
        evento=evento,
        comprador=request.user,
        codigo_unico=codigo,
        precio_pagado=evento.precio,
    )

    # Generar el QR
    # 5. Generar el código QR
    qr = qrcode.make(f'Ticket:{codigo}')
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    #guarda la imagen en el campo qr_code

    entrada.qr_code.save(f"{codigo}.png", File(buffer), save=True)

    messages.success(request, f'¡Compra exitosa! Tu código: {codigo}')
    return redirect('eventos:mis_entradas')

def mis_entradas(request):
    entradas = Entrada.objects.filter(comprador=request.user).order_by('-fecha_compra')
    return render(request, 'eventos/mis_entradas.html', {'entradas':entradas})


# dashboard
def dashboard_organizador(request):
    #1 obtain eventos created by user 
    eventos = Evento.objects.filter(organizador=request.user).order_by('-creado')

    #2 calacular estadísticas 

    total_eventos = eventos.count()
    total_entradas_vendidas = Entrada.objects.filter(evento__in=eventos).count()
    total_recaudado = Entrada.objects.filter(evento__in=eventos).aggregate(
        total=Sum('precio_pagado')
    )['total'] or 0

    #preparar datos para cada evento 
    eventos_data = []
    for evento in eventos:
        entradas_vendidas = evento.entrada_set.count()
        recaudado = evento.entrada_set.aggregate(
            total=Sum('precio_pagado')
        )['total'] or 0 
        eventos_data.append({
            'evento':evento,
            'entradas_vendidas': entradas_vendidas,
            'recaudado': recaudado,
        })
    context = {
        'eventos': eventos_data,
        'total_eventos': total_eventos,
        'total_entradas_vendidas': total_entradas_vendidas,
        'total_recaudado': total_recaudado,
    }
    return render(request, 'eventos/dashboard.html', context)
