// Drawer functionality
function openDrawer(upgradeId) {
    const drawer = document.getElementById('drawer');
    const content = document.getElementById('drawerContent');
    
    // Populate drawer content based on upgradeId
    content.innerHTML = `
        <h3>Upgrade ID: ${upgradeId}</h3>
        <p>Student: John Doe</p>
        <p>Requested: 2024-01-20</p>
        <p>Type: Mark Adder</p>
        <p>Amount: $150.00</p>
        <p>Status: Pending</p>
        <p>Details: Request to add 15 marks to Final Exam score.</p>
    `;
    
    drawer.classList.add('open');
}

function closeDrawer() {
    const drawer = document.getElementById('drawer');
    drawer.classList.remove('open');
}

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
    });
});

// Checkbox form submission
document.querySelectorAll('.checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            // Simulate form submission
            console.log(`Marking upgrade ${e.target.id} as completed`);
            // Here you would typically make an API call
            setTimeout(() => {
                const upgradeItem = e.target.closest('.upgrade-item');
                upgradeItem.style.opacity = '0.5';
            }, 500);
        }
    });
});

// Add touch events for drawer
let startY;
const drawer = document.getElementById('drawer');

drawer.addEventListener('touchstart', (e) => {
    startY = e.touches[0].clientY;
});

drawer.addEventListener('touchmove', (e) => {
    const currentY = e.touches[0].clientY;
    const deltaY = currentY - startY;
    
    if (deltaY > 0) {
        drawer.style.bottom = `-${deltaY}px`;
    }
});

drawer.addEventListener('touchend', (e) => {
    const deltaY = e.changedTouches[0].clientY - startY;
    
    if (deltaY > 100) {
        closeDrawer();
    } else {
        drawer.style.bottom = '0';
    }
});