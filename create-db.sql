CREATE DATABASE instrumentcollector;

CREATE USER instrument_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE instrumentcollector TO instrument_admin;