CREATE TABLE `person` (
	`id_person`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`fisrtname`	TEXT NOT NULL,
	`middlename`	TEXT,
	`lastname`	TEXT NOT NULL,
	`suffix`	INTEGER
);

CREATE TABLE `project` (
	`id_proj`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nome`	TEXT NOT NULL
);

CREATE TABLE `source` (
	`id_source`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`date`	TEXT NOT NULL,
	`title`	TEXT NOT NULL,
	`subtitle`	TEXT,
	`local`	TEXT
);

CREATE TABLE `article` (
	`id_source`	INTEGER NOT NULL,
	`doi`	INTEGER NOT NULL UNIQUE,
	`journal`	TEXT NOT NULL,
	`vol_journal`	INTEGER NOT NULL,
	`fascicle`	TEXT NOT NULL,
	PRIMARY KEY(`id_source`)
);

CREATE TABLE `site` (
	`id_source`	INTEGER NOT NULL,
	`link`	TEXT NOT NULL UNIQUE,
	`dt_access`	TEXT NOT NULL,
	PRIMARY KEY(`id_source`)
);

CREATE TABLE `book` (
	`id_source`	INTEGER NOT NULL,
	`isbn`	TEXT NOT NULL,
	`publisher`	TEXT NOT NULL,
	`series_book`	TEXT,
	`edition_book`	INTEGER NOT NULL,
	`vol_book`	INTEGER,
	PRIMARY KEY(`id_source`,`isbn`)
);

CREATE TABLE `person_contribute_source` (
	`id_person`	INTEGER NOT NULL,
	`id_source`	INTEGER NOT NULL,
	`type` TEXT NOT NULL,
	PRIMARY KEY(`id_person`,`id_source`),
	FOREIGN KEY(`id_person`) REFERENCES `person_contribute_source`(`id_person`),
	FOREIGN KEY(`id_source`) REFERENCES `source`(`id_source`)
);


CREATE TABLE `project_quote_source` (
    `idproj` INTEGER NOT NULL,
    `id_source` INTEGER NOT NULL,
    `pg_start` INTEGER, `pg_end` INTEGER,
    PRIMARY KEY(`idproj`,`id_source`),
    FOREIGN KEY(`id_source`) REFERENCES `source`(`id_source`),
    FOREIGN KEY(`idproj`) REFERENCES `project_quote_source`(`id_proj`)
);