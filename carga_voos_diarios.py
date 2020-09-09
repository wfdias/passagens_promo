# -*- coding: utf-8 -*-

import pandas as pd
import itertools
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
from pytz import timezone
from math import radians, sin, cos, asin, sqrt

"""
Definindo funções para uso geral
""" 
def obter_data_atual(string_timezone):
    """Função usada para obter a data atual, a partir de um fuso / timezone pré-definido. Ex.: 'America/Sao_Paulo'"""
    fuso_horario = timezone(string_timezone)
    data_hora_atual = datetime.now().astimezone(fuso_horario)
    return data_hora_atual.strftime("%Y-%m-%d")

def obter_data_futura(string_timezone, num_dias):
    """Função usada para somar o numero de dias passado como parâmetro à data atual considerando o fuso / timezone pré-definido."""
    fuso_horario = timezone(string_timezone)
    data_hora_atual = datetime.now().astimezone(fuso_horario)
    data_hora_futura = data_hora_atual + timedelta(days=num_dias)
    return data_hora_futura.strftime("%Y-%m-%d")

def obter_distancia_km_haversine(lon1, lat1, lon2, lat2):
    """Fórmula de Haversine. Retorna a distância em KM entre 2 pontos geográficos."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


## Importando informações de aeroportos ##

# Variáveis de conexão com API de daods
chave = 'pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc'
user = 'demo'
password = 'swnvlD'

# Variaveis de conxexão com o banco postgres
pgDatabase = 'bd_belvitur'
pgUser = 'user_belvitur'
pgPassword = 'swnvlD'

print("Importando / atualizando base de dados de aeroportos...", "(", datetime.now().time(), ")")

# Recuperando informações de aeroportos
url_aeroportos = "http://stub.2xt.com.br/air/airports/{key}".format(key=chave)
aeroportos = requests.get(url_aeroportos, auth=HTTPBasicAuth(user, password))

# Criando o dataframe de aeroportos
df_aeroportos = pd.read_json(aeroportos.content, orient='index', encoding='UTF-8')

# Renomeando colunas para o padrão do schema de banco de dados
df_aeroportos.columns = ['cod_aeroporto', 'desc_cidade', 'latitude', 'longitude', 'cod_uf']

# Lista completa de aeroportos (para uso na segunda parte do script, no caso de não se trabalhar com a lista pré-definida)
lista_aeroportos = df_aeroportos.cod_aeroporto.values.tolist()

# Conexao com o banco de dados postgres
url_conexao_banco = "postgresql+psycopg2://{db_user}:{db_pass}@localhost/{db}".format(db_user=pgUser, db_pass=pgPassword, db=pgDatabase)
engineDatabase = create_engine(url_conexao_banco)

# Recuperando informações da chave da tabela de aeroportos
df_chave_aero = pd.read_sql_query('SELECT cod_aeroporto FROM aeroportos', engineDatabase)

# Se não existir dados, insere todos os aeroportos. Caso contrario, insere aeroportos faltantes
if df_chave_aero.empty:
    df_aeroportos.to_sql('aeroportos', engineDatabase, if_exists='append', index=False)
else: 
    # Conventendo codigos de aeroporto encontrados na tabela de aeroportos para string
    cod_iata_db = '|'.join(df_chave_aero.cod_aeroporto.values.tolist()).replace("'", "")

    # Recuperando somente códigos inexistentes na base de dados
    df_aeroportos = df_aeroportos[~df_aeroportos["cod_aeroporto"].str.contains(cod_iata_db)]

    # Inserção dos dados de aeroportos ausentes
    if not df_aeroportos.empty:
        df_aeroportos.to_sql('aeroportos', engineDatabase, if_exists='append', index=False)

        
print("Base de dados de aeroportos importada e/ou atualizada com sucesso!", "(", datetime.now().time(), ")")

#######################################
## Definindo matriz de 20x20 de voos ##
#######################################

print("Importando / atualizando base de dados de voos encontrados...", "(", datetime.now().time(), ")")

# Definindo lista com 20 aeroportos (ocultar se quiser usar a lista completa)
lista_aeroportos = ['CNF', 'VIX', 'SDU', 'GRU', 'CWB', 'POA', 'FLN', 'AJU', 'NAT', 'THE', 'REC', 'JPA', 'SLZ', 'FOR', 'SSA', 'BPS', 'MAO', 'RBR', 'BEL', 'PMW']

# Definindo o numero de dias posteriores a data atual para execucao de pesquisa de voos disponiveis
numero_dias_posterior_data_atual = 40

# Efetuando a permutação dos 20 aeroportos adicionando o resultado em uma nova lista
lst_permutacoes_voos = []
for i in range(len(lista_aeroportos),len(lista_aeroportos)+1):
    lst_permutacoes_voos.append(list(itertools.permutations(lista_aeroportos,2)))
lst_permutacoes_voos = lst_permutacoes_voos[0]

# Definindo data de busca referente à 40 dias após a data atual
data_voo = obter_data_futura("America/Sao_Paulo", numero_dias_posterior_data_atual)

# Criação de lista de dicionários de voos
lst_dict_voos = []

for i in range(0, len(lst_permutacoes_voos)):
    param_voos = {
        'iata_orig': lst_permutacoes_voos[i][0],
        'iata_dest': lst_permutacoes_voos[i][1],
    }
    
    url_busca = "http://stub.2xt.com.br/air/search/{key}/{orig}/{dest}/{data}".format(
    key=chave, orig=param_voos['iata_orig'], dest=param_voos['iata_dest'], data=data_voo)
    
    ## Resultado dos voos encontrados com a combinação ##
    voos_encontrados = requests.get(url_busca, auth=HTTPBasicAuth(user, password))
    
    ## Dicionário com informações de longitude e latitude do par de aeroportos encontrado ##
    dict_sumario_voo = voos_encontrados.json()["summary"]
    
    ## Lista de opções de viagens com informações de data de saída e chegada, preço da tarifa e aeronaves ##
    list_opcoes_voo = voos_encontrados.json()["options"]
    
    ## Recuperando dados de busca do vôo procurado ##
    df_info_busca_efetuada = pd.DataFrame.from_dict(dict_sumario_voo, orient='index')
    # Invertendo linhas e colunas
    df_info_busca_efetuada = df_info_busca_efetuada.transpose()

    # Dataframe com informações do aeroporto de origem 
    df_info_origem = pd.DataFrame.from_dict(df_info_busca_efetuada['from'].dropna().tolist())
    # Dataframe com informações do aeroporto de destino
    df_info_destino = pd.DataFrame.from_dict(df_info_busca_efetuada['to'].dropna().tolist())
    # Dataframe de informações do usuário conectado
    df_info_user = pd.DataFrame.from_dict(df_info_busca_efetuada['user'].dropna().tolist())
    
    # Dataframe com os dados de viagens disponíveis para a data escolhida
    df_info_opcoes_voo = pd.DataFrame.from_records(list_opcoes_voo)
    # Verifica se existem voos disponíveis para continuar
    if not df_info_opcoes_voo.empty:
        # Dataframe de aeronaves das opções de voo
        raw_list_aeronaves = df_info_opcoes_voo['aircraft'].dropna().tolist()
        df_aeronaves = pd.DataFrame.from_dict(raw_list_aeronaves)
    
        # Dataframe de opções de voos concatenado com dataframe de aeronaves disponíveis
        df_info_voos = df_info_opcoes_voo.merge(df_aeronaves, left_index=True, right_index=True, how='inner')
        df_info_voos = df_info_voos[['departure_time', 'arrival_time', 'fare_price', 'model', 'manufacturer']]
        df_info_voos.columns = ['departure_time', 'arrival_time', 'fare_price', 'aircraft_model', 'aircraft_manufacturer']

        ## Calculos ##
        for j in range(0, len(df_info_opcoes_voo)):
            datetime_saida = datetime.strptime(df_info_voos.loc[j]['departure_time'], '%Y-%m-%dT%H:%M:%S')
            datetime_chegada = datetime.strptime(df_info_voos.loc[j]['arrival_time'], '%Y-%m-%dT%H:%M:%S')
            long_aero_1 = df_info_origem.loc[0]['lon']
            lat_aero_1 = df_info_origem.loc[0]['lat']
            long_aero_2 = df_info_destino.loc[0]['lon']
            lat_aero_2 = df_info_destino.loc[0]['lat']
            distancia_km = round(obter_distancia_km_haversine(long_aero_1, lat_aero_1, long_aero_2, lat_aero_2), 2)
            tempo_minutos = (datetime_chegada - datetime_saida) / timedelta(minutes=1)
            custo_tarifa_km = round(df_info_voos.loc[j]['fare_price'] / distancia_km, 2)
            vel_media_km_hora = round((float(distancia_km) / float(tempo_minutos / 60)), 2)
            
            # Definindo dados de registro da iteração em dicionário
            dict_dados_viagem = {
                'cod_aero_origem': df_info_origem.loc[0]['iata'],
                'cod_aero_destino': df_info_destino.loc[0]['iata'],
                'data_referencia': data_voo,
                'url_busca': url_busca, 
                'dist_total_km': distancia_km, 
                'vlr_melhor_tarifa_encontrada': df_info_voos.loc[j]['fare_price'], 
                'desc_modelo_aeronave': df_info_voos.loc[j]['aircraft_model'], 
                'desc_fabricante_aeronave': df_info_voos.loc[j]['aircraft_manufacturer'], 
                'dth_partida': datetime_saida,
                'dth_chegada': datetime_chegada, 
                'vlr_custo_por_km': custo_tarifa_km, 
                'vlr_velocidade_media': vel_media_km_hora, 
                'total_minutos_viagem': tempo_minutos 
            }

            # Adicionando registro de dados à lista de dicionários
            lst_dict_voos.append(dict_dados_viagem)

# Transformando lista de dicionários de voôs para dataframe
df_viagens = pd.DataFrame(lst_dict_voos)

# Contra-prova
# df_viagens.to_excel("planilha_voos.xlsx", sheet_name=data_voo, engine='xlsxwriter')

# Selecionando registros com a melhor tarifa (menor preço) e seus reespectivos modelos de aeronaves
df_viagens = df_viagens.iloc[df_viagens.groupby(['cod_aero_origem', 'cod_aero_destino', 'data_referencia'])['vlr_melhor_tarifa_encontrada'].idxmin()]

# Recuperando informações da chave da tabela de aeroportos
df_chave_voos = pd.read_sql_query('SELECT cod_aero_origem, cod_aero_destino, data_referencia FROM voos_encontrados', engineDatabase)

# Se não existir dados, insere todos os voos encontrados. Caso contrario, insere apenas os voos faltantes.
if df_chave_voos.empty:
    df_viagens.to_sql('voos_encontrados', engineDatabase, if_exists='append', index=False)
else: 
    # Normalizando tipos do dataframe das chaves de voos recuperados do banco de dados
    df_chave_voos.cod_aero_origem = df_chave_voos.cod_aero_origem.astype(str)
    df_chave_voos.cod_aero_destino = df_chave_voos.cod_aero_destino.astype(str)
    df_chave_voos.data_referencia = df_chave_voos.data_referencia.astype(str)

    # Normalizando tipos do dataframe das chaves de voos recuperados da API
    df_viagens.cod_aero_origem = df_viagens.cod_aero_origem.astype(str)
    df_viagens.cod_aero_destino = df_viagens.cod_aero_destino.astype(str)
    df_viagens.data_referencia = df_viagens.data_referencia.astype(str)

    # Copiando coluna de índice do dataframe da API para realização de join de faltantes
    df_viagens['copy_index'] = df_viagens.index

    # Realização de join de dataframes através das colunas chaves buscando os registros coincidentes
    df_voos_coincidentes = pd.merge(df_viagens, df_chave_voos, left_on=['cod_aero_origem', 'cod_aero_destino', 'data_referencia'], right_on=['cod_aero_origem', 'cod_aero_destino', 'data_referencia'], how='inner')

    # Obtendo apenas os registros faltantes através da coluna de índice criada temporariamente
    df_viagens = df_viagens[~df_viagens['copy_index'].isin(df_voos_coincidentes.copy_index.tolist())].drop(columns=['copy_index'])

    # Inserção dos dados de voos ausentes
    if not df_viagens.empty:
        # Importando registros para a base de dados
        df_viagens.to_sql('voos_encontrados', engineDatabase, if_exists='append', index=False)
        
print("Base de dados de voos encontrados importada e/ou atualizada com sucesso!", "(", datetime.now().time(), ")")