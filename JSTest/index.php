<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>Spacetree - Tree Animation</title>

	<!-- CSS Files -->
	<script type="text/javascript">
		// variables defined here
		
		var eventType = <?php echo '"'.$_GET["eventType"].'"'; ?>;
		var eventName = <?php echo '"'.$_GET["eventName"].'"'; ?>;
		var countryField = <?php echo '"'.$_GET["countryField"].'"'; ?>;
		var stateField = <?php echo '"'.$_GET["stateField"].'"'; ?>;
		var cityField = <?php echo '"'.$_GET["cityField"].'"'; ?>;
		var monthField = <?php echo '"'.$_GET["monthField"].'"'; ?>;
		var yearField = <?php echo '"'.$_GET["yearField"].'"'; ?>;
		var dayField = <?php echo '"'.$_GET["dayField"].'"'; ?>;
		
	</script>
	<link type="text/css" href="base.css" rel="stylesheet" />
	<link type="text/css" href="Spacetree.css" rel="stylesheet" />


	<!-- JIT Library File -->

	<script language="javascript" type="text/javascript" src="jit-yc.js"></script>

	<!-- Example File -->
	<script language="javascript" type="text/javascript" src="TreeJS.js"></script>
</head>

<body onload="init();">
	<div id="container">
		<div id="id-list"></div>
		<div id="center-container">
			<div id="infovis"></div>    
		</div>
		<div id="right-container">
			<h4>Tree Orientation</h4>
			<table>
				<tr>
					<td>
						<label for="r-left">Left </label>
					</td>
					<td>
						<input type="radio" id="r-left" name="orientation" checked="checked" value="left" />
					</td>
				</tr>
				<tr>
					 <td>
						<label for="r-top">Top </label>
					 </td>
					 <td>
						<input type="radio" id="r-top" name="orientation" value="top" checked="checked" />
					 </td>
				</tr>
				<tr>
					 <td>
						<label for="r-bottom">Bottom </label>
					  </td>
					  <td>
						<input type="radio" id="r-bottom" name="orientation" value="bottom" />
					  </td>
				</tr>
				<tr>
					  <td>
						<label for="r-right">Right </label>
					  </td> 
					  <td> 
					   <input type="radio" id="r-right" name="orientation" value="right" />
					  </td>
				</tr>
			</table>

			<h4>Selection Mode</h4>
			<table>
				<tr>
					<td>
						<label for="s-normal">Normal </label>
					</td>
					<td>
						<input type="radio" id="s-normal" name="selection" checked="checked" value="normal" />
					</td>
				</tr>
			</table>
		</div>
		<div id="log"></div>
	</div>
</body>
</html>
