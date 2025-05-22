FROM python:3.11-slim

WORKDIR ./

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py makemigrate && python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py import_segments.py && python manage.py import_sensors.py && python manage.py runserver"]
