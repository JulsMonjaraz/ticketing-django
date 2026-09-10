from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evento, Entrada
import uuid 
import qrcode 
from io import BytesIO
from django.core.files import File
from django.db.models import Sum, Count
import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .forms import EventoForm


# secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

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
        messages.error(request, 'No hay entradas disponibles.')
        return redirect('eventos:detalle', pk=evento.pk)

    # 1. Crear una sesión de pago en Stripe
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': evento.nombre,
                            'description': evento.descripcion[:200],
                        },
                        'unit_amount': int(evento.precio * 100),  # Stripe usa centavos
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('eventos:pago_exitoso', args=[evento.pk])),
            cancel_url=request.build_absolute_uri(reverse('eventos:detalle', args=[evento.pk])),
            metadata={
                'evento_id': evento.pk,
                'user_id': request.user.pk,
                'precio': str(evento.precio),
            }
        )
    except Exception as e:
        messages.error(request, f'Error al procesar el pago: {str(e)}')
        return redirect('eventos:detalle', pk=evento.pk)

    # 2. Redirigir al usuario a Stripe
    return redirect(checkout_session.url, code=303)

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

@login_required
def pago_exitoso(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/pago_exitoso.html', {'evento': evento})

@csrf_exempt
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.metadata.to_dict()       # <-- Convierte a dict
        user_id = metadata.get('user_id')           # <-- Ahora sí funciona .get()
        evento_id = metadata.get('evento_id')       # <-- Ahora sí funciona .get()

        if user_id and evento_id:
            try:
                user = User.objects.get(id=user_id)
                evento = Evento.objects.get(id=evento_id)

                if not Entrada.objects.filter(evento=evento, comprador=user).exists():
                    codigo = str(uuid.uuid4()).replace('-', '')[:12].upper()
                    entrada = Entrada.objects.create(
                        evento=evento,
                        comprador=user,
                        codigo_unico=codigo,
                        precio_pagado=evento.precio,
                    )
                    qr = qrcode.make(f"TICKET:{codigo}")
                    buffer = BytesIO()
                    qr.save(buffer)
                    buffer.seek(0)
                    entrada.qr_code.save(f"{codigo}.png", File(buffer), save=True)
            except (User.DoesNotExist, Evento.DoesNotExist):
                pass

    return HttpResponse(status=200)

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            messages.success(request, '¡Evento creado exitosamente!')
            return redirect('eventos:dashboard')
    else:
        form = EventoForm()
    return render(request, 'eventos/evento_form.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado correctamente.')
            return redirect('eventos:dashboard')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/evento_form.html', {
        'form': form,
        'accion': 'Editar',
        'evento': evento,
    })


@login_required
def desactivar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    evento.activo = False
    evento.save()
    messages.info(request, f'Evento "{evento.nombre}" desactivado.')
    return redirect('eventos:dashboard')
