document.onload = start();

function start() {
	
	if (jsonString.length === 0)
		return;
	
	// These two help parse the demon string that arrives from Python.
	// Leave them be!
	jsonString = jsonString.replace(/&quot;/g, '\"');
	jsonString = jsonString.replace(/&amp;/g, '\&');
	jsonString = jsonString.replace(/&#39;/g, '\'');
	
	// Store objects
	var objs = load_objects();
	
	for(var i = 0; i < objs.length; i++) {
		var currentObj = objs[i],
			isbn = currentObj.pk;
			
		var imgTag = document.querySelector('#img_' + isbn);
		imgTag.setAttribute('src', currentObj.fields.large_img);
		
		var titleTag = document.querySelector('#title_' + isbn);
		titleTag.innerText = currentObj.fields.title;
	}
}

function load_objects() {
	return JSON.parse(jsonString);
}