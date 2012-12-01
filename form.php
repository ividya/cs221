<!DOCTYPE html>
<html>
	<head>
		<title>Sudoku Generator</title>
		<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
		<link href="style.css" rel="stylesheet" type="text/css">
		<link rel="stylesheet" href="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
			<script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
			<script src="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>
		
		<style type="text/css" media="screen">
		table{
		border-collapse:collapse;
		border:1px solid black;
		}

		table td{
		border:1px solid black;
		padding: 25px;
		}
		
		.move_right { 
		padding: 30px;
		}
		</style>
	</head>

	<body class="move_right">
		<a href="interface.html" data-role="button" data-icon="home" data-theme="b" data-inline="true">Home</a>
		
		<?php
			$level = "very easy";
			if($_GET['radio-choice'] == "choice-2") {
				$level = "easy";
			}
			if($_GET['radio-choice'] == "choice-3") {
				$level = "medium";
			}
			if($_GET['radio-choice'] == "choice-4") {
				$level = "hard";
			}
			if($_GET['radio-choice'] == "choice-5") {
				$level = "fiendish";
			}
			echo "<h2>". "Enjoy!"."</h2>"; 
			echo "<h4>". "Level: " . $level . "</h4>";
			$command = '/usr/local/bin/python generate.py' . ' ' . $level;
			$temp = exec($command, $output);
			$filename = "output.txt";
			$handle = fopen($filename, "r");
			echo "<table>";
			if ($handle) {
			    while (($buffer = fgets($handle, 4096)) !== false) {
			        echo $buffer;
			    }
			    if (!feof($handle)) {
			        echo "Error: unexpected fgets() fail\n";
			    }
			    fclose($handle);
			}
			echo "</table>";
			
			echo "<h4>". "Our Solution" . "</h4>";
			$filename = "solution.txt";
			$handle = fopen($filename, "r");
			echo "<table>";
			if ($handle) {
			    while (($buffer = fgets($handle, 4096)) !== false) {
			        echo $buffer;
			    }
			    if (!feof($handle)) {
			        echo "Error: unexpected fgets() fail\n";
			    }
			    fclose($handle);
			}
			echo "</table>";
		?>
	</body>
</html>