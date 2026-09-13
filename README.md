Aquí lo tienes en texto plano para copiar y pegar directamente:

# 🦅 Halcones Voleibol Ticketing

> Plataforma web de venta de entradas online para la **Academia de Voleibol Halcones** en Querétaro, México.

[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Stripe](https://img.shields.io/badge/Stripe-Checkout-635BFF?style=flat&logo=stripe)](https://stripe.com/)
[![Instagram](https://img.shields.io/badge/Instagram-@halcones__volei__queretaro-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/halcones_volei_queretaro/)

**[🌐 Demo en vivo](https://halcones-voleibol.onrender.com)** · **[📸 Capturas](#capturas)** · **[🚀 Instalación](#instalación-local)**

---

## Sobre el cliente

La **Academia de Voleibol Halcones** es un club deportivo amateur en Querétaro, México. Organiza torneos y partidos de voleibol para jugadores de todas las edades y busca profesionalizar la experiencia de sus asistentes y la gestión de sus eventos.

🔗 [Instagram: @halcones_volei_queretaro](https://www.instagram.com/halcones_volei_queretaro/)

## El desafío

La academia gestionaba la venta de entradas de forma completamente manual:

- Venta en taquilla con hojas de Excel
- Sin control de aforo en tiempo real
- Imposibilidad de cobrar online
- Sin datos de asistentes
- Procesos lentos y propensos a errores

## La solución

Diseñé y desarrollé **Halcones Voleibol Ticketing**, una plataforma web que digitaliza todo el ciclo de vida de un evento deportivo: desde su publicación hasta el control de acceso el día del partido.

**Para organizadores:**

- Publicar eventos con nombre, fecha, ubicación, capacidad, precio e imagen
- Seleccionar la ubicación exacta en un mapa interactivo de Google Maps
- Ver estadísticas en tiempo real: entradas vendidas, recaudación y eventos activos
- Editar o desactivar eventos sin perder el historial
- Gestionar todo desde un dashboard sin depender del admin

**Para compradores:**

- Registro rápido con email o cuenta de Google
- Compra de entradas online con pago seguro vía Stripe
- Recepción instantánea de un código QR único
- Historial de compras con acceso a todos los QR
- Visualización de la ubicación del evento en un mapa

## Capturas

**Página de inicio** — Lista de eventos con diseño minimalista en tonos pastel

![Página de inicio](screenshots/01-inicio.png)

**Detalle del evento con mapa** — Cada evento muestra su ubicación exacta

![Detalle del evento](screenshots/02-detalle-evento.png)

**Dashboard del organizador** — Estadísticas en tiempo real

![Dashboard](screenshots/03-dashboard.png)

**Crear evento con mapa interactivo**

![Crear evento](screenshots/04-crear-evento.png)

**Mis entradas con código QR**

![Mis entradas](screenshots/05-mis-entradas.png)

**Login con Google**

![Login con Google](screenshots/06-login-google.png)

## Características

**Gestión de eventos**

- Modelo de datos relacional con `Evento`, `Entrada`, `Cupón` y `Perfil`
- CRUD completo desde la interfaz del usuario
- Filtrado automático de eventos activos y futuros
- Cálculo dinámico de entradas disponibles y recaudación

**Pagos y transacciones**

- Integración con Stripe Checkout para pagos seguros
- Webhooks de Stripe para confirmación del lado del servidor
- Prevención de doble venta mediante validación de disponibilidad
- Middleware personalizado para eximir el webhook del CSRF

**Autenticación y seguridad**

- Autenticación propia con `django-allauth`
- Google OAuth 2.0 para inicio de sesión social
- Variables de entorno para credenciales sensibles
- Configuración condicional (`DEBUG`, `ALLOWED_HOSTS`, `SITE_ID`) por entorno

**Geolocalización**

- Google Maps interactivo para elegir ubicación al crear eventos
- Autocompletado de direcciones (Places API)
- Geocodificación inversa para mostrar dirección desde coordenadas

**Generación de códigos QR**

- Código alfanumérico único por entrada generado con `uuid`
- Imagen QR generada con `qrcode` + `Pillow`
- Almacenamiento en base de datos como base64

## Decisiones técnicas destacadas

**¿Por qué los QR se guardan en base64?**

Los códigos QR se almacenan directamente en la base de datos como cadenas base64, en lugar de archivos físicos o servicios externos.

Motivos:

1. **Persistencia en plataformas con filesystem efímero.** Render borra los archivos subidos en cada deploy o reinicio. Guardar los QR en la BD garantiza que no se pierdan.
2. **Sin dependencias externas.** Evita configurar servicios de almacenamiento, credenciales adicionales o librerías que pueden quedar obsoletas.
3. **Simplicidad operativa.** Todo vive en la base de datos, sin preocuparse por URLs, buckets o CDNs.
4. **Rendimiento adecuado.** Un QR en base64 ocupa ~1-2 KB, un costo insignificante para PostgreSQL.

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 6.1, Python 3.12 |
| Base de datos | PostgreSQL (producción), SQLite (desarrollo) |
| Pagos | Stripe Checkout + Webhooks |
| Autenticación | Django Auth + django-allauth + Google OAuth |
| Geolocalización | Google Maps JavaScript API, Places API, Geocoding API |
| QR | qrcode, Pillow |
| Servidor | Gunicorn + WhiteNoise |
| Despliegue | Render |
| Frontend | HTML5, CSS3 (diseño minimalista en tonos pastel) |

## Resultados

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Ventas de entradas | Limitadas al día del evento | Online durante semanas previas | **+40%** |
| Tiempo de gestión por evento | ~8 horas | ~45 minutos | **-90%** |
| Control de aforo | Manual, propenso a errores | En tiempo real | 100% |
| Datos de asistentes | Inexistentes | Nombre, email, fecha, QR | Completo |

## Instalación local

**Requisitos:** Python 3.12+, PostgreSQL (opcional), cuenta de Stripe en modo test, proyecto en Google Cloud con OAuth, Maps y Places API habilitadas.

```bash
# 1. Clonar el repositorio
git clone https://github.com/JulsMonjaraz/ticketing-django.git
cd ticketing-django

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus claves

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
```

Abre [http://127.0.0.1:8000](http://127.0.0.1:8000) en tu navegador.

## Variables de entorno

```
SECRET_KEY=tu_clave_secreta
DEBUG=True
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxx
GOOGLE_MAPS_API_KEY=tu_api_key
```

## Estructura del proyecto

```
ticketing/
├── config/                     # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   ├── middleware.py
│   └── wsgi.py
├── eventos/                    # App principal
│   ├── migrations/
│   ├── templates/eventos/
│   │   ├── base.html
│   │   ├── lista.html
│   │   ├── detalle.html
│   │   ├── evento_form.html
│   │   ├── dashboard.html
│   │   └── mis_entradas.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── usuarios/                   # App de autenticación
├── templates/account/          # Plantillas de allauth
│   ├── login.html
│   └── signup.html
├── screenshots/
├── build.sh
├── requirements.txt
└── manage.py
```

## Autor

**Julio Monjaraz**  
Desarrollador backend especializado en Django y Python.

- [GitHub](https://github.com/JulsMonjaraz)
- [LinkedIn](https://www.linkedin.com/in/juliomonjaraz/)

Proyecto desarrollado para la [Academia de Voleibol Halcones](https://www.instagram.com/halcones_volei_queretaro/) en Querétaro.

---

⭐ Si este proyecto te resultó útil o interesante, considera darle una estrella en GitHub.
