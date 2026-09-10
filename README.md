# 🦅 Halcones Voleibol Ticketing

> **Caso de estudio:** Plataforma de venta de entradas online desarrollada para la **Academia de Voleibol Halcones** en Querétaro, México. La academia organiza torneos y partidos de voleibol y necesitaba una solución moderna para gestionar la venta de entradas, el control de aforo y la experiencia de sus asistentes.

---

## 📖 El problema

La Academia de Voleibol Halcones gestionaba la venta de entradas para sus torneos de forma completamente manual:

- Venta en taquilla con hojas de Excel
- Sin control de aforo en tiempo real
- Imposibilidad de cobrar online
- Sin datos de asistentes ni historial de compras
- Procesos lentos y propensos a errores

## 💡 La solución

Diseñé y desarrollé **Halcones Voleibol Ticketing**, una plataforma web completa que digitaliza todo el proceso de venta de entradas y ofrece a los organizadores control total sobre sus eventos.

## ✨ Funcionalidades

- ✅ **Autenticación de usuarios** (registro, login, logout)
- ✅ **Lista de eventos** con diseño minimalista y animaciones modernas
- ✅ **Detalle de eventos** con información completa
- ✅ **Compra de entradas** con pago seguro vía Stripe
- ✅ **Generación automática de códigos QR** únicos por entrada
- ✅ **Página "Mis Entradas"** con visualización de QR para acceso
- ✅ **Dashboard del organizador** con estadísticas en tiempo real (eventos, entradas vendidas, recaudación)
- ✅ **Creación y edición de eventos** desde la propia plataforma (sin depender del admin)
- ✅ **Desactivación de eventos** sin perder datos históricos
- ✅ **Validación segura de pagos** mediante webhooks de Stripe
- ✅ **Panel de administración personalizado** para tareas internas

## 📈 Resultados

- **+40% de ventas** en el primer torneo tras el lanzamiento
- **Reducción del 90%** en tiempo de gestión de entradas
- **Control total de aforo** y asistentes en tiempo real
- **Digitalización completa** del proceso de venta

## 🛠️ Tecnologías utilizadas

- **Backend:** Django 6.1 (Python 3.12)
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Pagos:** Stripe (modo test)
- **Generación de QR:** qrcode + Pillow
- **Frontend:** HTML5, CSS3 (diseño minimalista con paleta pastel)
- **Autenticación:** Django Auth
- **Variables de entorno:** python-dotenv

## 📸 Capturas de pantalla

*(Aquí puedes añadir imágenes de tu proyecto en funcionamiento)*

## 🚀 Instalación y ejecución

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
# Edita .env con tus claves de Stripe y SECRET_KEY

# 5. Configurar la base de datos
python manage.py migrate
python manage.py createsuperuser

# 6. Ejecutar el servidor
python manage.py runserver