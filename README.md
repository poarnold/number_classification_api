# Setting Up an Apache2 Server for the Flask Application

This guide provides a step-by-step instructions to set up an Apache2 server to host the Flask Backend application - `number_api_app.py`  on Ubuntu.

## Prerequisites
- Ubuntu system (22.04) 

Update the package installers:
```sh

sudo apt-get update -y && apt-get upgrade -y
```
- Python 3, Pip and Venv installed
```sh

sudo apt-get install python3 python3-pip python3-venv -y
```
Create a symbolic link of **python3** installation to **python** keyword

```sh
sudo ln -s /usr/bin/python3 /usr/bin/python
```

- Apache2 installed
```sh

sudo apt install apache2 -y
```

## Steps to Set Up the Server

Python 3.11+ on Debian systems currently do not allow you to install specific packages system wide with `pip3` or `pip`.
`apt-get` and `apt`. A virtual environment is recommended using [venv](https://virtualenv.pypa.io/en/latest/user_guide.html) or  [pipx](https://pipx.pypa.io/latest/installation/), or you can run the application as root user *[This is not recommended]*

Switching to root user
```sh
sudo -i || sudo su -
```
### 1. Create Application Directory and Virtual Environment 
```sh
mkdir -p /opt/flask-app
cd /opt/flask-app
python -m venv flask-venv
```

### 2. Activate Virtual Environment
```sh
source flask-venv/bin/activate
```

### 3. Install Dependencies
```sh
pip3 install flask requests
```

### 4. Create Application file in Application Directory

```sh
sudo nano app.py
```
Paste the contents of `number_api_app.py` file into `app.py`


```sh
export FLASK_APP=app.py
```
### 5. Run Flask Application Locally (Optional)
```sh
flask run --host=0.0.0.0
```

### 6. Deactivate Virtual Environment
```sh
deactivate
```

### 7. Install Apache Python WSGI Module
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
    DocumentRoot /opt/flask-app/

    WSGIDaemonProcess app user=$USER group=$USER threads=5 python-home=/opt/flask-app/flask-venv
    WSGIScriptAlias / /opt/flask-app/flask-app.wsgi

    ErrorLog ${APACHE_LOG_DIR}/flask-error.log
    CustomLog ${APACHE_LOG_DIR}/flask-access.log combined
    
    <Directory /opt/flask-app>
        WSGIProcessGroup app
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Require all granted
    </Directory>

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

![Application_Endpoint_Test](/Screenshot.png)

## Troubleshooting
- Check Apache logs for errors:
```sh
tail -f /var/log/apache2/error.log
```
- Ensure the Flask application runs correctly before deploying to Apache.

## Troubleshooting Documentations
- [X] [Rosehosting](https://www.rosehosting.com/blog/how-to-install-flask-on-ubuntu-22-04-with-apache-and-wsgi/)
- [X] [Flask Documentation](https://flask.palletsprojects.com/en/stable/deploying/mod_wsgi/)
- [x] [Apache2 Configuration](https://blog.geekinstitute.org/2024/11/apache2-virtual-host-configuration.html#7-ssltls-configuration)
- [X] [Flask, Apache and Wsgi](https://www.thegeeksearch.com/setup-flask-with-apache-and-wsgi/)
- [X] [Graycode](https://graycode.ie/blog/deploy-python-flask-app-on-apache2-with-mod-wsgi/)

## Enabling HTTPS
- <https://techexpert.tips/apache/enable-https-apache/>
- <https://plainenglish.io/blog/how-to-securely-deploy-flask-with-apache-in-a-linux-server-environment>


