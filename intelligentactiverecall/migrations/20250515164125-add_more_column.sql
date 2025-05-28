
-- +migrate Up
ALTER TABLE english_most_forgotten ADD COLUMN definition TEXT;
ALTER TABLE english_most_forgotten ADD COLUMN example_sentence TEXT;
ALTER TABLE english_most_forgotten ADD COLUMN context TEXT;
-- +migrate Down
ALTER TABLE english_most_forgotten DROP COLUMN context;
ALTER TABLE english_most_forgotten DROP COLUMN example_sentence;
ALTER TABLE english_most_forgotten DROP COLUMN definition;
