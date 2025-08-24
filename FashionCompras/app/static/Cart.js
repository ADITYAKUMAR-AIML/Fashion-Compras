document.addEventListener('DOMContentLoaded', () => {
  const cartItems = document.querySelectorAll('.cart-item');
  const summarySubtotalEl = document.querySelector('.cart-summary .Subtotal'); // summary area
  const summaryTotalEl = document.querySelector('.cart-summary .total span:last-child'); // total area
  const shipping = 5.00; // your fixed shipping

  // Sum only the item subtotals (not the summary .Subtotal)
  function updateCartSummary() {
    let subtotal = 0;
    // Select only .Subtotal elements that are inside .cart-item
    document.querySelectorAll('.cart-item .Subtotal').forEach(sub => {
      subtotal += parseFloat(sub.textContent.replace(/[^0-9.]/g, '') || 0);
    });
    if (summarySubtotalEl) summarySubtotalEl.textContent = subtotal.toFixed(2);
    if (summaryTotalEl) summaryTotalEl.textContent = `$${(subtotal + shipping).toFixed(2)}`;
  }

  cartItems.forEach(item => {
    // IMPORTANT: always scope with item.querySelector so we get THIS item's elements
    const priceEl = item.querySelector('.Price');
    const qtyEl = item.querySelector('.qty');
    const Minus = item.querySelector('.Minus');
    const Plus = item.querySelector('.Plus');
    const Remove = item.querySelector('.remove');

    // try to find this item's subtotal element; if not found, create one
    let itemSubtotalEl = item.querySelector('.Subtotal');
    if (!itemSubtotalEl) {
      itemSubtotalEl = document.createElement('span');
      itemSubtotalEl.className = 'Subtotal';
      // append it where you prefer inside the item; here appended at end
      item.appendChild(itemSubtotalEl);
    }

    // optional text_subtotal element (if exists)
    const textSubtotal = item.querySelector('.text_subtotal');

    function updateItemSubtotal() {
      const qty = parseInt(qtyEl.textContent) || 0;
      const price_num = parseFloat((priceEl.textContent || '').replace(/[^0-9.]/g, '')) || 0;
      itemSubtotalEl.textContent = (qty * price_num).toFixed(2); // store raw number text
      if (textSubtotal) textSubtotal.textContent = `Subtotal ×${qty}`;
      updateCartSummary();
    }

    Minus && Minus.addEventListener('click', () => {
      let qty = parseInt(qtyEl.textContent) || 0;
      if (qty > 1) {
        qty--;
        qtyEl.textContent = qty;
        updateItemSubtotal();
      }
    });

    Plus && Plus.addEventListener('click', () => {
      let qty = parseInt(qtyEl.textContent) || 0;
      qty++;
      qtyEl.textContent = qty;
      updateItemSubtotal();
    });

    Remove && Remove.addEventListener('click', () => {
      item.remove();
      updateCartSummary();
    });

    // initialize this item
    updateItemSubtotal();
  });

  // initialize summary on load
  updateCartSummary();
});
