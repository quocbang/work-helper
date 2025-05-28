-- +migrate Up
CREATE TABLE IF NOT EXISTS forgotten_status (
  id VARCHAR(2) PRIMARY KEY,
  order int NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "public"."forgotten_status" ("created_at", "id", "order_number") VALUES ('2025-05-12 16:20:15.942788', 'A1', 1), ('2025-05-12 16:20:15.942788', 'A2', 2), ('2025-05-12 16:20:15.942788', 'B1', 3), ('2025-05-12 16:20:15.942788', 'B2', 4), ('2025-05-12 16:20:15.942788', 'C1', 5), ('2025-05-12 16:20:15.942788', 'C2', 6)

CREATE TYPE english_type AS ENUM('word', 'phrase');
CREATE TABLE IF NOT EXISTS english_most_forgotten (
  id SERIAL PRIMARY KEY,
  content text NOT NULL,
  type english_type DEFAULT 'word' NOT NULl,
  difficult_score smallint NOT NULL,
  status_id VARCHAR(2) NOT NULL DEFAULT 'A1',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);
ALTER TABLE english_most_forgotten ADD CONSTRAINT uidx_content UNIQUE (content);
ALTER TABLE english_most_forgotten ADD CONSTRAINT fk_english_most_forgotten_status_id FOREIGN KEY (status_id) REFERENCES forgotten_status(id)
CREATE TABLE IF NOT EXISTS forgotten_review_histories (
  id SERIAL PRIMARY KEY,
  english_most_forgotten_id BIGINT NOT NULL,  
  status VARCHAR(2) NOT NULL,
  user_answer text NOT NULL,
  reviewed_by_ai text NOT NULL,
  reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT fk_forgotten_review_histories_english_most_forgotten_id FOREIGN KEY (english_most_forgotten_id) REFERENCES english_most_forgotten(id)
);
-- +migrate Down
DROP TABLE IF EXISTS forgotten_review_histories;
DROP TABLE IF EXISTS english_most_forgotten;
DROP TYPE IF EXISTS english_type;
DROP TABLE IF EXISTS forgotten_status;
