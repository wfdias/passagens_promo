-- 1) 30 viagens mais longas (em km), com a duração da viagem e aeronave da viagem
select 	voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' )' as origem, 
		voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' )' as destino, 
		voos.dist_total_km, voos.total_minutos_viagem, voos.desc_modelo_aeronave, voos.desc_fabricante_aeronave 
from 	voos_encontrados voos 
inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto 
inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto
where data_referencia = to_date('15/10/2020', 'dd/mm/yyyy')
order by voos.dist_total_km desc fetch first 30 rows only;

-- 2) Estado com o maior número de aeroportos
select cod_uf, count(*) as "qtd" from aeroportos group by cod_uf order by count(*) desc fetch first 1 rows only;

-- 3) Todos os aeroportos de origem com destinos mais distantes e mais próximos (com voos disponíveis)

-- Voos com aeroporto destino mais distante
SELECT desc_aero_origem, desc_aero_mais_distante, distancia_total_km FROM (
	select 	ROW_NUMBER() OVER (PARTITION BY voos.cod_aero_origem ORDER BY voos.dist_total_km desc) as rownum, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ' as desc_aero_origem, 
			voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' as desc_aero_mais_distante, 
			max(voos.dist_total_km) as distancia_total_km 
	from 	voos_encontrados voos 
	inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto 
	inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto
	where data_referencia = to_date('15/10/2020', 'dd/mm/yyyy')
	group by voos.cod_aero_origem, 
	 		voos.dist_total_km, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ', 
	 		voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) '
) voos_mais_distantes
WHERE rownum = 1

-- Voos com aeroporto destino mais próximo 
SELECT desc_aero_origem, desc_aero_mais_proximo, distancia_total_km FROM (
	select 	ROW_NUMBER() OVER (PARTITION BY voos.cod_aero_origem ORDER BY voos.dist_total_km asc) as rownum, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ' as desc_aero_origem, 
			voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' as desc_aero_mais_proximo, 
			max(voos.dist_total_km) as distancia_total_km 
	from 	voos_encontrados voos 
	inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto 
	inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto 
	where data_referencia = to_date('15/10/2020', 'dd/mm/yyyy')
	group by voos.cod_aero_origem, 
	 		voos.dist_total_km, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ', 
	 		voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) '
) voos_mais_proximos
WHERE rownum = 1;


-- JOIN CONSULTAS
select 	dist.desc_aero_origem as origem, 
		dist.desc_aero_mais_distante, 
		dist.distancia_total_km as total_km_mais_dist, 
		prox.desc_aero_mais_proximo, 
		prox.distancia_total_km as total_km_mais_prox 
from 
(SELECT desc_aero_origem, desc_aero_mais_distante, distancia_total_km FROM (
	select 	ROW_NUMBER() OVER (PARTITION BY voos.cod_aero_origem ORDER BY voos.dist_total_km desc) as rownum, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ' as desc_aero_origem, 
			voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' as desc_aero_mais_distante, 
			max(voos.dist_total_km) as distancia_total_km 
	from 	voos_encontrados voos 
	inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto 
	inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto
	where data_referencia = to_date('17/10/2020', 'dd/mm/yyyy')
	group by voos.cod_aero_origem, 
	 		voos.dist_total_km, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ', 
	 		voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) '
) voos_mais_distantes
WHERE rownum = 1) dist, 
(SELECT desc_aero_origem, desc_aero_mais_proximo, distancia_total_km FROM (
	select 	ROW_NUMBER() OVER (PARTITION BY voos.cod_aero_origem ORDER BY voos.dist_total_km asc) as rownum, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ' as desc_aero_origem, 
			voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' as desc_aero_mais_proximo, 
			max(voos.dist_total_km) as distancia_total_km 
	from 	voos_encontrados voos 
	inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto 
	inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto 
	where data_referencia = to_date('17/10/2020', 'dd/mm/yyyy')
	group by voos.cod_aero_origem, 
	 		voos.dist_total_km, 
	 		voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ', 
	 		voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) '
) voos_mais_proximos
WHERE rownum = 1) prox 
where dist.desc_aero_origem = prox.desc_aero_origem 