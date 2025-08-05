FROM python:3.12.4

WORKDIR /app

COPY ./backend/library/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./backend/library /app


EXPOSE 8000

CMD sh -c "python manage.py makemigrations && \
           python manage.py migrate && \
           python manage.py runserver 0.0.0.0:8000"

