<?php

include_once('ConectaBanco.php');

class Aeroportos {

	private $codigoAeroporto;
	private $cidade;
	private $latititude;
	private $longitude;
	private $uf;

	private $aeroOrigem;
	private $aeroDestino;
	private $distanciaTotalKm;
	private $tempoTotalMinutos;
	private $modeloAeronave;
	private $fabricanteAeronave;

	private $unidadeFederativa; 
	private $quantidadeAeroportos;

	private $aeroportoOrigem;
	private $aeroportoMaisDistante;
	private $totalKMMaisDistante;
	private $aeroportoMaisProximo;
	private $totalKMMaisProximo;

	private $dataDisponivel;

	private $conexao;

	function __construct() {
		$this->conexao = ConectaBanco::conexao();
	}

	function __get($propriedade) {
		return $this->$propriedade;
	}

	function __set($propriedade, $valor) {
		$this->$propriedade = $valor;
	}

	public function retornar($id) {

		$rs = $this->conexao->query("SELECT * FROM aeroportos WHERE cod_aeroporto = '$id'");
		$row = $rs->fetch(PDO::FETCH_OBJ);

		if(empty($row)) {
			return null;
		}

		$this->codigoAeroporto = $row->cod_aeroporto;
		$this->cidade = $row->desc_cidade;
		$this->latitude = $row->latitude;
		$this->longitude = $row->longitude;
		$this->uf = $row->cod_uf;

	}

	public function listarTodos() {
		
		$rs = $this->conexao->query("SELECT * FROM aeroportos");
		
		$aeroportos = null;
		$i = 0;

		while($row = $rs->fetch(PDO::FETCH_OBJ)) {

			$aeroporto = new Aeroportos();

			$aeroporto->codigoAeroporto = $row->cod_aeroporto;
			$aeroporto->cidade = $row->desc_cidade;
			$aeroporto->latitude = $row->latitude;
			$aeroporto->longitude = $row->longitude;
			$aeroporto->uf = $row->cod_uf;

			$aeroportos[$i] = $aeroporto;
			$i++;

		}

		return $aeroportos;

	}

	public function listarViagensMaisLongas($data) {
		
		$selectViagens = "select voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' )' as origem, " .
		"voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' )' as destino, " .
		"voos.dist_total_km, voos.total_minutos_viagem, voos.desc_modelo_aeronave, voos.desc_fabricante_aeronave " .
		"from voos_encontrados voos " . 
		"inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto " .
		"inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto " .
		"where data_referencia = to_date('$data', 'dd/mm/yyyy') " .
		"order by voos.dist_total_km desc fetch first 30 rows only";

		$rs = $this->conexao->query($selectViagens);
		
		$viagens = null;
		$i = 0;

		while($row = $rs->fetch(PDO::FETCH_OBJ)) {

			$dadosViagemAeroporto = new Aeroportos();

			$dadosViagemAeroporto->aeroOrigem = $row->origem;
			$dadosViagemAeroporto->aeroDestino = $row->destino;
			$dadosViagemAeroporto->distanciaTotalKm = $row->dist_total_km;
			$dadosViagemAeroporto->tempoTotalMinutos = $row->total_minutos_viagem;
			$dadosViagemAeroporto->modeloAeronave = $row->desc_modelo_aeronave;
			$dadosViagemAeroporto->fabricanteAeronave = $row->desc_fabricante_aeronave;

			$viagens[$i] = $dadosViagemAeroporto;
			$i++;

		}

		return $viagens;
	}	

	public function listarUFMaisAeroportos() {
		
		$selectUFMaisAeroportos = "select cod_uf, count(*) as qtd from aeroportos group by cod_uf order by count(*) desc fetch first 1 rows only";

		$rs = $this->conexao->query($selectUFMaisAeroportos);
		
		$unidadesFederativas = null;
		$i = 0;

		while($row = $rs->fetch(PDO::FETCH_OBJ)) {

			$dadosUF = new Aeroportos();

			$dadosUF->unidadeFederativa = $row->cod_uf;
			$dadosUF->quantidadeAeroportos = $row->qtd;

			$unidadesFederativas[$i] = $dadosUF;
			$i++;

		}

		return $unidadesFederativas;

	}	

	public function listarAeroportosMaisLongesMaisProximos($data) {

		$selectAeroportos = "select	dist.desc_aero_origem as origem, dist.desc_aero_mais_distante, dist.distancia_total_km as total_km_mais_dist, " .
		"prox.desc_aero_mais_proximo, prox.distancia_total_km as total_km_mais_prox from " .
		"(SELECT desc_aero_origem, desc_aero_mais_distante, distancia_total_km FROM ( " .
		"select 	ROW_NUMBER() OVER (PARTITION BY voos.cod_aero_origem ORDER BY voos.dist_total_km desc) as rownum, " .
	 	"	voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ' as desc_aero_origem, " . 
		"	voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' as desc_aero_mais_distante, " .
		"	max(voos.dist_total_km) as distancia_total_km " . 
		"from 	voos_encontrados voos " .
		"inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto " . 
		"inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto " . 
		"where data_referencia = to_date('$data', 'dd/mm/yyyy') " .
		"group by voos.cod_aero_origem, " . 
	 	"	voos.dist_total_km, " . 
	 	"	voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ', " .
	 	"	voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' " .
		") voos_mais_distantes " .
		"WHERE rownum = 1) dist, " . 
		"(SELECT desc_aero_origem, desc_aero_mais_proximo, distancia_total_km FROM ( " . 
		"select 	ROW_NUMBER() OVER (PARTITION BY voos.cod_aero_origem ORDER BY voos.dist_total_km asc) as rownum, " . 
	 	"	voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ' as desc_aero_origem, " .
		"	voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' as desc_aero_mais_proximo, " . 
		"	max(voos.dist_total_km) as distancia_total_km " . 
		"from 	voos_encontrados voos " . 
		"inner join aeroportos aero1 on voos.cod_aero_origem = aero1.cod_aeroporto " . 
		"inner join aeroportos aero2 on voos.cod_aero_destino = aero2.cod_aeroporto " . 
		"where data_referencia = to_date('$data', 'dd/mm/yyyy') " . 
		"group by voos.cod_aero_origem, " . 
	 	"	voos.dist_total_km, " . 
	 	"	voos.cod_aero_origem || ' ( ' || aero1.desc_cidade || ' ) ', " . 
	 	"	voos.cod_aero_destino || ' ( ' || aero2.desc_cidade || ' ) ' " .
		") voos_mais_proximos " . 
		"WHERE rownum = 1) prox " . 
		"where dist.desc_aero_origem = prox.desc_aero_origem ";

		$rs = $this->conexao->query($selectAeroportos);
		
		$listaViagens = null;
		$i = 0;

		while($row = $rs->fetch(PDO::FETCH_OBJ)) {

			$dadosViagens = new Aeroportos();

			$dadosViagens->aeroportoOrigem = $row->origem;
			$dadosViagens->aeroportoMaisDistante = $row->desc_aero_mais_distante;
			$dadosViagens->totalKMMaisDistante = $row->total_km_mais_dist;
			$dadosViagens->aeroportoMaisProximo = $row->desc_aero_mais_proximo;
			$dadosViagens->totalKMMaisProximo = $row->total_km_mais_prox;

			$listaViagens[$i] = $dadosViagens;
			$i++;

		}

		return $listaViagens;

	}


	public function listarDatasDisponiveis() {
		
		$selectDatasDisponiveis = "select distinct (to_char(data_referencia, 'dd/mm/yyyy')) as data from voos_encontrados";

		$rs = $this->conexao->query($selectDatasDisponiveis);
		
		$datas = null;
		$i = 0;

		while($row = $rs->fetch(PDO::FETCH_OBJ)) {

			$dadosDataDisponivel = new Aeroportos();

			$dadosDataDisponivel->dataDisponivel = $row->data;
			
			$datas[$i] = $dadosDataDisponivel;
			$i++;

		}

		return $datas;

	}	

}

?>