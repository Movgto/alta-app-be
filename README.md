# Alta App - Backend API

Una aplicación Flask para la gestión de clientes y documentos con almacenamiento en base de datos MySQL.

## 🚀 Tecnologías Utilizadas

### Backend
- **Flask 3.1.1** - Framework web de Python
- **SQLAlchemy 2.0.42** - ORM para base de datos
- **Flask-SQLAlchemy 3.1.1** - Integración de SQLAlchemy con Flask
- **Flask-CORS 6.0.1** - Manejo de CORS para aplicaciones web
- **PyMySQL 1.1.0** - Driver MySQL puro en Python

### Seguridad y Autenticación
- **bcrypt 4.3.0** - Hashing de contraseñas
- **PyJWT 2.10.1** - Manejo de JSON Web Tokens

### Base de Datos
- **MySQL 8.0** - Base de datos relacional
- **Docker** - Containerización de la base de datos

### Herramientas de Desarrollo
- **python-dotenv 1.1.1** - Gestión de variables de entorno
- **gunicorn 20.1.0** - Servidor WSGI para producción

## 📋 Características

- ✅ CRUD completo para gestión de clientes
- ✅ Almacenamiento de documentos en base64
- ✅ Relaciones uno-a-uno entre clientes y documentos
- ✅ API RESTful con rutas versionadas
- ✅ Configuración flexible por entornos
- ✅ Soporte para CORS
- ✅ Containerización con Docker
- ✅ Despliegue a Google App Engine

## ⚙️ Configuración e Instalación

### Prerrequisitos
- Python 3.11+
- Docker y Docker Compose
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Movgto/alta-app-be.git
cd alta-app-be
```

### 2. Configurar Variables de Entorno
Crea un archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones:
```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui

# Database
MYSQL_ROOT_PASSWORD=tupassword
MYSQL_DATABASE=alta_app
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:tupassword@mysql_db/alta_app

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:4200

# API Configuration
API_VERSION=v1
```

## 🐳 Ejecución con Docker (Recomendado)

### 1. Construir y Ejecutar
```bash
docker-compose up --build
```

### 2. Ejecutar en Background
```bash
docker-compose up -d --build
```

### 3. Ver Logs
```bash
docker-compose logs -f
```

### 4. Detener Servicios
```bash
docker-compose down
```

## 🖥️ Ejecución Local (Desarrollo)

### 1. Crear Entorno Virtual
```bash
python -m venv .venv
```

### 2. Activar Entorno Virtual
```bash
# Windows
.venv\\Scripts\\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos MySQL
Asegúrate de tener MySQL ejecutándose y actualiza la `SQLALCHEMY_DATABASE_URI` en tu `.env`

### 5. Ejecutar la Aplicación
```bash
python start.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📚 API Endpoints

### Base URL
- **Local**: `http://localhost:5000/api/v1`
- **Producción**: `https://tu-dominio.com/api/v1`

### Clientes

#### 📋 Listar Todos los Clientes
```http
GET /api/v1/clients
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "company_name": "Empresa ABC",
    "representative_name": "Juan Pérez",
    "rfc": "ABC123456789",
    "email": "juan@empresa.com",
    "phone_number": "555-1234"
  }
]
```

#### 👤 Obtener Cliente por ID
```http
GET /api/v1/clients/{id}
```

**Respuesta:**
```json
{
  "id": 1,
  "company_name": "Empresa ABC",
  "representative_name": "Juan Pérez",
  "rfc": "ABC123456789",
  "email": "juan@empresa.com",
  "phone_number": "555-1234",
  "document": {
    "id": 1,
    "filename": "documento.pdf",
    "content_type": "application/pdf",
    "file_data": "base64_encoded_content",
    "upload_date": "2025-01-15T10:30:00"
  }
}
```

#### ➕ Crear Nuevo Cliente
```http
POST /api/v1/clients
Content-Type: application/json
```

**Body:**
```json
{
  "company_name": "Nueva Empresa",
  "representative_name": "María García",
  "rfc": "NEE123456789",
  "email": "maria@nuevaempresa.com",
  "phone_number": "555-5678",
  "document": {
    "filename": "contrato.pdf",
    "content_type": "application/pdf",
    "file_data": "base64_encoded_content"
  }
}
```

#### ✏️ Actualizar Cliente
```http
PUT /api/v1/clients/{id}
Content-Type: application/json
```

**Body:** (misma estructura que POST)

#### 🗑️ Eliminar Cliente
```http
DELETE /api/v1/clients/{id}
```

#### 📄 Obtener Documento de Cliente
```http
GET /api/v1/clients/{id}/document
```

## 🗄️ Modelos de Base de Datos

### Cliente (Client)
```sql
CREATE TABLE client (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    representative_name VARCHAR(100) NOT NULL,
    rfc VARCHAR(13) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL
);
```

### Documento (Document)
```sql
CREATE TABLE document (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    file_data MEDIUMBLOB NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    client_id INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE
);
```

## 🛠️ Desarrollo

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `FLASK_ENV` | Entorno de ejecución | `development`, `production` |
| `FLASK_DEBUG` | Modo debug | `True`, `False` |
| `SECRET_KEY` | Clave secreta para sesiones | `mi-clave-secreta` |
| `SQLALCHEMY_DATABASE_URI` | Conexión a base de datos | `mysql+pymysql://user:pass@host/db` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS | `http://localhost:3000` |

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contacto

**📧 Correo:** maromvz@gmail.com

## 🖥️ Repositorio Frontend

https://github.com/Movgto/alta-app-fe

---

⭐ Si este proyecto te ha sido útil, ¡dale una estrella!
