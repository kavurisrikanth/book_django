document.onload = start();

function start() {
	
	orderDetails = orderDetails.replace(/&quot;/g, '\"');
	orderDetails = orderDetails.replace(/&amp;/g, '\&');
	orderDetails = orderDetails.replace(/&#39;/g, '\'');
	bookList = bookList.replace(/&quot;/g, '\"');
	
	console.log('order data string: ' + orderDetails);
	console.log('book list string: ' + bookList);
	
	var orderObjs = load_objects(),
		bookObjs = load_books_data(),
		mainHeading = document.querySelector('.main_heading');
	mainHeading.innerHTML += '<h2>Order #' + orderObjs[0].pk + ' placed on ' + orderObjs[0].fields.placed_date + '</h2>';
	mainHeading.innerHTML += '<h3>Total amount paid: &#x20b9;' + orderObjs[0].fields.total_amount + '</h3>';
		
	for (var i = 0; i < bookObjs.length; i++) {
		var currentBook = bookObjs[i];
		
		var currentRow = document.createElement('div'),
			imgDiv = document.createElement('div'),
			dataDiv = document.createElement('div');
		
		imgDiv.innerHTML = '<img src="' + currentBook.fields.large_img + '" alt="Cover of book titled \"' + currentBook.fields.title + '\"">'
		imgDiv.setAttribute('class', 'col-4');
		currentRow.appendChild(imgDiv);
		
		dataDiv.setAttribute('class', 'col-8 book_data');
		dataDiv.innerHTML += '<h3>' + currentBook.fields.title + '</h3>';
		dataDiv.innerHTML += '<p>by ' + currentBook.fields.author + '</p>';
		currentRow.appendChild(dataDiv);
		
		mainHeading.appendChild(currentRow);
	}
}

function load_objects() {
	return JSON.parse(orderDetails);
}

function load_books_data() {
	return JSON.parse(bookList);
}