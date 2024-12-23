# Flatscrape
Scraping flat offers from OLX.

Contains Docker project meant to be started periodically by some devops process.

Sends emails with links to the newest unique offers conditioned on filtering criteria. Contains sqlite database with past offers for uniqueness checks.

## Contents
 - `pipelines.py` contains filtering criteria
 - `crawl.py` main script file
 - `db/flatscrape.db` sqlite file
 - `logs`

## How to launch
first of all need to reset furtive.py file with data required in crawl.py. then:

### as a script from venv
needs to have the database initialised. if it's not, run from the outer `flatscrape` directory:
> $ mkdir -p db
>
> $ sqlite3 db/flatscrape.db < initialise.sql

and to run:

> $ python crawl.py

### manually just the spider, venv
the result will be logged to stdout. from the outer `flatscrape` directory:
>$ scrapy crawl olx

parameters can be added with the `-a` parameter from the following:
- name
- city
- price_from
- price_to
- radius
- initial_pages, default = 1

### Docker
from the top-level git directory:
>$ docker build -t flatscrape .
> 
>$ docker run -v flatscrape-db:/scrapes/flatscrape/db --mount type=bind,source=/home/sami/dev/scrapes/flatscrape/logs,target=/scrapes/flatscrape/logs flatscrape

this is intended to be run by the devops process.

debugging - entering the container
>$ docker run -it -v flatscrape-db:/scrapes/flatscrape/db --mount type=bind,source=/home/sami/dev/scrapes/flatscrape/logs,target=/scrapes/flatscrape/logs flatscrape bash

## Details
The project relies on the database storing past offers. If the database file is not created manually,
the Docker process will create it. It will then appear on the host filesystem (bind mound) and every change
to the file on either the host or Docker will trigger change to the other.

## Debugging
take troublesome url and run the following. need to dupa-debug.
>$ scrapy parse --spider=olx -c parse_offer -d 2 -v <item_url>

## TODO
find some way of reusing containers. at the moment it seems every invocation creates a new one (confirm it)

# Camerascrape
Scraping cameras from optyczne.pl

Not launched using docker but with a Bash script `crawl_lexicon.sh`.

## TODO
Setup persistence pipeline

# News
scraping news from the web
## DONE
written spider, persisting pipeline, initialise.sql
basic working crawl.py logic

## TODO
write Printer loading from db and printing to output
move previous Docker file inside flatscrape, create separate