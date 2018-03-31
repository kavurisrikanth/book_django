start();

function start() {
	var cartLink = document.querySelector('#cart_link');
	if(cartSize > 0)
		cartLink.innerText += ' (' + cartSize + ')';
}