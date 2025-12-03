🏢 Sistema de Gestión de Recursos Humanos (RRHH)

Sistema integral de gestión de recursos humanos desarrollado en Django, que permite administrar empleados, nóminas, capacitaciones, contratos y otros procesos relacionados con la gestión del personal.



✨ Características Principales
Módulos del Sistema

Gestión de Personal: Administración completa de empleados, cargos, áreas y datos personales.

Nómina y Pagos: Gestión de roles de pago, sobretiempos, rubros y frecuencias.

Capacitación: Administración de cursos, proveedores, solicitudes y certificados.

Selección de Personal: Gestión de ofertas laborales, candidatos, entrevistas y contratos.

Control de Asistencia: Registro biométrico, jornadas y marcadas de reloj.

Vacaciones y Permisos: Calendario de vacaciones y gestión de permisos.

Seguridad: Gestión de usuarios, roles, permisos y menús.

Gestión de Ventas (opcional): Categorías, productos, clientes y facturación.

⚙️ Requisitos Previos

Python 3.8 o superior

PostgreSQL 12 o superior

wkhtmltopdf (para generación de PDFs)

🚀 Instalación
1. Clonar el repositorio
git clone <url-del-repositorio>
cd rrhhs

2. Crear y activar entorno virtual
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate

3. Instalar dependencias
pip install -r requi.txt

4. Configurar variables de entorno

Crear un archivo .env en la raíz del proyecto con la siguiente estructura:

DB_ENGINE=django.db.backends.postgresql
DB_DATABASE=nombre_base_datos
DB_USERNAME=usuario_postgres
DB_PASSWORD=contraseña_postgres
DB_SOCKET=localhost
DB_PORT=5432

EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=contraseña_aplicacion

5. Configurar la base de datos
# Crear la base de datos en PostgreSQL
psql -U postgres
CREATE DATABASE nombre_base_datos;
\q

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

6. Crear superusuario
python manage.py createsuperuser

7. Ejecutar el servidor
python manage.py runserver
