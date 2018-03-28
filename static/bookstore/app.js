document.onload = start()

function start() {
	console.log('About to load')
	$.getJSON(jsonFile, function(myObj) {
		console.log('Done reading JSON data.');
		var booksBoxDiv = document.querySelector('.books_box');
		var i = 0;
		var currentRow = document.createElement('div');
		currentRow.setAttribute('class', 'row justify-content-center book_row');
		currentRow.setAttribute('id', ' row_' + i);
		
		for(i = 0; i < myObj.items.length; i++) {
			// Multiple of 3 and not zero.
			// Append current row and create new one.
			if (i % 3 === 0 && i !== 0) {
				booksBoxDiv.appendChild(currentRow);
				booksBoxDiv.innerHTML += '<hr>';
				currentRow = document.createElement('div');
				currentRow.setAttribute('class', 'row justify-content-center book_row');
				currentRow.setAttribute('id', ' row_' + i);
			}
			
			// Just keep adding to the current row.
			var currentCol = document.createElement('div');
			currentCol.setAttribute('class', 'col-md-3 one_book');
			currentCol.setAttribute('id', 'book_' + i);
			
			var bookImgTag = document.createElement('div');
			bookImgTag.setAttribute('class', 'col-md-6');
			var bookImg = document.createElement('img');
			bookImg.setAttribute('src', myObj.items[i].volumeInfo.imageLinks.thumbnail);
			
			var bookTitle = myObj.items[i].volumeInfo.title;
			bookImg.setAttribute('alt', "Cover of book titled '" + bookTitle + "'")
			bookImgTag.appendChild(bookImg);
			
			currentCol.appendChild(bookImgTag);
			
			var bookTitleTag = document.createElement('div');
			bookTitleTag.setAttribute('class', 'col-md-6');
			bookTitleTag.innerHTML = '<a href=#>' + bookTitle + '</a>';
			bookTitleTag.innerHTML += '<br>';
			bookTitleTag.innerHTML += '<p>by ' + myObj.items[i].volumeInfo.authors[0] + '</p>';
			
			currentCol.appendChild(bookTitleTag);
			currentRow.appendChild(currentCol);
		
		}
		
		var lastRow = document.querySelector('#row_' + ((i / 3)) * 3);
		if (lastRow === null)
			booksBoxDiv.appendChild(currentRow);
	});
}