CREATE USER dl_user WITH PASSWORD 'pgadmin123' CREATEDB;
CREATE DATABASE dl_pg_db
    WITH 
    OWNER = dl_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;