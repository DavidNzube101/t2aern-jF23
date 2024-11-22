// Tab Functionality
function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabId).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');
}

// Counter Functionality
function updateCounter(button, change) {
    const counterSpan = button.parentElement.querySelector('span');
    let count = parseInt(counterSpan.textContent);
    count = Math.max(0, count + change); // Prevent negative numbers
    counterSpan.textContent = count;
}

// Modal Functionality
function showModal() {
    document.getElementById('aboutModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('aboutModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById('aboutModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

document.querySelectorAll('.faq-question').forEach(button => {
    button.addEventListener('click', () => {
        const answer = button.nextElementSibling;
        const arrow = button.querySelector('.arrow');
        
        // Toggle active state
        button.classList.toggle('active');
        
        // Toggle answer visibility
        if (answer.classList.contains('show')) {
            answer.classList.remove('show');
        } else {
            answer.classList.add('show');
        }
    });
});


// Cart state
let cart = {};
let total = 0;

function formatPrice(price) {
    return new Intl.NumberFormat('en-NG', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(price);
}

function updateCounter(button, change, subject, offerTitle, price) {
    const counterSpan = button.parentElement.querySelector('span');
    let count = parseInt(counterSpan.textContent);
    count = Math.max(0, count + change);
    counterSpan.textContent = count;

    updateCart(subject, offerTitle, count, price);
}

function updateCart(subject, offerTitle, count, price) {
    const key = `${subject}-${offerTitle}`;
    if (count > 0) {
        cart[key] = { subject, offerTitle, count, price };
    } else {
        delete cart[key];
    }
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    total = 0;

    if (Object.keys(cart).length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <p>Your cart is empty</p>
            </div>
        `;
    } else {
        for (const item of Object.values(cart)) {
            const itemTotal = item.count * item.price;
            total += itemTotal;

            cartItems.innerHTML += `
                <div class="cart-item">
                    <div class="cart-item-details">
                        <span class="cart-item-title">${item.subject}</span>
                        <span class="cart-item-subtitle">${item.offerTitle}</span>
                    </div>
                    <div class="cart-item-price">
                        ${item.count} × ₦${formatPrice(item.price)} = ₦${formatPrice(itemTotal)}
                    </div>
                </div>
            `;
        }
    }

    document.getElementById('cart-total').textContent = formatPrice(total);
}

// Initialize cart display
updateCartDisplay();