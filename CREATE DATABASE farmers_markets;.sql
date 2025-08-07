CREATE DATABASE farmers_markets;

CREATE TABLE markets (
	FMID int4 NOT NULL UNIQUE,
	market_name varchar NOT NULL,
	website varchar NULL,
    facebook varchar NULL,
    twitter varchar NULL,
    youtube varchar NULL,
    other_media varchar NULL,
    CONSTRAINT markets_pk PRIMARY KEY (FMID)
);

CREATE TABLE states (
	state_id serial4 NOT NULL,
	state_full varchar NULL,
	CONSTRAINT states_pk PRIMARY KEY (state_id)
);

CREATE TABLE county (
	county_id serial4 NOT NULL,
	county_full varchar NULL,
	CONSTRAINT county_pk PRIMARY KEY (county_id)
);


CREATE TABLE address_market (
    FMID int4 NOT NULL UNIQUE,
    street varchar NOT NULL,
    county_id serial4 NOT NULL,
    states_id serial4 NOT NULL,
    zip int4 NULL,
    CONSTRAINT address_market_pk PRIMARY KEY (FMID),
    CONSTRAINT address_markets_fk FOREIGN KEY (FMID) REFERENCES markets(FMID),
    CONSTRAINT address_states_fk FOREIGN KEY (states_id) REFERENCES states(state_id),
    CONSTRAINT address_county_fk FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE pay (
    pay_id int4 NOT NULL UNIQUE,
    name_of_pay varchar NOT NULL,
    CONSTRAINT pay_pk PRIMARY KEY (pay_id)
);

CREATE TABLE markets_pay (
    markets_pay_id int4 NOT NULL UNIQUE,
    FMID int4 NOT NULL,
    pay_id int4 NOT NULL,
    CONSTRAINT markets_pay_pk PRIMARY KEY ( markets_pay_id),
    CONSTRAINT markets_markets_pay_fk FOREIGN KEY (FMID) REFERENCES markets(FMID),
	CONSTRAINT pay_markets_pay_fk FOREIGN KEY (pay_id) REFERENCES pay(pay_id)
);

CREATE TABLE categorias (
    categorias_id int4 NOT NULL UNIQUE,
    categorias_name varchar NOT NULL,
    CONSTRAINT categorias_pk PRIMARY KEY (categorias_id)
);

CREATE TABLE market_categories (
    market_categories_id int4 NOT NULL UNIQUE,
    FMID int4 NOT NULL,
    categorias_id int4 NOT NULL,
    CONSTRAINT market_categories_pk PRIMARY KEY (market_categories_id),
    CONSTRAINT market_categories_markets_fk FOREIGN KEY (FMID) REFERENCES markets(FMID),
    CONSTRAINT market_categories_categorias_fk FOREIGN KEY (categorias_id) REFERENCES categorias(categorias_id)
);

COPY markets (FMID, market_name,website, facebook, twitter, youtube, other_media) FROM markets;

COPY states (state_id, state_full) FROM states;

COPY county (county_id, county_full) FROM county;

COPY address_market (FMID, street, county_id, states_id, zip) FROM address_market;

COPY pay (pay_id, name_of_pay) FROM pay;

COPY markets_pay (markets_pay_id, FMID, pay_id) FROM markets_pay;

COPY categorias (categorias_id, categorias_name) FROM categorias;

COPY market_categories (market_categories_id, FMID, categorias_id) FROM market_categories;