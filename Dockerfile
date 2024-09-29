FROM python:3


ENV TZ=America/Chicago
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y tzdata cron dos2unix && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "$TZ" > /etc/timezone && \
    apt-get clean


WORKDIR /code

COPY launch-app.sh /code/
RUN dos2unix /code/launch-app.sh
RUN chmod +x /code/launch-app.sh
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./miniproject1 /code/

CMD ["/code/launch-app.sh"]