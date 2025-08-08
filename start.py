import os
from app import create_app
import pymysql
pymysql.install_as_MySQLdb()

# Determina que configuración usar
config_name = os.environ.get('FLASK_ENV', 'development')
print(f"Using configuration: {config_name}")
app = create_app(config_name)

print(f"Running in {app.config.get('FLASK_ENV')} mode")

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False))