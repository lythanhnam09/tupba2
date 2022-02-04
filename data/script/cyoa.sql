-- Run this every time you connect to it (even when you using DBeaver):
--PRAGMA foreign_keys = ON;

drop table if exists post_reply_by;
drop table if exists post_reply_to;
drop table if exists post_image;
drop table if exists post;
drop table if exists cyoa_thread;
drop table if exists thread;
drop table if exists cyoa_tag;
drop table if exists tag;
drop table if exists cyoa;

create table if not exists cyoa (
	id integer primary key,
	name text,
	short_name text,
	description text,
	image_link text,
	cyoa_type integer,
	board text,
	chan text,
	is_live integer,
	status integer,
	last_post_time integer,
	first_post_time integer,
	quest_time integer,
	total_image integer,
	total_post integer,
	total_thread integer,
	total_fanart integer,
	word_count integer,
	lewd_exist integer,
	image_path text,
	save_status integer
);

create table if not exists fanart (
	id integer primary key,
	cyoa_id integer,
	title text,
	artist text,
	is_lewd integer,
	link text unique,
	offline_link text,
	status_code integer,
	foreign key (cyoa_id) references cyoa(id) on delete cascade
);

create table if not exists tag (
	id integer primary key,
	name text unique,
	color text,
	sort_index integer
);

create table if not exists cyoa_tag (
	cyoa_id integer,
	tag_id integer,
	primary key (cyoa_id, tag_id),
	foreign key (cyoa_id) references cyoa(id) on delete cascade,
	foreign key (tag_id) references tag(id) on delete cascade
);

create table if not exists thread (
	id integer primary key,
	title text,
	is_canon integer,
	thread_date integer,
	thread_image text,
	op_name text,
	chan text,
	board text,
	total_op_post integer,
	total_post integer,
	total_word integer,
	thread_time integer,
	current_page integer
);

create table if not exists cyoa_thread (
	cyoa_id integer,
	thread_id integer,
	primary key (cyoa_id, thread_id),
	foreign key (cyoa_id) references cyoa(id) on delete cascade,
	foreign key (thread_id) references thread(id) on delete cascade
);

create table if not exists post (
	id integer primary key,
	thread_id integer,
	title text,
	username text,
	tripcode text,
	comment_plain text,
	comment_html text,
	is_qm integer,
	post_date integer,
	foreign key (thread_id) references thread(id) on delete cascade
);

create table if not exists post_image (
	post_id integer,
	alt_id integer, --0:normal 1:lewd (or other alt num)
	alt_name text,
	filename text,
	link text,
	offline_link text null,
	status_code integer, -- 0:notyet 200:ok 404:notfound (same as http status code)
	primary key (post_id, alt_id),
	foreign key (post_id) references post(id) on delete cascade
);

create table if not exists post_reply_to (
	post_id integer,
	reply_id integer,
	primary key (post_id, reply_id),
	foreign key (post_id) references post(id) on delete cascade,
	foreign key (reply_id) references post(id) on delete cascade
);

create table if not exists post_reply_by (
	post_id integer,
	reply_id integer,
	primary key (post_id, reply_id),
	foreign key (post_id) references post(id) on delete cascade,
	foreign key (reply_id) references post(id) on delete cascade
);




