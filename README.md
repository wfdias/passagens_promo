# Desafio Belvitur (Passagens Promo)

Pré-requisitos:

* Instalação do Anaconda versão 2020.02 (https://docs.anaconda.com/anaconda/install/windows/)
* Instalação do banco de dados Postgres versão 12 (https://www.postgresql.org/download/windows/)
* Instalação do PHP versão 7.4 (https://windows.php.net/download/)

Procedimentos de execução:

1) Após a instalação do banco de dados Postgres, crie o banco de dados e usuário de acesso através do script "ScriptCriacaoBancoUsuario_Postgres.sql"

2) Após a criação do banco de dados "bd_belvitur", crie as tabelas dentro deste banco através so script "ScriptCriacaoTabelas_Postgres.sql". Certifique-se que após a criação das tabelas, o owner das mesmas esteja setado para o usuário "user_belvitur".

3) Crie uma virtualenv para iniciar o projeto de importação de dados no python:
	-- Instalação do virtual enviroment
	pip3 install virtualenv

	-- Criando uma virtualenv
	virtualenv --system-site-packages -p python3 ./venv/

	-- Ativando a virtualenv criada
	.\venv\Scripts\activate

	-- Caso necessário, segue abaixo o comando de instalação de algumas bibliotecas do python utilizados no script:
	pip3 install pandas
	pip3 install sqlalchemy
	pip3 install psycopg2
	pip3 install pytz
	pip3 install requests

4) Execute o script de importação de dados de voos:
	python carga_voos_diarios.py

5) Para visualizar os dados, é preciso configurar o servidor PHP primeiramente. Para isso execute os seguintes passos:
	
	* Descompacte a pasta do servidor PHP em C:\
	* Renomeie a pasta para "PHP"
	* Incluir o caminho "C:\PHP" no PATH do sistema (variáveis de ambiente do Windows)
	* Renomeie o arquivo "php.ini-development" para "php.ini"
	* Edite o arquivo "php.ini" e descomente (remova o ';') as seguintes configurações para habilitar o acesso ao banco postgres:
		extension_dir = "ext" (linha 757)
		extension=pdo_pgsql (linha 930)
		extension=pgsql (linha 932)

6) Acesse a pasta "PassagensPromo" e execute o seguinte comando através do prompt de comando do windows para iniciar o servidor PHP:
	php -S localhost:8000

7) Acesse o endereco http://localhost:8000/ e escolha a data desejada para consulta clicando posteriormente no comando 'Enviar'.

Observações:

	* As instruções SQL's utilizadas nas consultas do sistema estão disponíveis no arquivo "ConsultasSQL_Etapa03_Postgres.sql".
	* O desenho do esquema de modelagem do banco de dados postgres está disponível através do arquivo "modelo_banco_postgres.png". 
	* O software utilizado para a modelagem do banco foi o "DBDesigner Fork" e o xml está disponível através do arquivo "bd_belvitur.xml".
	* Os testes para a construção do script foram feitos através do jupyter notebook (dispnível na instalação do Anaconda) e as construções e testes efetuados estão disponíveis no arquivo "laboratorio_testes.ipynb".
