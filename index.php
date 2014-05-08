<?php 
date_default_timezone_set("UTC"); 
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>
			Focused Event Crawler
		</title>
        
		<link href="includes/style.css" rel="stylesheet" type="text/css" />
	    <script src="includes/jquery-1.11.0.js" type="text/javascript"></script>
	    <script src="includes/main.js" type="text/javascript"></script>
		
	</head>
	<body>
	
		<!-- Input -->
		<div class="mainSection">
		<h2 style="margin:0">Focused Event Crawler</h2><br />
		Give as much information as you know about natural disaster event URL's.<br /><br />
		<form id="inputForm" method="post" action="cgi-bin/src/FocusedCrawler.py">
		        <div id="siteUrls">
				<div id="siteDetailsContainer">
				</div>
			</div>
			<input type="button" id="addInput" name="add" value="+ URL Entry">
			<input type="submit" name="submit" value="Submit Entries" class="submitButton">
			<input type="reset" name="clear" value="Clear Fields" id="clearURLFields">
			
		</form> 
		
		<!-- Results -->
		</div>
		<div class="mainSection" style="margin-top:10px;">
		<input type="button" name="clear" value="Clear Results" id="clearResults" style="float:right">
		<h2 style="margin:0">Results</h2><br />
			<div id="resultHolder">
				<div id="topHere"></div>
				<div class="noSubmissionsLabel">There have been no current submissions.</div>
			</div>
		</div>
		<div class="treeComparisonBackground"></div>
		<div class="treeComparisonWindow">
		</div>
		
	<script type="text/javascript">
		$(document).ready(function(){
			$("#resultHolder").delegate(".comparisonButtonLink","click",function(){
				var pos = $(this).attr('id');
				var treeURL = $(this).parent().prev().text();
				var linkPosition;
				var eventTypeText = "z";
				var nameFieldText = "";
				var countryFieldText = "";
				var stateFieldText = "";
				var cityFieldText = "";
				var yearFieldText = "";
				var monthFieldText = "";
				var dayFieldText = "";
				
				$.get('/cgi-bin/src/readtrees.py', function(myContentFile) {
					var lines = myContentFile.split("\n");
					var fields = lines[pos-6].split("|");

					// Grab fields from textfile once we have found the matched URL					
					eventTypeText = fields[1];
					countryFieldText = fields[2];
					stateFieldText = fields[3];
					cityFieldText = fields[4];
					nameFieldText = fields[5];
					dayFieldText = fields[6];
					monthFieldText = fields[7];
					yearFieldText = fields[8];
					
					window.open('JSTest/index.php?eventType='+eventTypeText+'&eventName='+nameFieldText+
						'&countryField='+countryFieldText+'&stateField='+stateFieldText+'&cityField='+cityFieldText+
						'&monthField='+monthFieldText+'&yearField='+yearFieldText+'&dayField='+dayFieldText);
			
				}, 'text');
			});
		});
	</script>
	</body>
</html>




