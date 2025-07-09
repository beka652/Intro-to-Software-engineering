// Cart logic for floating cart icon and modal
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.reduce((sum, item) => sum + item.qty, 0);
}

function showCartIcon() {
    document.getElementById('floating-cart').style.display = 'flex';
    updateCartCount();
}

function hideCartIcon() {
    document.getElementById('floating-cart').style.display = 'none';
}

function renderCartItems() {
    const cartItemsDiv = document.getElementById('cart-items');
    cartItemsDiv.innerHTML = '';
    let total = 0;
    if (cart.length === 0) {
        cartItemsDiv.innerHTML = '<p>Your cart is empty.</p>';
    } else {
        cart.forEach((item, idx) => {
            total += item.price * item.qty;
            cartItemsDiv.innerHTML += `
                <div class="cart-item">
                    <span class="cart-item-name">${item.name}</span>
                    <span class="cart-item-qty">x${item.qty}</span>
                    <span>${item.price.toFixed(2)}$</span>
                    <span class="remove-cart-item" data-idx="${idx}">&times;</span>
                </div>
            `;
        });
    }
    document.getElementById('cart-total').textContent = 'Total: $' + total.toFixed(2);
}

function showCartModal() {
    renderCartItems();
    document.getElementById('cart-modal').style.display = 'block';
}

function hideCartModal() {
    document.getElementById('cart-modal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    // Add floating cart icon and modal to body if not present
    if (!document.getElementById('floating-cart')) {
        const cartIconDiv = document.createElement('div');
        cartIconDiv.id = 'floating-cart';
        cartIconDiv.style.display = 'none';
        cartIconDiv.innerHTML = `<img src="/static/img/logo-icon.png" alt="Cart" id="cart-icon" /><span id="cart-count">0</span>`;
        document.body.appendChild(cartIconDiv);
    }
    if (!document.getElementById('cart-modal')) {
        const cartModalDiv = document.createElement('div');
        cartModalDiv.id = 'cart-modal';
        cartModalDiv.innerHTML = `
            <div class="cart-modal-content">
                <span class="close-cart">&times;</span>
                <h2>Your Cart</h2>
                <div id="cart-items"></div>
                <div id="cart-total"></div>
            </div>
        `;
        document.body.appendChild(cartModalDiv);
    }
    // Show cart icon if cart has items
    if (cart.length > 0) showCartIcon();
    updateCartCount();

    // Cart icon click
    document.getElementById('floating-cart').onclick = showCartModal;
    // Close modal
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('close-cart')) hideCartModal();
        if (e.target.classList.contains('remove-cart-item')) {
            const idx = parseInt(e.target.getAttribute('data-idx'));
            cart.splice(idx, 1);
            localStorage.setItem('cart', JSON.stringify(cart));
            renderCartItems();
            updateCartCount();
            if (cart.length === 0) hideCartModal();
        }
    });
    // Hide modal on outside click
    window.onclick = function(event) {
        if (event.target == document.getElementById('cart-modal')) {
            hideCartModal();
        }
    };
});

// To be called by Add to Cart buttons
window.addToCart = function(product) {
    // product: {name, price, qty}
    let found = false;
    for (let item of cart) {
        if (item.name === product.name) {
            item.qty += product.qty;
            found = true;
            break;
        }
    }
    if (!found) cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    showCartIcon();
    updateCartCount();
};
