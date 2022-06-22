FROM python:3.9.1-alpine3.12

RUN pip install -U pip

RUN apk add --update postgresql-dev \
                     gcc \
                     python3-dev \
                     musl-dev \
					 build-base \
					 linux-headers \
					 pcre-dev \
					 py-pip \
					 curl \
					 openssl\
                     git\
					 zlib-dev\
					 jpeg-dev\
					 libffi-dev\
					 cairo-dev\
					 pango-dev\
					 gdk-pixbuf-dev\
					 fontconfig\
					 ttf-dejavu

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .
