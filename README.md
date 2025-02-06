# Setting Up an Apache2 Server for a Flask Application

This guide provides step-by-step instructions to set up an Apache2 server to host a Flask application on Ubuntu.

## Prerequisites
- Ubuntu system
- Python 3 installed
- Apache2 installed

## Steps to Set Up the Server

### 1. Install Flask
```sh
pip3 install flask requests
```

### 2. Navigate to the Application Directory
```sh
cd /opt/flask-app/
```

### 3. Activate Virtual Environment
```sh
source flask-venv/bin/activate
```

### 4. Install Dependencies
```sh
pip3 install flask requests
```

### 5. Run Flask Application Locally (Optional)
```sh
flask run --host=0.0.0.0
```

### 6. Deactivate Virtual Environment
```sh
deactivate
```

### 7. Install Apache and WSGI Module
```sh
sudo apt-get install libapache2-mod-wsgi-py3
```

### 8. Create and Configure WSGI File
```sh
sudo nano /opt/flask-app/flask-app.wsgi
```
Add the following content to `flask-app.wsgi`:
```python
import sys
import logging
sys.path.insert(0, "/opt/flask-app")

from app import app as application
```

### 9. Configure Apache Virtual Host
```sh
sudo nano /etc/apache2/sites-available/flask.conf
```
Add the following content to `flask.conf`:
```apache
<VirtualHost *:80>
    ServerName your_domain_or_IP
    WSGIDaemonProcess flask-app threads=5
    WSGIScriptAlias / /opt/flask-app/flask-app.wsgi

    <Directory /opt/flask-app>
        Require all granted
    </Directory>

    Alias /static /opt/flask-app/static
    <Directory /opt/flask-app/static/>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/flask-error.log
    CustomLog ${APACHE_LOG_DIR}/flask-access.log combined
</VirtualHost>
```

### 10. Enable the New Site and Restart Apache
```sh
sudo a2ensite flask.conf
apachectl -t
sudo systemctl restart apache2
```

## API Endpoints

### 1. Welcome Endpoint
```http
GET /
```
Response:
```json
"HNG Backend Stage 1 Task"
```

### 2. Number Classification API
```http
GET /api/classify-number?number=<int>
```
#### Features:
- Checks if a number is **prime**
- Determines if it is **perfect**
- Identifies if it is an **Armstrong number**
- Checks its **parity (odd/even)**
- Fetches a **fun fact** about the number from the Numbers API

#### Example Response:
```json
{
    "number": 7,
    "is_prime": true,
    "is_perfect": false,
    "properties": ["odd"],
    "digit_sum": 7,
    "fun_fact": "7 is the number of wonders in the world."
}
```

## Verification
Check if Apache is running:
```sh
sudo systemctl status apache2
```

Visit your server's IP or domain in a browser to confirm Flask is running under Apache.

## Troubleshooting
- Check Apache logs for errors:
```sh
tail -f /var/log/apache2/error.log
```
- Ensure the Flask application runs correctly before deploying to Apache.


