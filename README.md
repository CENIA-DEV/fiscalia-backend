# Fiscalía backend
Backend para piloto proyecto fiscalía. Contempla la descarga de RUCs desde SAF y la creación y mantención de una BB.DD. postgres en local para acceder a los datos vía API.

## Instalación
Crear ambiente virtual y ejecutar `pip install -r requirements/base.txt`. Correr también `sudo apt-get install libpq-dev` para poder usar las librerías de postgres. Setear las variables de entorno con `cp .env.example .env`, e introducir las credenciales tanto del acceso al SAF como del postgres montado localmente.

## Uso
El archivo `update_postgres.py` está pensado para ejecutarse una vez al día mediante un crontab, y actualiza las causas en el postgres. Para levantar la API en el puerto 8000 ejecutar `make run`.

## Por hacer
1. Incorporación de modelos de ML en su primera versión
2. Agregar login a la API para acceso de usuarios
