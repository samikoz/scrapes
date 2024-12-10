FROM python:slim-buster

RUN apt update && apt --assume-yes install sqlite3
COPY . /scrapes

RUN mkdir -p /scrapes/camerascrape/db
RUN bash -c '[[ ! -f /scrapes/camerascrape/db/camerascrape.db ]] && sqlite3 /scrapes/camerascrape/db/camerascrape.db < /scrapes/camerascrape/initialise.sql'

RUN pip install -r /scrapes/requirements.txt
WORKDIR /scrapes/camerascrape

CMD ["python", "crawl.py"]
