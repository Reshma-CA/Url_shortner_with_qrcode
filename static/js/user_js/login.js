document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameField = document.getElementById('username');
    const passwordField = document.getElementById('password');
    

    form.addEventListener('submit', function(event) {
        let isValid = true;

        // Clear previous error messages
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');

        // Check if fields are not empty
        if (!usernameField.value.trim()) {
            isValid = false;
            document.getElementById('username-error').textContent = 'Username is required.';
        }
        
        if (!passwordField.value.trim()) {
            isValid = false;
            document.getElementById('password-error').textContent = 'Password is required.';
        }
        


        if (!isValid) {
            event.preventDefault(); // Prevent form submission
        }
    });
});