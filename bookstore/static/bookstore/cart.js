document.onload = start();

function start() {
	
	if (jsonString.length === 0 || cartDataStr.length === 0)
		return;
	
	// These help parse the demon string that arrives from Python.
	// Leave them be!
	jsonString = jsonString.replace(/&quot;/g, '\"');
	jsonString = jsonString.replace(/&amp;/g, '\&');
	jsonString = jsonString.replace(/&#39;/g, '\'');
	cartDataStr = cartDataStr.replace(/&quot;/g, '\"');
	
	console.log('json string: ' + jsonString);
	console.log('cart data: ' + cartData);
	
	// Store objects
	var objs = load_objects();
	var cartData = load_cart_data();
	
	// Get the order info div. Everything is stored here.
	var orderInfoDiv = document.querySelector('#order_info_div');
	
	for(var i = 0; i < objs.length; i++) {
		var currentObj = objs[i],
			isbn = currentObj.pk;
			
		/*
			Each order info "card" will contain the following information:
			- The book's cover
			- The book's title
			- The quantity
		*/
		
		var bookCard = document.createElement('div');
		bookCard.setAttribute('class', 'col-12 need_flex');
		
		var imgPart = document.createElement('div');
		imgPart.setAttribute('class', 'col-4');
		
		var imgTag = document.createElement('img');
		imgTag.setAttribute('src', currentObj.fields.large_img);
		imgPart.appendChild(imgTag);
		
		var titlePricePart = document.createElement('div');
		titlePricePart.setAttribute('class', 'col-6');
		
		var titleTag = document.createElement('h3');
		titleTag.innerText = currentObj.fields.title;
		titlePricePart.appendChild(titleTag);
		
		var amtTag = document.createElement('div');
		console.log('isbn: ' + isbn + ' of type: ' + (typeof isbn));
		console.log('price: ' + currentObj.fields.price + ', amt: ' + cartData[isbn]);
		console.log('types: price - ' + (typeof currentObj.fields.price) + ', amt: ' + (typeof cartData[isbn]));
		for (var key in cartData) {
			console.log('comparing ' + key + ' and ' + isbn);
			console.log(key === isbn);
			console.log(key + ' -> ' + cartData[key]);
		}
		amtTag.innerHTML = '<h4>&#x20b9;' + (currentObj.fields.price * cartData[isbn]) + '</h4>';
		titlePricePart.appendChild(amtTag);
		
		bookCard.appendChild(imgPart);
		bookCard.appendChild(titlePricePart);
		
		orderInfoDiv.appendChild(bookCard);
		
		if(i != objs.length - 1) {
			var hor = document.createElement('hr');
			orderInfoDiv.appendChild(hor);
		}
	}
}

function load_objects() {
	return JSON.parse(jsonString);
}

function load_cart_data() {
	return JSON.parse(cartDataStr);
}