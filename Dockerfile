# Base Image
FROM python:3.8
RUN pip install pipenv

WORKDIR /code

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

VOLUME /code

CMD /bin/bash && wait
