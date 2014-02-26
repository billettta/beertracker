var baMainSite = 'http://www.beeradvocate.com';	

function discoverBreweries()
{
	var baDirectory = 'http://www.beeradvocate.com/place/directory/';
	$('#breweryLinks').empty();
	traverseRegions(baDirectory, function() {
		alert('traversing regions complete');
	});
}

function breweryJSON()
{
	$('#breweryJSON').empty();
	
	$('div.brewery').each(function() {
		traverseBreweries($(this).text(), 0, function(result) {
			alert(result);
		});
	});
}

function styleJSON()
{
	var baStyles = 'http://www.beeradvocate.com/beer/style/';
	loadPage(baStyles, function (styleList) {
		$(styleList).find('#baContent a[href^="/beer/style"]').each(function() {
			var styleLink = baMainSite + $(this).attr('href');			
			loadPage(styleLink, function (stylePage) {
				var styleIDArray = styleLink.split("/");
				var styleID = styleIDArray[styleIDArray.length-2];
				var styleName = $(stylePage).find('div.titleBar').text();
				var fullDescriptionText = $(stylePage).find('#baContent table:first tr:first td:first').html();
				fullDescriptionText = fullDescriptionText.replace(/(\r\n|\n|\r)/gm,"");
				fullDescriptionText = fullDescriptionText.replace(/.*?<p>/gi,"");
				var descriptionArray = fullDescriptionText.split('Average alcohol by volume (abv) range: ');
				var descriptionText = descriptionArray[0].substring(0, descriptionArray[0].lastIndexOf('<br>'));
				descriptionText = descriptionText.substring(0,descriptionText.lastIndexOf('<br>'));
				descriptionText = descriptionText.replace(/</g,'&lt;');
				descriptionText = descriptionText.replace(/</g,'&gt;');
				var jsonData = '{ "model": "tracker.Style", "pk": ' + styleID + ', "fields": { "name": "' + styleName.trim() + '"';
				jsonData = jsonData + ', "description": "' + descriptionText.replace(/"/g,'\\"').trim() + '"';
	
				if (descriptionArray.length >= 2)
				{
					var abvText = descriptionArray[1].substring(0, descriptionArray[1].indexOf('%'));
					var abvArray = abvText.split('-');
					if (abvArray.length >= 1)
					{
						if (abvArray[0].trim() != "")
						{
							jsonData = jsonData + ', "lowabv": ' + abvArray[0].trim();
						}
					}
					if (abvArray.length >= 2)
					{
						jsonData = jsonData + ', "highabv": ' + abvArray[1].trim();
					}
				}

				jsonData = jsonData + ' } },<br>';

				$('#styleJSON').append(jsonData);
			});
		});
	});
}

function buildBeerSQL()
{
	var beersList = $('#beers').find('div');
	$(beersList).each(function() {
		var link = $(this).text();
		var beerID = $(this).attr('id');
		traverseBeerDescription(link, beerID, function(result) {
		});	
	});
}

function traverseBeerDescription (url, beerID, callback)
{
	loadPage(url, function (beerList) {
		var beerTable = $(beerList).find('#baContent table:first').find('table:first').find('tr:last');
		var noBreaksHtml = $(beerTable).html().replace(/(\r\n|\n|\r)/gm,"").replace(/</g,'&lt;').replace(/>/g,'&gt;');
		var descriptionTextArray = /Description:&lt;\/strong&gt;\s*&lt;br&gt;(.*)&lt;br&gt;\s*&lt;br&gt;\(Beer added by/gi.exec(noBreaksHtml);
		var descriptionText = descriptionTextArray[1].trim();
		if(!descriptionText.match(/.*No notes at this time.*/gi))
		{
			var sqlCommand = 'update tracker_beer set description = \'' + descriptionText.replace(/'/g,"''") + '\' where id = ' + beerID + ';';
			$('#beerSQL').append(sqlCommand + '<br/>');
		}
		else
		{	
			$('#beerJSON').append(beerID + ', ');
		}
		callback('');
	});
}


function beerJSON()
{
	var archiveLink = '?view=beers&show=arc';
	$('#breweryToSearch').find('div').each(function() {
		var link = $(this).text() + archiveLink;
		var breweryID = $(this).attr('id');
		traverseBeers(link, breweryID,'true', function(result) {
		});	
	});
}

function traverseBeers (url, breweryID, retired, callback)
{
	loadPage(url, function (beerList) {
		var beerTable = $(beerList).find('#baContent table:last');
		$(beerTable).find('tr:gt(1)').each(function() {
			var beerNameLink = $(this).children('td').eq(1).find('a');
			var beerName = $(beerNameLink).text().replace(/"/g,'\\"').trim();
			var beerIDArray = $(beerNameLink).attr('href').split("/");
			var beerID = beerIDArray[beerIDArray.length-2];
			var beerStyleLink = $(this).children('td').eq(2).find('a');
			var beerStyleIDArray = $(beerStyleLink).attr('href').split("/");
			var styleID = beerStyleIDArray[beerStyleIDArray.length-2];
			var abvText = $(this).children('td').eq(3).text().trim();

			var jsonData = '{ "model": "tracker.Beer", "pk": ' + beerID + ', "fields": { "brewery": ' + breweryID + ', "style": ' + styleID +
					', "name": "' + beerName.trim() + '", "retired": ' + retired;
			if (!isNaN(parseFloat(abvText)) && isFinite(abvText))
			{
				jsonData = jsonData + ', "abv": ' + abvText;
			}
			jsonData = jsonData + ' } },<br>';
			$('#beerJSON').append(jsonData);
		});
		callback('');
	});
}

function traverseBreweries (url, startIndex, callback)
{
	loadPage(url, function(breweryPage) {
		var elements = $(breweryPage).find('#baContent a[href^="/beer/profile"]');
		if(elements.length > 0)
		{
			$(elements).each(function() {
				var breweryName = $(this).text().replace(/['"]+/g, '').trim();
				var breweryLink = baMainSite + $(this).attr('href');
				var breweryIDArray = breweryLink.split("/");
				var breweryID = breweryIDArray[breweryIDArray.length-2];
				var addressFull = $(this).closest('tr').next('tr').children('td').eq(1);
				var city = $(addressFull).find('a:first');
				var state = $(city).nextUntil('br', 'a');
				var countryBR = $(city).nextAll('br:first');
				var country = $(countryBR).nextAll('a:first');
				var website = $(addressFull).find('a:contains("website")').attr('href');

				var jsonData = '{ "model": "tracker.Brewery", "pk": ' + breweryID + ', "fields": { "name": "' + breweryName + '", "city": "' + city.text().trim() + '"';
				if (typeof state != "undefined" && state.text() != "")
				{
					jsonData = jsonData + ', "state": "' + state.text().trim() + '"';
				}
				if (typeof country != "undefined" && country.text() != "")
				{
					jsonData = jsonData + ', "country": "' + country.text().trim() + '"';
				}
				if (typeof website != "undefined" && website != "undefined")
				{
					jsonData = jsonData + ', "website": "' + website.trim() + '"';
				}
				jsonData = jsonData + ', "description": "' + breweryLink.trim() + '" } },<br>';

				$('#breweryJSON').append(jsonData);
			});
			startIndex = startIndex + 20;
			var newURL = url.replace(/start=[0-9]*/g,'start='+startIndex);
			traverseBreweries(newURL, startIndex, function(){});
		}
		else
		{
			callback('')
		}
	
	});
}

function traverseRegions (url, callback)
{
	loadPage(url, function(directoryContent) {
		if(!$(directoryContent).find('#baContent li a:first').text().match(/Breweries.*/))
		{
			$(directoryContent).find('#baContent li a').each(function() {
				var regionLink = baMainSite + $(this).attr('href');
				if(!regionLink.match(/All count.*/)){
					traverseRegions(regionLink, function(){ });
				}
			});	
		}
		else
		{
			var breweriesLink = baMainSite + $(directoryContent).find('#baContent li a:first').attr('href');
			$('#breweryLinks').append('&lt;div class="brewery"&gt;' + breweriesLink + '&lt;/div&gt;<br>');

		}
	});
}

function loadPage(url,callback)
{
	$.ajax({
		url: url,
		type: 'GET',
		dataType: 'html',
		async: 'false',
		success: function(res) {
			callback(res.responseText);
		},
		error: function(xhr, status, error) {
		  var err = eval("(" + xhr.responseText + ")");
		  callback(err.Message);
		}
	 });
}
