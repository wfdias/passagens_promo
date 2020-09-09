DO
$do$
DECLARE
  _db TEXT := 'bd_belvitur'; -- banco de dados a ser criado
  _user TEXT := 'user_belvitur'; 
  _password TEXT := 'swnvlD'; 
BEGIN
	-- criação do usuário de acesso da aplicacao 
	IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'user_belvitur') THEN 
		CREATE ROLE user_belvitur WITH LOGIN PASSWORD 'swnvlD' CREATEDB;
		COMMIT;
	END IF;
	-- criação do banco de dados
	CREATE EXTENSION IF NOT EXISTS dblink; -- enable extension 
	IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = _db) THEN
    	PERFORM dblink_connect('host=localhost user=' || _user || ' password=' || _password || ' dbname=' || current_database());
    	PERFORM dblink_exec('CREATE DATABASE ' || _db || ' WITH OWNER = ' || _user || ' CONNECTION LIMIT = -1');
		--PERFORM dblink_exec('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ' || _user);
		COMMIT;
	END IF;
END;
$do$