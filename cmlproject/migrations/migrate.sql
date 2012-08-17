alter table cmlproject_mediaartefact add column thumbnail_url character varying(200);

alter table cmlproject_mediaartefact add column media_url character varying(200);

update cmlproject_mediaartefact set thumbnail_url = replace(thumbnail_url, '260x180', '210x180')

ALTER TABLE "cmlproject_topic" ADD COLUMN "related_tag_id" integer;
ALTER TABLE "cmlproject_topic" ADD CONSTRAINT "related_tag_id_refs_id_67e9aadc" 
FOREIGN KEY ("related_tag_id") REFERENCES "cmlproject_tag" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "cmlproject_topic" ALTER COLUMN "related_tag_id" DROP NOT NULL;