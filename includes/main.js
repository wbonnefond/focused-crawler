$(document).ready(function(){
	
	var descriptionFieldLabels = 'Event Type:<br />'+
		'City/State/Country:<br />'+
		'Day/Month/Year:<br />'+
		'Crawler Type:<br />'+
		'Search Page Limit:';
	var eventTypeFields = '<select name="eventTypeField" id="eventTypeField">'+
		'<option value="0"> </option>'+
		'<option value="avalanche">Avalanche</option>'+
		'<option value="blizzard">Blizzard</option>'+
		'<option value="cyclone">Cyclone</option>'+
		'<option value="drought">Drought</option>'+
		'<option value="earthquake">Earthquake</option>'+
		'<option value="forestfire">Forest Fire</option>'+
		'<option value="flood">Flood</option>'+
		'<option value="hailstorm">Hailstorm</option>'+
		'<option value="heatwave">Heat Wave</option>'+
		'<option value="hurricane">Hurricane</option>'+
		'<option value="landslide">Landslide</option>'+
		'<option value="tsunami">Tsunami</option>'+
		'<option value="tornado">Tornado</option>'+
		'<option value="tropicalstorm">Tropical Storm</option>'+
		'<option value="typhoon">Typhoon</option>'+
		'<option value="volcaniceruption">Volcanic Eruption</option>'+
		'<option value="wildfire">Wildfire</option>'+
		'</select><br />';
	var cityField = '<input type="text" name="cityField" value="" id="cityField"> ';
	var stateField = '<input type="text" name="stateField" value="" id="stateField"> ';
	var countryField = '<input type="text" name="countryField" value="" id="countryField"><br />';

	var today = new Date()
	var dayField = '<select id="dayField">';
		dayField += '<option value="0"> </option>';
	for (var i=1;i<=31;i++)
	{
		dayField += '<option value="'+i+'">'+i+'</option>';
	}
	dayField +='</select>';
	var monthField = '<select id="monthField">'+
		'<option value="0"> </option>'+
		'<option value="1">January</option>'+
		'<option value="2">February</option>'+
		'<option value="3">March</option>'+
		'<option value="4">April</option>'+
		'<option value="5">May</option>'+
		'<option value="6">June</option>'+
		'<option value="7">July</option>'+
		'<option value="8">August</option>'+
		'<option value="9">September</option>'+
		'<option value="10">October</option>'+
		'<option value="11">November</option>'+
		'<option value="12">December</option>'+
		'</select>';
	var yearField = '<select id="yearField">';
		yearField += '<option value="0"> </option>';
	for (var i=today.getFullYear();i>=1900;i--)
	{
		yearField += '<option value="'+i+'">'+i+'</option>';
	}
	yearField +='</select><br />';
	
	var pageLimitField = '<input type="text" name="pageLimitField" id="pageLimitField" value="10">';
	
	var crawlerFields = '<select name="crawlerField" id="crawlerField">'+
		'<option value="1">Event FC</option>'+
		'<option value="0">FC</option>'+
		'</select><br />'
	
    /* Handle adding Site URL fields */
	$('#siteDetailsContainer').append('<div id="siteDetailsLeft">'+
		descriptionFieldLabels+
		'</div>'+'<div id="siteDetailsRight">'+
		eventTypeFields+cityField+stateField+countryField+dayField+monthField+yearField+crawlerFields+pageLimitField+
		'</div>');
    $('#siteUrls').append('<br /><div style="clear:both"></div><span style="color:#7100A6;">Seed URL:</span> <input type="text" name="addedURL" class="addedURL">');
    $('#addInput').click( function(){
        $('#siteUrls').append('<br /><span style="color:#7100A6;">Seed URL:</span> <input type="text" name="addedURL" class="addedURL">');
    });
	
	$('#eventTypeField').change(function() {
		if ($(this).val() === 'hurricane' || $(this).val() === 'typhoon') {
			var n = $(this).val();
			n = n.charAt(0).toUpperCase() + n.slice(1);  // Capitalize first letter
			$(".nameLabel").html(n+" Name:");
			if(!$("#siteDetailsRight #nameField").length){
				$("#siteDetailsLeft br" ).first().after('<div class="nameLabel">'+n+' Name:</div>');
				$("#siteDetailsRight br" ).first().after('<div class="nameValue"><input type="text" name="nameField" value="" id="nameField" onfocus="this.value=\'\'"></div>');
			}
		}
		else if($("#siteDetailsRight #nameField").length) {
			$(".nameLabel").remove();
			$(".nameValue").remove();
		}
	});
	
	/* Handle input fields green shading */
	$('#siteUrls').delegate(".addedURL","input",function(){
		if($(this).val() != ''){
			$(this).css("background-color","#E0FFE7");
		}
		else {
			$(this).css("background-color","#FFFFFF");
		}
	});
	
	/* Handle tree comparison styling */
	$h = ($(window).height()-$(".treeComparisonWindow").height())/2;
	$w = ($(window).width()-$(".treeComparisonWindow").width())/2;
	$(".treeComparisonWindow").css("top",$h);
	$(".treeComparisonWindow").css("left",$w);
	
	
	
    /* Handle AJAX fields posting */
	var s = 1;
	var origSpinner = "";
	var submissionLabel = "";
	var fieldsFilled = true;
	$(".submitButton").click( function(){
		//$('#clearResults').attr("disabled",true);
	});
    $("#inputForm").on("submit", function(event) {
		event.preventDefault();
		
		var inputEventDetails = "";
		var inputURLValue = "";
		var nameField = "";
		if(typeof $("#nameField").val() !== "undefined"){
			nameField = $("#nameField").val();
		}
		
		// Format URLs for url text file
		inputURLValue = "";
		$(".addedURL").each(function(index) {
			inputURLValue += $(this).val()+"\n";
		});
		inputURLValue += "";
			
		// Format event details for details text file
		inputEventDetails = "";

		if($("#eventTypeField option:selected").text() != "0"){
			inputEventDetails += $("#eventTypeField option:selected").text()+"\r\n";
		}
		else{
			inputEventDetails += "\r\n";
		}
		if($("#countryField").val() != ""){
			inputEventDetails += $("#countryField").val()+"\r\n";
		}
		else{
			inputEventDetails += "\r\n";
		}
		if($("#stateField").val() != ""){
			inputEventDetails += $("#stateField").val()+"\r\n";
		}
		else{
			inputEventDetails += "\r\n";
		}
		if($("#cityField").val() != ""){
			inputEventDetails += $("#cityField").val()+"\r\n";
		}
		else{
			inputEventDetails += "\r\n";
		}
		inputEventDetails += nameField + "\r\n";
		if($("#dayField option:selected").val() != "0"){
			inputEventDetails += $("#dayField option:selected").val()+"\r\n";
		}
		else{
			inputEventDetails += "0\r\n";
		}
		if($("#monthField option:selected").val() != "0"){
			inputEventDetails += $("#monthField option:selected").val()+"\r\n";
		}
		else{
			inputEventDetails += "0\r\n";
		}
		if($("#yearField option:selected").val() != "0"){
			inputEventDetails += $("#yearField option:selected").val();
		}
		else{
			inputEventDetails += "0\r\n";
		}
		/*
		inputEventDetails += $("#eventTypeField option:selected").text()+"\r\n"+
			$("#countryField").val()+"\r\n"+
			$("#stateField").val()+"\r\n"+
			$("#cityField").val()+"\r\n"+
			nameField +"\r\n"+
			$("#dayField option:selected").text()+"\r\n"+
			$("#monthField option:selected").val()+"\r\n"+
			$("#yearField option:selected").text();
		*/
		inputEventDetails += "";
		
		// Check if at least one of the event details was provided
		if(/^\s*$/.test(inputURLValue)){
			alert("You must provide at least one site URL.");
			fieldsFilled = false;
		}
		else if(/^\s*$/.test(inputEventDetails)){
			alert("You must provide at least one event detail.\n(event type, city, state, country, day, month, or year)");
			fieldsFilled = false;
		}
		if(fieldsFilled){
			$('#clearResults').attr("disabled",true);
			$('.noSubmissionsLabel').html('');
			origSpinner = "spinner"+s;
			submissionLabel = '<div class="submission"><span class="submissionLabel">Submission '+s+'</span>';
			$('#topHere').after(submissionLabel+'<div class="spinner '+origSpinner+'" style=""></div>');
			
			var pageLimitField = "10";
			var crawlerField = "0";
			
			pageLimitField = $("#pageLimitField").val();
			crawlerField = $("#crawlerField").val();
			
			// type of crawler		"url list separated by spaces"		page limit		"event details separated by newlines"
			s++;
			
			// TODO: add spinner field in passing (it is last line in output), get real program working
			$.ajax({
				type: "POST",
				//used to have id: s-1
				data: {crawlField: crawlerField, urlInput: inputURLValue, pageLimit: pageLimitField, detailInput: inputEventDetails, id: s-1},
				url: "../cgi-bin/src/FocusedCrawler.py",
				success: function (out) {
					var html_output = "";
					/*
                    			var temp = msg.substr(msg.indexOf('|')+1);
					var id = temp.substr(0, temp.indexOf('|'));
					*/
					out = "Content-Type: text/plain\n\n"+out;
                    //out += "1\n";
					id = out.substr(out.lastIndexOf("\n")-1, out.length);
					$('.spinner'+id).toggle();

					// Begin grabbing specific URL output fields from array generated from python output
					var output = out.split("\n");

					// Grab URL output, removing beginning and ending junk
					var added_urls = output[3].substring(2, output[3].length-2);
					var individual_urls = added_urls.split("', '");
					var used_urls = "";
					var all_urls_good = true;
					
					var url_arr = individual_urls[0].split(" ");
					for(var i=0; i<individual_urls.length; i++){
						if(individual_urls[i] != ""){
													
							/* url_exists(individual_urls[i], function(status){
								alert(status);
							}); THIS DOESNT WORK YET (catching 404)*/
							if(all_urls_good){
								used_urls += individual_urls[i]+"<br />";
							}
						}
					}

					// Now with good urls, proceed
					if(all_urls_good){
						var relevant_urls = "";

						// Begin reading after the gap of repeated URL's, which is size of individual_urls
						// Since each URL has 2 scores ahead of it, take just the URL by taking the 3rd delimited item
						for(var i = 6; i < output.length - 4; i++){
							var raw_url = output[i].split("|")[2];
							var trunc_url = (raw_url.length > 93) ? raw_url.substring(0,90)+'...' : raw_url;
							relevant_urls += '<a href="'+raw_url+'" id="'+i+'" target="_blank">'+trunc_url+'</a>';
							if(crawlerField == 1){
								relevant_urls += '<div class="treeComparisonButtonLink"><input type="button" id = "'+i+'" class="comparisonButtonLink" style="float:right" value="View Tree"></div><br />';
							}
							else {
								relevant_urls += '<br />';
							}
						}
		
						// Grab score from last 2 elements in output
						relevant_articles = output[output.length-4];
						var total_articles = output[output.length-3];
		
						html_output += '<br />Entered URLs:<br /><div style="margin-left:15px;">'+used_urls+'</div>';
		
						if(relevant_urls != "" && relevant_articles > 0){
							html_output += 'Found unique relevant URLs:<br /><div style="margin-left:15px;">'+relevant_urls+'</div>';
						}
						else {
							html_output += 'No further unique relevant URLs found.<br />';
						}
						html_output += "<span style=\"text-size:1.0em;\">Accepted <span style=\"color:#0B7700;\"><strong>"+relevant_articles+"</strong></span> relevant web pages out of <span style=\"color:#680A0C;\"><strong>"+total_articles+"</strong></span>.</span></div>";
					}
					else {
						html_output += used_urls+"</div>";
					}
					//$('.spinner'+id).after("<pre>"+out+"</pre><br />");
					$('.spinner'+id).after(html_output);
				}
			});
		}
		else {
			fieldsFilled = true;
		}
	
    });
	
	/* Execute when all ajax is complete. */
	$(document).ajaxStop(function () {
		$('#clearResults').removeAttr("disabled");
	});
	
	/* Handle clearing URL text fields */
	$('#clearURLFields').click(function(){
		$(".addedURL").each(function(){
			$(this).css("background-color","#FFFFFF");
		});
	});
	
	/* Handle clearing URL results */
	$('#clearResults').click(function(){
		s = 1;
		$('#resultHolder').empty();
		$('#resultHolder').append('<div id="topHere"></div>');
		$('#resultHolder').append('<div class="noSubmissionsLabel">There have been no current submissions.</div>');
	});
	
});



function url_exists(url, cb) {
	jQuery.ajax({
		url: url, dataType: 'text', type: 'GET', complete: function(xhr){
			if(typeof cb === 'function')
				cb.apply(this, [xhr.status]);
		}
	});
}


