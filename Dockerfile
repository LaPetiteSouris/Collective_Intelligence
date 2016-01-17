FROM python:2.7
MAINTAINER Appturbo <contact@appturbo.it>



COPY . /src
WORKDIR /src
RUN ln -s /usr/include/freetype2 /usr/local/include/freetype
RUN pip install -r /src/dev-requirements.txt 



