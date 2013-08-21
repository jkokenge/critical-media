alter table cmlproject_glossaryterm add column auto_highlight bool;
update cmlproject_glossaryterm set auto_highlight = True;