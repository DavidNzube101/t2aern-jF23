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