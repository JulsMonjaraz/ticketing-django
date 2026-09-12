import requests
from django.conf import settings


def geocodificar_direccion(direccion):
    """
    Convierte una dirección en coordenadas (lat, lng) usando Google Maps Geocoding API.
    Devuelve un diccionario {'lat': ..., 'lng': ...} o None si falla.
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        return None

    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': direccion, 'key': api_key}

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get('status') == 'OK':
            location = data['results'][0]['geometry']['location']
            return {'lat': location['lat'], 'lng': location['lng']}
    except Exception:
        pass
    return None