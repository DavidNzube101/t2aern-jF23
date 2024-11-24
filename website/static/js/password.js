document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('passwordModal');
    const correctPassword = "09erdm%%ret*2";

    // Disable interaction with the rest of the page
    document.body.style.overflow = "hidden";

    function checkPassword() {
        const input = document.getElementById('passwordInput').value;

        if (input === correctPassword) {
            modal.style.display = "none";
            document.body.style.overflow = "auto"; // Restore page interaction
        } else {
            alert("Incorrect password. Try again.");
        }
    }

    if (event.key === 'Enter' || event.keyCode === 13) {
        checkPassword
    }

    // Attach the function to the global scope
    window.checkPassword = checkPassword;

    
});
