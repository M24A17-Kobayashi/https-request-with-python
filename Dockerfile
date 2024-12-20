FROM python:3.11.0
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt-get install graphviz -y


RUN python -m pip install numpy
RUN python -m pip install matplotlib
RUN python -m pip install beautifulsoup4
RUN python -m pip install requests
RUN python -m pip install python-dotenv
RUN python -m pip install icecream
RUN python -m pip install pandas