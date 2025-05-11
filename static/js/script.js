// Healthcare Login System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const loginForm = document.getElementById('login-form');
    const forgotForm = document.getElementById('forgot-password-form');
    
    // Helper function to show form validation errors
    function showValidationMessage(inputElement, message, isValid) {
        const feedbackElement = inputElement.nextElementSibling;
        if (!feedbackElement || !feedbackElement.classList.contains('invalid-feedback')) {
            const newFeedback = document.createElement('div');
            newFeedback.className = 'invalid-feedback';
            newFeedback.textContent = message;
            inputElement.parentNode.insertBefore(newFeedback, inputElement.nextSibling);
        } else {
            feedbackElement.textContent = message;
        }
        
        if (isValid) {
            inputElement.classList.remove('is-invalid');
            inputElement.classList.add('is-valid');
        } else {
            inputElement.classList.remove('is-valid');
            inputElement.classList.add('is-invalid');
        }
    }
    
    // Validate login form
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            // Username validation
            if (!username.value.trim()) {
                showValidationMessage(username, 'Username is required', false);
                isValid = false;
            } else {
                showValidationMessage(username, '', true);
            }
            
            // Password validation
            if (!password.value) {
                showValidationMessage(password, 'Password is required', false);
                isValid = false;
            } else {
                showValidationMessage(password, '', true);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Validate forgot password form
    if (forgotForm) {
        forgotForm.addEventListener('submit', function(event) {
            let isValid = true;
            const email = document.getElementById('email');
            
            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!email.value.trim()) {
                showValidationMessage(email, 'Email address is required', false);
                isValid = false;
            } else if (!emailRegex.test(email.value.trim())) {
                showValidationMessage(email, 'Please enter a valid email address', false);
                isValid = false;
            } else {
                showValidationMessage(email, '', true);
            }
            
            if (!isValid) {
                event.preventDefault();
            } else {
                // Show loading state - this would be more sophisticated in a real app
                const submitButton = forgotForm.querySelector('button[type="submit"]');
                submitButton.innerHTML = '<span class="spinner"></span> Sending...';
                submitButton.disabled = true;
            }
        });
    }
    
    // Password show/hide toggle
    const passwordToggle = document.querySelector('.password-toggle');
    if (passwordToggle) {
        passwordToggle.addEventListener('click', function() {
            const passwordField = document.getElementById('password');
            const icon = this.querySelector('i');
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
});
