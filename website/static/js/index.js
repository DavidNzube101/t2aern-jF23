const conversionRate = 1694.90;


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

// Payment Modal Functionality
function showPaymentModal() {
    currency = "USDT"
    modal = document.getElementById('paymentModal')
    modal.style.display = 'block'
    modal_price = modal.querySelector(".amount")
    modal_price_two = modal.querySelector(".amount-two")
    modal_address_code = modal.querySelector(".address-code")
    modal_address_code.textContent = "0x309632422dA612acA9E8fBF790A92D8F599D18e9"
    modal_price.textContent = `${document.querySelector("#cart-total").textContent} ${currency}`


    nairaAmount = parseFloat((document.querySelector("#cart-total").textContent).replace(/,/g, ""))
    console.log(nairaAmount, conversionRate);
    const usdtAmount = (nairaAmount / conversionRate).toFixed(7);
    modal_price.textContent = `${usdtAmount} ${currency}`
    modal_price_two.textContent = usdtAmount

}

function closePaymentModal() {
    document.getElementById('paymentModal').style.display = 'none';
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

function updateCounter(button, change, subject, offerTitle, price, upgradeId) {
    const counterSpan = button.parentElement.querySelector('span');
    let count = parseInt(counterSpan.textContent);
    count = Math.max(0, count + change);
    counterSpan.textContent = count;

    updateCart(subject, offerTitle, count, price, upgradeId);
}

function updateCart(subject, offerTitle, count, price, upgradeId) {
    const key = `${subject}-${offerTitle}`;
    if (count > 0) {
        cart[key] = { subject, offerTitle, count, price, upgradeId };
    } else {
        delete cart[key];
    }
    updateCartDisplay();
    console.log("Current cart:", cart); // Debug: Log the cart after each update
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


async function closePaymentModalAndUpdateHistory(cid) {
    const data = new FormData();
    const cartTotal = document.querySelector("#cart-total").textContent;
    const amount = (parseFloat(cartTotal.replace(/,/g, "")) / conversionRate).toFixed(7);
    
    data.append("amount", amount);
    data.append("crypsis_id", cid);

    // Fetch upgrade IDs from the cart items
    const upgradeIds = Object.values(cart).map(item => item.upgradeId).filter(id => id !== undefined);
    console.log("Upgrade IDs before filtering:", Object.values(cart).map(item => item.upgradeId)); // Debug: Log all upgradeIds before filtering
    console.log("Filtered Upgrade IDs:", upgradeIds);  // Log the filtered upgrade IDs
    data.append("upgrade_ids", JSON.stringify(upgradeIds));

    console.log("Sending data to server:", {
        amount,
        crypsis_id: cid,
        upgrade_ids: upgradeIds
    });

    try {
        const response = await fetch('/add-upgrade-request', {
            method: 'POST',
            body: data,
        });

        if (response.ok) {
            console.log("Upgrade request added successfully");
            document.getElementById('paymentModal').style.display = 'none';
            location.reload();
        } else {
            console.error("Failed to add upgrade request");
            // Handle error (e.g., show error message to user)
        }
    } catch (error) {
        console.error("Error sending upgrade request:", error);
        // Handle network errors
    }
}

// Initialize cart display
updateCartDisplay();

async function deleteHistory(hid){
    data = new FormData()
    data.append("history_id", hid)
    const response = await fetch('/delete-history', {
        method: 'POST',
        body: data,
    });

    if (response.ok) {
        console.log("Upgrade request added successfully");
        location.reload();
    } else {
        console.error("Failed to add upgrade request");
    }
}