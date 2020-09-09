<?php header("Content-type: text/html; charset=utf-8"); ?>
<?php include_once('Aeroportos.php'); ?>
<?php $aeroportos = new Aeroportos(); ?>
<?php $datasDisponiveis = $aeroportos->listarDatasDisponiveis(); ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Passagens Promo</title>
</head>

<body>

	<h1><center>Passagens Promo</center></h1>

	<form name="PassagensPromo" action="processaLista.php" method="POST">
 		<select name="dataRef" id="dataRef">
 			<option selected="selected">Escolha uma data disponível:</option>
 			<?php foreach($datasDisponiveis as $data) { ?>
 				<option value="<?php echo $data->dataDisponivel ?>"><?php echo $data->dataDisponivel ?></option>
			<?php } ?>
 		</select>
		<input type="submit" name="btnEnvia" value="Enviar">
	</form>

 </body>

</html>

