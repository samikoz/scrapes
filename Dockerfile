FROM python:slim-buster

RUN apt update && apt --assume-yes install sqlite3
COPY . /scrapes

RUN mkdir -p /scrapes/flatscrape/db
RUN bash -c '[[ ! -f /scrapes/flatscrape/db/flatscrape.db ]] && sqlite3 /scrapes/flatscrape/db/flatscrape.db < /scrapes/flatscrape/initialise.sql'

RUN pip install -r /scrapes/requirements.txt
WORKDIR /scrapes/flatscrape

CMD ["python", "crawl.py"]
