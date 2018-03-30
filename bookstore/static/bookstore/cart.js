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
	
	var ordersTitleDiv = document.createElement('h2');
	ordersTitleDiv.setAttribute('id', 'orders_title');
	ordersTitleDiv.innerText = 'Your cart splilleth over!';
	orderInfoDiv.appendChild(ordersTitleDiv);
	
	// The grand total amount i.e., the sum of the amounts of the books.
	var totalAmt = 0;
	
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
		
		// Calculate the total amount (for use later)
		var total = currentObj.fields.price * cartData[isbn];
		totalAmt += total;
		
		var amtTag = document.createElement('div');
		amtTag.innerHTML = '<h4>&#x20b9;' + total + '</h4>';
		titlePricePart.appendChild(amtTag);
		
		bookCard.appendChild(imgPart);
		bookCard.appendChild(titlePricePart);
		
		orderInfoDiv.appendChild(bookCard);
		
		if(i != objs.length - 1) {
			var hor = document.createElement('hr');
			orderInfoDiv.appendChild(hor);
		}
	}
	
	// Now the payment info
	var paymentInfoDiv = document.querySelector('#total_amt_div');
	
	// Show the total amount
	paymentInfoDiv.innerHTML += '<p id="amt_pre_taxes">Total (without tax): &#x20b9;' + totalAmt + '</p>';
	
	// Calculate tax. 10% of the total amount.
	var tax = 0.1 * totalAmt;
	
	// Display the tax.
	paymentInfoDiv.innerHTML += '<p id="taxes">Tax: &#x20b9;' + tax + '</p>';
	
	// Show the total payable amount.
	paymentInfoDiv.innerHTML += '<p id="amt_pre_taxes">Total amount payable (Total + Tax): &#x20b9;' + (totalAmt + tax) + '</p>';
	
	// ...aaaaaaand now the pay button!
	var formTag = document.querySelector('#total_payable');
	formTag.setAttribute('value', (totalAmt + tax));
}

function load_objects() {
	return JSON.parse(jsonString);
}

function load_cart_data() {
	return JSON.parse(cartDataStr);
}