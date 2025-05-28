
-- +migrate Up
CREATE OR REPLACE FUNCTION upsert_content_vector()
   RETURNS TRIGGER
   LANGUAGE PLPGSQL
AS $$
DECLARE
	new_rec RECORD;
BEGIN
	new_rec := NEW;
  CASE TG_OP
    WHEN 'UPDATE' THEN
    	IF (new_rec.content <> OLD.content) THEN
	  		new_rec.content_vector = to_tsvector('english', coalesce(new_rec.content, ''));
      END IF;
    WHEN 'INSERT' THEN
    	new_rec.content_vector = to_tsvector('english', coalesce(new_rec.content, ''));
  END CASE;
      
  return new_rec;
END;
$$
-- Create Trigger to execute upsert_content_vector
CREATE OR REPLACE TRIGGER upsert_content_vector
	BEFORE UPDATE OR INSERT ON english_most_forgotten
  FOR EACH ROW
  EXECUTE FUNCTION upsert_content_vector();
-- +migrate Down
DROP TRIGGER upsert_content_vector;
DROP FUNCTION upsert_content_vector;
