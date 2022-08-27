FROM python:3.7-alpine3.15

RUN apk update
RUN apk add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev make cmake libpq-dev postgresql postgresql-contrib tk

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "TallerChaPin/manage.py", "runserver" ]
