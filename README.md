# 🎟️ Ticketing Django

Sistema de ticketing para eventos deportivos y culturales. Permite a los organizadores crear eventos, vender entradas con códigos QR, y a los usuarios comprar entradas y gestionar sus compras.

## 🚀 Tecnologías utilizadas

- **Django 6.1** (backend)
- **SQLite** (base de datos)
- **HTML/CSS** (frontend)
- **qrcode + Pillow** (generación de códigos QR)
- **Django REST Framework** (API, opcional)

## ✨ Funcionalidades

- ✅ Autenticación de usuarios (registro, login, logout)
- ✅ Lista de eventos con diseño moderno
- ✅ Detalle de eventos
- ✅ Compra de entradas con generación automática de QR
- ✅ Mis Entradas (visualización de QR)
- ✅ Dashboard del organizador con estadísticas (eventos, entradas vendidas, recaudación)
- ✅ Panel de administración personalizado

## 📸 Capturas de pantalla

*(Aquí puedes añadir imágenes de tu proyecto en funcionamiento)*

## 🛠️ Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/ticketing-django.git
cd ticketing-django

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install django qrcode pillow

# 4. Configurar la base de datos
python manage.py migrate
python manage.py createsuperuser

# 5. Ejecutar el servidor
python manage.py runserver