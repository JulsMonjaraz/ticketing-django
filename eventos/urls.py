from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.lista_eventos, name='lista'),
    path('<int:pk>/', views.detalle_evento, name='detalle'), 
    path('mis-entradas/', views.mis_entradas, name='mis_entradas'),
    path('<int:pk>/comprar/', views.comprar_entrada, name='comprar'),
    path('dashboard/', views.dashboard_organizador, name='dashboard')
]