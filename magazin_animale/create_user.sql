CREATE USER blanita_user WITH PASSWORD 'blanita';
CREATE DATABASE blanita_db OWNER blanita_user ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE blanita_db TO blanita_user;