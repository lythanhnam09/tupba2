-- Run this every time you connect to it (even when you using DBeaver) (if you want to):
--PRAGMA foreign_keys = ON;

drop table if exists album_image;
drop table if exists album;
drop table if exists feed_tag;
drop table if exists feed;
drop table if exists booru_filter_tag;
drop table if exists booru_filter;
drop table if exists history;
drop table if exists image_tag;
drop table if exists image_size;
drop table if exists image;
drop table if exists tag;

create table tag (
	id integer primary key, --auto
	name text unique,
	color text,
	sort_index integer,
	description text
);

create table image (
	id integer primary key,
	name text,
	description text,
	thumbnail_generated integer,
	mime_type text,
	animated integer,
	extension text,
	upvote integer,
	downvote integer,
	score integer,
	fave integer,
	comment_count integer,
	wilson_score real,
	uploader text,
	image_size integer,
	width integer,
	height integer,
	link_view text,
	link_source text,
	duration text,
	delete_reason text,
	created_at text,
	updated_at text
);

create table image_size (
	image_id integer,
	link text,
	name text,
	size_index integer,
	primary key (image_id, link),
	foreign key (image_id) references image(id) on delete cascade
);

create table image_tag (
	image_id integer,
	tag_id integer,
	primary key (image_id, tag_id),
	foreign key (image_id) references image(id) on delete cascade,
	foreign key (tag_id) references tag(id) on delete cascade
);

create table history (
	image_id integer primary key,
	view_timestamp integer,
	view_count integer,
	foreign key (image_id) references image(id) on delete cascade
);

create table booru_filter (
	id integer primary key,
	name text,
	color text,
	show_count integer,
	spoiler_count integer,
	hide_count integer,
	spoiler_list text,
	filter_text text,
	sort_index integer
);

create table feed (
	id integer primary key, --auto
	name text,
	color text,
	show_count integer,
	spoiler_count integer,
	hide_count integer,
	spoiler_list text,
	filter_text text
);

create table album (
	id integer primary key, --auto
	thumbnail_id integer,
	name text,
	color text,
	foreign key (thumbnail_id) references image(id) on delete set null
);

create table album_image (
	album_id integer,
	image_id integer,
	sort_index integer,
	primary key (album_id, image_id),
	foreign key (album_id) references album(id) on delete cascade,
	foreign key (image_id) references image(id) on delete cascade
);
