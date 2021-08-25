CREATE TABLE galleries (
	id			integer PRIMARY KEY NOT NULL,
	type			text NOT NULL,
	title 			text NOT NULL,
	language 		text,
	language_localname 	text,
	japanese_title 		text,
	tag_ids 		text,
	file_ids 		text,
	date 			text
);

CREATE TABLE tags (
  full TEXT PRIMARY KEY NOT NULL,
  type TEXT,
  name TEXT NOT NULL
);
