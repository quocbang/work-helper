
-- +migrate Up
ALTER TABLE english_most_forgotten ADD COLUMN content_vector tsvector;
CREATE INDEX idx_content_vector ON english_most_forgotten USING GIN(content_vector); 
-- +migrate Down
ALTER TABLE english_most_forgotten DROP COLUMN content_vector;
