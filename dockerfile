FROM python:3.9-alpine as build

LABEL maintainer="mcxvio@outlook.com"

WORKDIR /home
COPY . .

# separate install for uwsgi due to azure ative app deploy error.
RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers;
RUN pip install uwsgi
RUN apk del .build-deps;
# install remaining dependencies.
RUN pip install --no-cache-dir -r requirements.txt

#FROM build as test
#RUN python -m unittest tests/test_ebird_json.py
#RUN python -m unittest tests/test_ebird_api.py

FROM build as final
WORKDIR /app
COPY --from=build /home .
CMD uwsgi uwsgi.ini