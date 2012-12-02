<!DOCTYPE html>
<html>
	<head>
		<title>Sudoku Generator</title>
		<link rel="stylesheet" href="style.css" />
		
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
		<a href="interface.html" class="button3" data-role="button" data-icon="home" data-theme="b" data-inline="true">Home</a>
		<br>
		<br>
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
			echo "<h1>". "Enjoy!"."</h1>"; 
			echo "<h2>". "Level: " . $level . "</h2>";
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