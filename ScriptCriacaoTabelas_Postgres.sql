CREATE TABLE aeroportos (
  cod_aeroporto CHAR(3)   NOT NULL ,
  desc_cidade VARCHAR(80)   NOT NULL ,
  latitude DECIMAL(10,6)   NOT NULL ,
  longitude DECIMAL(10,6)   NOT NULL ,
  cod_uf CHAR(2)   NOT NULL   ,
PRIMARY KEY(cod_aeroporto));


CREATE TABLE voos_encontrados (
  cod_aero_origem CHAR(3)   NOT NULL ,
  cod_aero_destino CHAR(3)   NOT NULL ,
  data_referencia DATE   NOT NULL ,
  url_busca TEXT   NOT NULL ,
  dist_total_km DECIMAL(7,2)   NOT NULL ,
  vlr_melhor_tarifa_encontrada DECIMAL(7,2)   NOT NULL ,
  desc_modelo_aeronave VARCHAR(50)   NOT NULL ,
  desc_fabricante_aeronave VARCHAR(50)   NOT NULL ,
  dth_partida TIMESTAMP   NOT NULL ,
  dth_chegada TIMESTAMP   NOT NULL ,
  vlr_custo_por_km DECIMAL(5,2)    ,
  vlr_velocidade_media DECIMAL(7,2)    ,
  total_minutos_viagem DECIMAL(7,2)      ,
PRIMARY KEY(cod_aero_origem, cod_aero_destino, data_referencia)    ,
  FOREIGN KEY(cod_aero_origem)
    REFERENCES aeroportos(cod_aeroporto),
  FOREIGN KEY(cod_aero_destino)
    REFERENCES aeroportos(cod_aeroporto));


CREATE INDEX voos_encontrados_FKIndex1 ON voos_encontrados (cod_aero_origem);
CREATE INDEX voos_encontrados_FKIndex2 ON voos_encontrados (cod_aero_destino);


CREATE INDEX IFK_R_VOO_ENC_01 ON voos_encontrados (cod_aero_origem);
CREATE INDEX IFK_R_VOO_ENC_02 ON voos_encontrados (cod_aero_destino);
