drop table if exists books;
create table books (
  id integer primary key autoincrement,
  title text not null,
  author text not null,
  description text not null,
  isbn text not null
);