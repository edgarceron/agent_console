#!/usr/bin/php -q
<?php
    /** See more on http://phpagi.sourceforge.net/phpagi2/docs/phpAGI/AGI.html */
    include "phpagi.php";//llama el phpagi
    $uniqueid = trim($argv[1]);
    $agi = new AGI();//instancia el AGI
    $agi->answer();// contesta la llamada
	
	$dbase='call_center';
	$servidor='localhost';
	$usuario='user';
    $pass='password';
    $link = mysql_connect($servidor,$usuario,$pass) or die("DB Connection Error");
    mysql_select_db($dbase) or die(mysqlerror()."Error: Cannot open database");
    
    $data = $agi->get_data('custom/digitecedula',12000,10);//Pide numero de cedula
    $cedula = trim($data['result']);
    $query = "INSERT INTO cedula_llamada (uniqueid, cedula) VALUES ('".$uniqueid."','".$cedula."');";
    $agi->verbose($query);
    $result = mysql_query($query) or die(mysql_error());
    $agi->verbose('Cedula guardada');
    mysql_free_result($result);
    mysql_close($link);
    $agi->exec("Queue", "6000,t,,"); //Llamo a la cola 

?>