ALTER TABLE cmlproject_glossaryterm ADD COLUMN auto_highlight BOOL;

update cmlproject_glossaryterm set auto_highlight = True;