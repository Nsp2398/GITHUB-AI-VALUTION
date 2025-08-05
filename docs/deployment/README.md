# Deployment Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (for production)
- Docker (optional)
- NGINX (for production)

## Development Environment

### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd server
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run development server:
```bash
flask run
```

### Frontend Setup

1. Install dependencies:
```bash
cd client
npm install
```

2. Start development server:
```bash
npm run dev
```

## Production Deployment

### Backend Deployment

1. Set up PostgreSQL:
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres createdb ucaas_valuation
sudo -u postgres createuser ucaas_user
```

2. Configure NGINX:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Set up Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 server.app:app
```

### Frontend Deployment

1. Build the application:
```bash
cd client
npm run build
```

2. Configure NGINX for frontend:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/client/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Docker Deployment

1. Build backend image:
```bash
docker build -t ucaas-backend ./server
```

2. Build frontend image:
```bash
docker build -t ucaas-frontend ./client
```

3. Run with docker-compose:
```yaml
version: '3.8'
services:
  backend:
    image: ucaas-backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/ucaas
    depends_on:
      - db
  
  frontend:
    image: ucaas-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ucaas
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Monitoring

1. Install monitoring tools:
```bash
pip install prometheus_client
pip install flask-prometheus-metrics
```

2. Set up Grafana dashboard for metrics visualization

3. Configure logging:
```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

## Backup Strategy

1. Database backups:
```bash
# Daily backups
pg_dump ucaas_valuation > backup_$(date +%Y%m%d).sql
```

2. File backups:
```bash
# Backup uploaded files
rsync -av /path/to/uploads/ /backup/uploads/
```

## Security Considerations

1. Enable HTTPS:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # ... rest of configuration
}
```

2. Set up firewall:
```bash
# Allow only necessary ports
ufw allow 80
ufw allow 443
ufw allow 5432  # PostgreSQL
```

3. Configure security headers:
```python
from flask_talisman import Talisman

Talisman(app,
    force_https=True,
    content_security_policy={
        'default-src': "'self'",
        'img-src': '*',
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"]
    }
)
```

## Maintenance

1. Regular updates:
```bash
# Update dependencies
pip install -r requirements.txt --upgrade
npm update
```

2. Monitor disk space:
```bash
# Set up disk space alerts
df -h | awk '{ print $5 " " $1 }' | while read output;
do
  usage=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  if [ $usage -ge 90 ]; then
    echo "Alert: Disk space critical"
  fi
done
```

3. Log rotation:
```
/var/log/ucaas/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 root adm
}
