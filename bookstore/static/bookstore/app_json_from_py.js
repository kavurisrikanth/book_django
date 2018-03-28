document.onload = start();

function start() {
	
	console.log('started');
	console.log(jsonString);
	
	// These two help parse the demon string that arrives from Python.
	// Leave them be!
	jsonString = jsonString.replace(/&quot;/g, '\"');
	jsonString = jsonString.replace(/&amp;/g, '\&');
	jsonString = jsonString.replace(/&#39;/g, '\'');
	
	console.log(jsonString);
	
	// Store objects
	var objs = load_objects();
	
	// Now we have a list of objects
	// Render html according to number of objects in list.
	if (objs.length > 1)
		render_index(objs);
	else
		if(objs.length === 1)
			render_book(objs);
}

/*
function load_objects() {
	var ans = new Array;
	for(var i = 0; i < jsonString.length; i++) {
		ans[i] = JSON.parse(jsonString[i]);
		console.log(ans[i]);
	}
	return ans;
}
*/

function load_objects() {
	return JSON.parse(jsonString);
}

function render_index(objs) {
	
	var booksBoxDiv = document.querySelector('.books_box');
	var i = 0;
	var currentRow = document.createElement('div');
	var currentObj;
	currentRow.setAttribute('class', 'col book_set');
	//currentRow.setAttribute('id', ' row_' + i);
	
	for (i = 0; i < objs.length; i++) {
		
		currentObj = objs[i];
		//console.log(currentObj);
		
		// Multiple of 3 and not zero.
		// Append current row and create new one.
		/*
		if (i % 3 === 0 && i !== 0) {
			booksBoxDiv.appendChild(currentRow);
			booksBoxDiv.innerHTML += '<hr>';
			currentRow = document.createElement('div');
			currentRow.setAttribute('class', 'col book_set');
			currentRow.setAttribute('id', ' row_' + i);
		} */
		
		// Just keep adding to the current row.
		var currentCol = document.createElement('div');
		currentCol.setAttribute('class', 'col one_book');
		currentCol.setAttribute('id', 'book_' + i);
		
		var bookImgTag = document.createElement('div');
		bookImgTag.setAttribute('class', 'col');
		var bookImg = document.createElement('img');
		bookImg.setAttribute('src', currentObj.fields.small_img);
		
		var bookTitle = currentObj.fields.title;
		bookImg.setAttribute('alt', "Cover of book titled '" + bookTitle + "'")
		bookImgTag.appendChild(bookImg);
		
		currentCol.appendChild(bookImgTag);
		
		var bookTitleTag = document.createElement('div');
		bookTitleTag.setAttribute('class', 'col');
		bookTitleTag.innerHTML = '<a href=/bookstore/viewbook?isbn=' + currentObj.pk + '>' + bookTitle + '</a>';
		bookTitleTag.innerHTML += '<br>';
		bookTitleTag.innerHTML += '<p>by ' + currentObj.fields.author + '</p>';
		
		currentCol.appendChild(bookTitleTag);
		currentRow.appendChild(currentCol);
	
	}
	
	//var lastRow = document.querySelector('#row_' + ((i / 3)) * 3);
	//if (lastRow === null)
	booksBoxDiv.appendChild(currentRow);
	
}

/*
This function renders the HTML for /bookstore/viewbook?isbn=<>, meaning for a SINGLE
book.
*/
function render_book(objs) {
	var onlyObj = objs[0];
	
	var title = document.querySelector('#book_title');
	title.innerText = onlyObj.fields.title;
	
	var img = document.querySelector('#book_image');
	img.setAttribute('src', onlyObj.fields.large_img);
	img.setAttribute('alt', img.getAttribute('alt') + '"' + onlyObj.fields.title + '"');
	
	var desc = document.querySelector('#description');
	desc.innerText = onlyObj.fields.description;
	return;
}