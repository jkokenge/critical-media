-- Table: cmlproject_medialist

-- DROP TABLE cmlproject_medialist;

CREATE TABLE cmlproject_medialist
(
  id serial NOT NULL,
  site_id integer NOT NULL,
  title character varying(500) NOT NULL,
  slug character varying(2000),
  name character varying(100) NOT NULL,
  CONSTRAINT cmlproject_medialist_pkey PRIMARY KEY (id ),
  CONSTRAINT cmlproject_medialist_site_id_fkey FOREIGN KEY (site_id)
      REFERENCES django_site (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE cmlproject_medialist
  OWNER TO cml;

-- Index: cmlproject_medialist_site_id

-- DROP INDEX cmlproject_medialist_site_id;

CREATE INDEX cmlproject_medialist_site_id
  ON cmlproject_medialist
  USING btree
  (site_id );


-- Table: cmlproject_medialist_listed_media

-- DROP TABLE cmlproject_medialist_listed_media;

CREATE TABLE cmlproject_medialist_listed_media
(
  id serial NOT NULL,
  medialist_id integer NOT NULL,
  mediaartefact_id integer NOT NULL,
  CONSTRAINT cmlproject_medialist_listed_media_pkey PRIMARY KEY (id ),
  CONSTRAINT cmlproject_medialist_listed_media_mediaartefact_id_fkey FOREIGN KEY (mediaartefact_id)
      REFERENCES cmlproject_mediaartefact (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT medialist_id_refs_id_a47530d FOREIGN KEY (medialist_id)
      REFERENCES cmlproject_medialist (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT cmlproject_medialist_listed_m_medialist_id_mediaartefact_id_key UNIQUE (medialist_id , mediaartefact_id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE cmlproject_medialist_listed_media
  OWNER TO cml;

-- Index: cmlproject_medialist_listed_media_mediaartefact_id

-- DROP INDEX cmlproject_medialist_listed_media_mediaartefact_id;

CREATE INDEX cmlproject_medialist_listed_media_mediaartefact_id
  ON cmlproject_medialist_listed_media
  USING btree
  (mediaartefact_id );

-- Index: cmlproject_medialist_listed_media_medialist_id

-- DROP INDEX cmlproject_medialist_listed_media_medialist_id;

CREATE INDEX cmlproject_medialist_listed_media_medialist_id
  ON cmlproject_medialist_listed_media
  USING btree
  (medialist_id );



