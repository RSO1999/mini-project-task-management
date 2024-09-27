FROM python:3


ENV TZ=America/Chicago
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y tzdata cron && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "$TZ" > /etc/timezone && \
    apt-get clean


WORKDIR /code

COPY launch-app.sh /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./miniproject1 /code/

CMD ["./launch-app.sh"]