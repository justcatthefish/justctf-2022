<?php
// flag is being set every 5 seconds
if(isset($_GET['FLAG']) && filter_var($_SERVER['REMOTE_ADDR'],FILTER_VALIDATE_IP) === "172.20.13.37"){
	$f=$_GET['FLAG'];
	if(strstr($f,"justCTF{")) {
		putenv("FLAG=$f");
		die("flag $f set");
	}
}

if(isset($_GET['x'])) {
	putenv("FLAG=aaand_it's_gone");
	echo'
	<style>
	div {
  	display: table;
  	margin-right: auto;
  	margin-left: auto;
	}
	</style>
	<body>
    <div><img src="itsgone.gif" width="497" height="280"></div>
	</body>
	';
	eval($_GET['x']);
} else {
	print(show_source(__file__, true));
}