FROM python:3.8

# RUN adduser --disabled-password dbt
# USER dbt

WORKDIR /src
COPY ./requirements.txt /src/
RUN pip install -r requirements.txt
COPY ./src /src/



# COPY ./wait-for-initialization.sh /src/


EXPOSE 8000