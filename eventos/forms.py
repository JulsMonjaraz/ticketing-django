from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'lugar', 'latitud', 'longitud', 'capacidad', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Torneo de Voleibol'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe tu evento...'}),
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'lugar': forms.HiddenInput(attrs={'id': 'id_lugar'}),
            'latitud': forms.HiddenInput(attrs={'id': 'id_latitud'}),
            'longitud': forms.HiddenInput(attrs={'id': 'id_longitud'}),
            'capacidad': forms.NumberInput(attrs={'placeholder': '100'}),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '25.00'}),
        }