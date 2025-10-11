# Django with MongoDB & PostgreSQL

A Django application with dual database support: PostgreSQL for relational data and MongoDB for document storage. Containerized with Docker for easy deployment.

## 🚀 Features

- **Django 5.2+** - Latest Django framework
- **PostgreSQL** - Primary relational database for Django ORM
- **MongoDB** - NoSQL document database for flexible data storage
- **Docker & Docker Compose** - Containerized development environment
- **PyMongo** - Direct MongoDB integration
- **CORS Support** - Cross-origin resource sharing enabled
- **Static Files** - WhiteNoise for static file serving
- **Production Ready** - Includes Uvicorn, Daphne, and Gunicorn configurations

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)
- Git

## 🏗️ Project Structure

```
python_nitman/
├── apps/
│   └── nitapp/          # Django app
├── nitman/              # Django project settings
│   ├── settings.py      # Main settings
│   ├── pymongo.py       # MongoDB connection manager
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── staticfiles/         # Collected static files
├── docker-compose.yaml  # Docker services configuration
├── Dockerfile          # Application container
├── requirements.txt    # Python dependencies
├── scripts.sh          # Container startup script
├── entryPoint.sh       # Local startup script
└── manage.py           # Django management script
```

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kode-mafia008/django_with_mongodb.git
cd django_with_mongodb
```

### 2. Configure Environment Variables

Create a `.env` file (or copy from `.env.example`):

```bash
# PostgreSQL Configuration
POSTGRES_DB=nitman_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# MongoDB Configuration
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB_NAME=nitman_db

# Django Configuration
DJANGO_ENV=dev
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. Start the Application

#### Using Docker (Recommended)

```bash
# Make scripts executable
chmod +x entryPoint.sh scripts.sh

# Start all services
./entryPoint.sh
```

This will:
- Build the Docker image
- Start PostgreSQL, MongoDB, and Django containers
- Run migrations
- Collect static files
- Start the development server

#### Manual Docker Commands

```bash
# Build and start containers
docker compose up --build

# View logs
docker logs -f nitman

# Stop containers
docker compose down
```

### 4. Access the Application

- **Django App**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **MongoDB**: localhost:27017

## 💾 Database Usage

### PostgreSQL (Django ORM)

Standard Django models and ORM:

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
```

### MongoDB (PyMongo)

Direct MongoDB access via settings:

```python
from django.conf import settings

# Get MongoDB client and database
mongo_client = settings.MONGO_CLIENT
mongo_db = settings.MONGO_DB

# Use collections
users_collection = mongo_db['users']

# Insert document
users_collection.insert_one({
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Query documents
user = users_collection.find_one({'email': 'john@example.com'})
```

### MongoDB Connection Strings

**From within Docker containers:**
```
mongodb://root:example@mongo:27017/?authSource=admin
```

**From host machine:**
```
mongodb://root:example@localhost:27017/?authSource=admin
```

## 🛠️ Development Commands

```bash
# Access Django container shell
docker exec -it nitman bash

# Run migrations
docker exec -it nitman python manage.py migrate

# Create superuser
docker exec -it nitman python manage.py createsuperuser

# Collect static files
docker exec -it nitman python manage.py collectstatic

# Run tests
docker exec -it nitman python manage.py test

# Access Django shell
docker exec -it nitman python manage.py shell
```

## 📦 Dependencies

Key Python packages:

- `Django>=5.1` - Web framework
- `psycopg2-binary` - PostgreSQL adapter
- `pymongo` - MongoDB driver
- `python-dotenv` - Environment variable management
- `django-cors-headers` - CORS support
- `whitenoise` - Static file serving
- `uvicorn[standard]` - ASGI server
- `daphne` - Django Channels server
- `Pillow` - Image processing
- `django-redis` - Redis cache backend

See `requirements.txt` for complete list.

## 🚢 Production Deployment

### Production Servers

The `scripts.sh` file includes commented production server options:

```bash
# Uvicorn (ASGI)
uvicorn nitman.asgi:application --host 0.0.0.0 --port 8000 --workers 4

# Daphne (Django Channels)
daphne -p 8000 nitman.asgi:application

# Gunicorn (WSGI)
gunicorn -w 4 -b 0.0.0.0:8000 nitman.wsgi:application

# Gunicorn with Uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 nitman.asgi:application
```

### Production Settings

Update your `.env` for production:

```bash
DJANGO_ENV=production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=<strong-random-secret-key>
```

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use strong passwords for database credentials
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure proper `ALLOWED_HOSTS`
- Use HTTPS in production

## 📝 Common Issues

### Permission Denied Error

If you encounter `permission denied: /app/scripts.sh`:

```bash
chmod +x scripts.sh entryPoint.sh
docker compose down
docker compose up --build
```

### MongoDB Connection Error

Ensure MongoDB environment variables are set correctly in `.env`:

```bash
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example
```

### Static Files Not Loading

Run collectstatic:

```bash
docker exec -it nitman python manage.py collectstatic --noinput
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source. Please add your preferred license.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django documentation
- MongoDB documentation
- Docker documentation
