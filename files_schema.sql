CREATE TABLE files (
  hash text PRIMARY KEY NOT NULL,
  hasavif integer,
  haswebp integer,
  width integer NOT NULL,
  height integer NOT NULL,
  name text NOT NULL
);
