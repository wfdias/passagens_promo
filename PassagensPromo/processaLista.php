<?php include_once('Aeroportos.php'); ?>
<?php $aeroportos = new Aeroportos(); ?>
<?php $dataSelecionadaPost = $_POST['dataRef']; ?>
<?php $registrosViagens = $aeroportos->listarViagensMaisLongas($dataSelecionadaPost); ?>
<?php $registroUFMaisAeroportos = $aeroportos->listarUFMaisAeroportos(); ?>
<?php $registrosAeroportosDistancia = $aeroportos->listarAeroportosMaisLongesMaisProximos($dataSelecionadaPost); ?>



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aeroportos</title>
</head>

<body>
	<h1><center>Passagens Promo</center></h1>
	<br>

	<h2>Top 30 viagens mais longas (em km)</h2>

	<table border="1px">
		<tr>
			<th>Origem</th>
			<th>Destino</th>
			<th>Distância total (km)</th>
			<th>Tempo total (min)</th>
			<th>Aeronave</th>
			<th>Fabricante</th>
		</tr>
		<?php foreach ($registrosViagens as $v) { ?>
	     <tr>
	        <td><?php echo $v->aeroOrigem ?></td>
	        <td><?php echo $v->aeroDestino ?></td>
	        <td><?php echo $v->distanciaTotalKm ?></td>
	        <td><?php echo $v->tempoTotalMinutos ?></td>
	        <td><?php echo $v->modeloAeronave ?></td>
	        <td><?php echo $v->fabricanteAeronave ?></td>
	    </tr>
		<?php } ?>
	</table>

	<h2>Estado brasileiro com o maior número de aeroportos</h2>

	<table border="1px">
		<tr>
			<th>Estado</th>
			<th>Quantidade</th>
		</tr>
		<?php foreach ($registroUFMaisAeroportos as $a) { ?>
	     <tr>
	        <td><?php echo $a->unidadeFederativa ?></td>
	        <td><?php echo $a->quantidadeAeroportos ?></td>
	    </tr>
		<?php } ?>
	</table>

	<h2>Lista de aeroportos mais distantes e mais próximos</h2>

	<table border="1px">
		<tr>
			<th>Origem</th>
			<th>Aeroporto mais distante</th>
			<th>KM Total</th>
			<th>Aeroporto mais proximo</th>
			<th>KM Total</th>
		</tr>
		<?php foreach ($registrosAeroportosDistancia as $d) { ?>
	     <tr>
	        <td><?php echo $d->aeroportoOrigem ?></td>
	        <td><?php echo $d->aeroportoMaisDistante ?></td>
	        <td><?php echo $d->totalKMMaisDistante ?></td>
	        <td><?php echo $d->aeroportoMaisProximo ?></td>
	        <td><?php echo $d->totalKMMaisProximo ?></td>
	    </tr>
		<?php } ?>
	</table>

</body>

</html>
