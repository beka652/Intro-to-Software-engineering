// Simple popup for add-to-cart feedback
function showPopup(message, isError = false) {
    let popup = document.getElementById('cart-popup-message');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'cart-popup-message';
        popup.style.position = 'fixed';
        popup.style.top = '30px';
        popup.style.left = '50%';
        popup.style.transform = 'translateX(-50%)';
        popup.style.zIndex = '9999';
        popup.style.padding = '16px 32px';
        popup.style.borderRadius = '8px';
        popup.style.fontWeight = 'bold';
        popup.style.fontSize = '1.1em';
        popup.style.boxShadow = '0 2px 12px rgba(0,0,0,0.15)';
        popup.style.transition = 'opacity 0.5s';
        document.body.appendChild(popup);
    }
    popup.textContent = message;
    popup.style.background = isError ? '#ff4d4f' : '#256d27';
    popup.style.color = '#fff';
    popup.style.opacity = '1';
    popup.style.display = 'block';
    setTimeout(() => {
        popup.style.opacity = '0';
        setTimeout(() => { popup.style.display = 'none'; }, 500);
    }, 1000);
}
