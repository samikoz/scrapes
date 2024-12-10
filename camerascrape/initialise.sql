create table flats(title_hash str CONSTRAINT title_hash PRIMARY KEY, title text NOT NULL, url text NOT NULL, creation_time int NULL, scrape_time int NOT NULL);
insert into flats values ('x', 'fake', 'https://fake_url.com', NULL, 1651836036);
.quit