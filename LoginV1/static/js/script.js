/**
 * NoName System - Modern JavaScript
 * Enhanced functionality and animations for a better user experience
 */

// Translations for multi-language support
const translations = {
    'en': {
        'welcome': 'Welcome',
        'dashboard': 'Dashboard',
        'profile': 'Profile',
        'logout': 'Logout',
        'theme': 'Theme',
        'appointments': 'Appointments',
        'medicalHistory': 'Medical History',
        'medications': 'Medications',
        'darkMode': 'Dark Mode',
        'settings': 'Settings',
        'language': 'Language',
        'english': 'English',
        'spanish': 'Spanish',
        'loggedIn': 'You are now logged in.',
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'submit': 'Submit',
        'signIn': 'Sign In',
        'forgotPassword': 'Forgot Password',
        'resetPassword': 'Reset Password',
        'confirmPassword': 'Confirm Password',
        'rememberMe': 'Remember Me',
        'passwordResetRequested': 'Password reset requested',
        'checkYourEmail': 'Check your email for a reset link',
        'invalidCredentials': 'Invalid username or password',
        'passwordRequired': 'Password is required',
        'usernameRequired': 'Username is required',
        'emailRequired': 'Email is required',
        'validEmailRequired': 'Please enter a valid email',
        'passwordsDoNotMatch': 'Passwords do not match',
        'confirmPasswordRequired': 'Confirm password is required',
    },
    'es': {
        'welcome': 'Bienvenido',
        'dashboard': 'Panel de Control',
        'profile': 'Perfil',
        'logout': 'Cerrar Sesión',
        'theme': 'Tema',
        'appointments': 'Citas',
        'medicalHistory': 'Historial Médico',
        'medications': 'Medicamentos',
        'darkMode': 'Modo Oscuro',
        'settings': 'Configuración',
        'language': 'Idioma',
        'english': 'Inglés',
        'spanish': 'Español',
        'loggedIn': 'Has iniciado sesión correctamente.',
        'username': 'Usuario',
        'password': 'Contraseña',
        'email': 'Correo Electrónico',
        'submit': 'Enviar',
        'signIn': 'Iniciar Sesión',
        'forgotPassword': 'Olvidé mi Contraseña',
        'resetPassword': 'Restablecer Contraseña',
        'confirmPassword': 'Confirmar Contraseña',
        'rememberMe': 'Recordarme',
        'passwordResetRequested': 'Solicitud de restablecimiento de contraseña enviada',
        'checkYourEmail': 'Revisa tu correo para el enlace de restablecimiento',
        'invalidCredentials': 'Usuario o contraseña incorrectos',
        'passwordRequired': 'La contraseña es obligatoria',
        'usernameRequired': 'El nombre de usuario es obligatorio',
        'emailRequired': 'El correo electrónico es obligatorio',
        'validEmailRequired': 'Por favor ingresa un correo electrónico válido',
        'passwordsDoNotMatch': 'Las contraseñas no coinciden',
        'confirmPasswordRequired': 'La confirmación de contraseña es obligatoria',
    }
};

// Current language and theme
let currentLanguage = localStorage.getItem('language') || 'en';
let currentTheme = localStorage.getItem('theme') || 'light';

document.addEventListener('DOMContentLoaded', function() {
    // Apply saved theme
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    // Apply saved language
    applyLanguage(currentLanguage);
    
    // Theme toggle
    setupThemeToggle();
    
    // Language selector
    setupLanguageSelector();
    
    // Animación inicial para la página
    animatePageLoad();
    
    // Form validation
    setupFormValidation();
    
    // Password toggle
    setupPasswordToggle();
    
    // Setup alerts
    setupAlerts();
    
    // Setup tooltips and interactive elements
    setupInteractiveElements();
    
    // Enhanced security
    setupSecurityFeatures();
});

/**
 * Animate page load with subtle effects
 */
function animatePageLoad() {
    const authForm = document.querySelector('.auth-form');
    const logoContainer = document.querySelector('.logo-container');
    
    if (authForm) {
        // Añadir clase para iniciar animación
        setTimeout(() => {
            authForm.style.opacity = '1';
            authForm.style.transform = 'translateY(0)';
        }, 100);
    }
    
    if (logoContainer) {
        // Añadir animación al logo
        setTimeout(() => {
            const img = logoContainer.querySelector('img');
            if (img) {
                img.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    img.style.transform = 'scale(1)';
                }, 300);
            }
        }, 300);
    }
}

/**
 * Setup form validation for all forms
 */
function setupFormValidation() {
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input:not([type="hidden"]):not([type="submit"])');
        
        // Add input event listeners for real-time validation
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                validateInput(this);
            });
            
            input.addEventListener('blur', function() {
                validateInput(this, true);
            });
        });
        
        // Form submit validation
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateInput(input, true)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                // Shake effect on form for invalid submissions
                form.classList.add('shake');
                setTimeout(() => {
                    form.classList.remove('shake');
                }, 500);
            } else if (form.id === 'forgot-password-form') {
                // Show loading state for forgot password form
                const submitButton = form.querySelector('button[type="submit"]');
                submitButton.innerHTML = '<span class="spinner"></span> Enviando...';
                submitButton.disabled = true;
            }
        });
    });
}

/**
 * Setup theme toggle functionality
 */
function setupThemeToggle() {
    // Add theme toggle to the navbar if user is logged in
    const navbar = document.querySelector('.navbar .container');
    if (navbar) {
        const themeToggle = document.createElement('div');
        themeToggle.className = 'theme-switch';
        themeToggle.innerHTML = `
            <span class="theme-switch-label" data-translate="theme">Tema</span>
            <label class="switch">
                <input type="checkbox" id="themeSwitch" ${currentTheme === 'dark' ? 'checked' : ''}>
                <span class="slider"></span>
            </label>
        `;
        
        // If there's a nav collapse, insert before it, otherwise append to navbar
        const navCollapse = navbar.querySelector('.navbar-collapse');
        if (navCollapse) {
            navbar.insertBefore(themeToggle, navCollapse);
        } else {
            navbar.appendChild(themeToggle);
        }
        
        // Add event listener to the theme toggle
        const themeSwitchInput = document.getElementById('themeSwitch');
        if (themeSwitchInput) {
            themeSwitchInput.addEventListener('change', function() {
                if (this.checked) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    localStorage.setItem('theme', 'dark');
                    currentTheme = 'dark';
                } else {
                    document.documentElement.setAttribute('data-theme', 'light');
                    localStorage.setItem('theme', 'light');
                    currentTheme = 'light';
                }
            });
        }
    }
}

/**
 * Setup language selector
 */
function setupLanguageSelector() {
    // Add language selector to the navbar if user is logged in
    const navbar = document.querySelector('.navbar .container');
    if (navbar) {
        const languageSelector = document.createElement('div');
        languageSelector.className = 'language-selector';
        languageSelector.innerHTML = `
            <select id="languageSelect">
                <option value="en" ${currentLanguage === 'en' ? 'selected' : ''} data-translate="english">English</option>
                <option value="es" ${currentLanguage === 'es' ? 'selected' : ''} data-translate="spanish">Español</option>
            </select>
        `;
        
        // If there's a theme toggle, insert after it, otherwise insert at the same place
        const themeToggle = navbar.querySelector('.theme-switch');
        if (themeToggle) {
            navbar.insertBefore(languageSelector, themeToggle.nextSibling);
        } else {
            const navCollapse = navbar.querySelector('.navbar-collapse');
            if (navCollapse) {
                navbar.insertBefore(languageSelector, navCollapse);
            } else {
                navbar.appendChild(languageSelector);
            }
        }
        
        // Add event listener to the language selector
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.addEventListener('change', function() {
                const newLanguage = this.value;
                localStorage.setItem('language', newLanguage);
                currentLanguage = newLanguage;
                applyLanguage(newLanguage);
                // Reload form labels if on a form page
                if (document.querySelector('form')) {
                    updateFormLabels();
                }
            });
        }
    }
}

/**
 * Apply language translations to the page
 * @param {string} language - Language code to apply
 */
function applyLanguage(language) {
    // Set data-language attribute on body to help with CSS selectors if needed
    document.body.setAttribute('data-language', language);
    
    // Translate elements with data-translate attribute
    const translatableElements = document.querySelectorAll('[data-translate]');
    translatableElements.forEach(element => {
        const translationKey = element.getAttribute('data-translate');
        if (translations[language] && translations[language][translationKey]) {
            element.textContent = translations[language][translationKey];
        }
    });
    
    // Update language selector if it exists
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = language;
    }
}

/**
 * Update form labels with the current language
 */
function updateFormLabels() {
    // Update username label
    const usernameLabel = document.querySelector('label[for="username"]');
    if (usernameLabel) {
        usernameLabel.textContent = translations[currentLanguage].username;
    }
    
    // Update password label
    const passwordLabel = document.querySelector('label[for="password"]');
    if (passwordLabel) {
        passwordLabel.textContent = translations[currentLanguage].password;
    }
    
    // Update email label
    const emailLabel = document.querySelector('label[for="email"]');
    if (emailLabel) {
        emailLabel.textContent = translations[currentLanguage].email;
    }
    
    // Update confirm password label
    const confirmPasswordLabel = document.querySelector('label[for="confirm_password"]');
    if (confirmPasswordLabel) {
        confirmPasswordLabel.textContent = translations[currentLanguage].confirmPassword;
    }
    
    // Update remember me label
    const rememberMeLabel = document.querySelector('label[for="remember-me"]');
    if (rememberMeLabel) {
        rememberMeLabel.textContent = translations[currentLanguage].rememberMe;
    }
    
    // Update submit buttons
    const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
    submitButtons.forEach(button => {
        button.value = translations[currentLanguage].submit;
        if (button.tagName === 'BUTTON') {
            button.textContent = translations[currentLanguage].submit;
        }
    });
}

/**
 * Setup enhanced security features
 */
function setupSecurityFeatures() {
    // Implement session timeout
    setupSessionTimeout();
    
    // Add CSRF protection to forms
    setupCSRFProtection();
    
    // Add basic password strength meter
    setupPasswordStrengthMeter();
}

/**
 * Setup session timeout
 */
function setupSessionTimeout() {
    // Set session timeout to 30 minutes
    const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes in milliseconds
    let sessionTimeoutId;
    
    function resetSessionTimeout() {
        clearTimeout(sessionTimeoutId);
        sessionTimeoutId = setTimeout(() => {
            // Show timeout warning
            showSessionTimeoutWarning();
        }, SESSION_TIMEOUT);
    }
    
    // Reset timeout on user activity
    ['click', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
        document.addEventListener(event, resetSessionTimeout);
    });
    
    // Initialize the timeout
    resetSessionTimeout();
}

/**
 * Show session timeout warning
 */
function showSessionTimeoutWarning() {
    // Create a modal or notification for session timeout warning
    const modal = document.createElement('div');
    modal.className = 'session-timeout-modal';
    modal.innerHTML = `
        <div class="session-timeout-content">
            <h3>Sesión a punto de expirar</h3>
            <p>Tu sesión está a punto de expirar por inactividad.</p>
            <div class="session-timeout-buttons">
                <button class="btn btn-primary" id="extendSession">Continuar sesión</button>
                <button class="btn btn-secondary" id="logoutNow">Cerrar sesión</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add event listeners to buttons
    document.getElementById('extendSession').addEventListener('click', () => {
        // Remove the modal
        modal.remove();
        // Reset the session timeout
        setupSessionTimeout();
    });
    
    document.getElementById('logoutNow').addEventListener('click', () => {
        // Redirect to logout
        window.location.href = '/logout';
    });
    
    // Auto logout after 1 minute if no action taken
    setTimeout(() => {
        window.location.href = '/logout';
    }, 60000);
}

/**
 * Setup CSRF protection
 */
function setupCSRFProtection() {
    // Add CSRF token to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Check if the form already has a CSRF token
        if (!form.querySelector('input[name="csrf_token"]')) {
            // Generate a random token
            const csrfToken = generateCSRFToken();
            
            // Add the token to the form
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrf_token';
            csrfInput.value = csrfToken;
            
            form.appendChild(csrfInput);
            
            // Store the token in session storage
            sessionStorage.setItem('csrf_token', csrfToken);
        }
    });
}

/**
 * Generate a CSRF token
 * @returns {string} - Random CSRF token
 */
function generateCSRFToken() {
    // Generate a random string for CSRF token
    const array = new Uint32Array(8);
    window.crypto.getRandomValues(array);
    return Array.from(array, dec => ('0' + dec.toString(16)).substr(-2)).join('');
}

/**
 * Setup password strength meter
 */
function setupPasswordStrengthMeter() {
    // Add password strength meter to password fields
    const passwordFields = document.querySelectorAll('input[type="password"][id="password"]');
    passwordFields.forEach(field => {
        // Create strength meter
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'password-strength-meter';
        strengthMeter.innerHTML = `
            <div class="strength-bar">
                <div class="strength-indicator"></div>
            </div>
            <div class="strength-text"></div>
        `;
        
        // Insert after the password field or its parent if in input group
        const fieldParent = field.closest('.input-group') || field.parentNode;
        fieldParent.parentNode.insertBefore(strengthMeter, fieldParent.nextSibling);
        
        // Add input event listener to update strength
        field.addEventListener('input', function() {
            updatePasswordStrength(this.value, strengthMeter);
        });
    });
}

/**
 * Update password strength indicator
 * @param {string} password - Password to check
 * @param {HTMLElement} meterElement - Strength meter element
 */
function updatePasswordStrength(password, meterElement) {
    // Calculate password strength
    let strength = 0;
    let feedback = '';
    
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[a-z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    
    // Update the strength indicator
    const indicator = meterElement.querySelector('.strength-indicator');
    const strengthText = meterElement.querySelector('.strength-text');
    
    // Reset classes
    indicator.className = 'strength-indicator';
    
    // Set width and class based on strength
    const strengthPercentage = Math.min(100, (strength / 6) * 100);
    indicator.style.width = `${strengthPercentage}%`;
    
    // Add appropriate class and text
    if (strength <= 2) {
        indicator.classList.add('weak');
        feedback = currentLanguage === 'es' ? 'Débil' : 'Weak';
    } else if (strength <= 4) {
        indicator.classList.add('medium');
        feedback = currentLanguage === 'es' ? 'Moderada' : 'Medium';
    } else {
        indicator.classList.add('strong');
        feedback = currentLanguage === 'es' ? 'Fuerte' : 'Strong';
    }
    
    strengthText.textContent = feedback;
}

/**
 * Validate a single input field
 * @param {HTMLElement} input - Input element to validate
 * @param {boolean} showMessage - Whether to show validation message
 * @returns {boolean} - Whether input is valid
 */
function validateInput(input, showMessage = false) {
    let isValid = true;
    let message = '';
    
    // Different validation based on input type or id
    switch(input.id) {
        case 'username':
            if (!input.value.trim()) {
                isValid = false;
                message = translations[currentLanguage].usernameRequired;
            }
            break;
            
        case 'password':
            if (!input.value) {
                isValid = false;
                message = translations[currentLanguage].passwordRequired;
            }
            break;
            
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!input.value.trim()) {
                isValid = false;
                message = translations[currentLanguage].emailRequired;
            } else if (!emailRegex.test(input.value.trim())) {
                isValid = false;
                message = translations[currentLanguage].validEmailRequired;
            }
            break;
            
        case 'confirm_password':
            const passwordInput = document.getElementById('password');
            if (!input.value) {
                isValid = false;
                message = translations[currentLanguage].confirmPasswordRequired;
            } else if (passwordInput && input.value !== passwordInput.value) {
                isValid = false;
                message = translations[currentLanguage].passwordsDoNotMatch;
            }
            break;
    }
    
    // Show validation state
    if (showMessage) {
        showValidationMessage(input, message, isValid);
    }
    
    return isValid;
}

/**
 * Show validation message for an input
 * @param {HTMLElement} inputElement - Input element
 * @param {string} message - Validation message
 * @param {boolean} isValid - Whether input is valid
 */
function showValidationMessage(inputElement, message, isValid) {
    // Check if input is in an input group
    const parent = inputElement.closest('.input-group') || inputElement.parentNode;
    
    // Remove any existing feedback
    const existingFeedback = parent.querySelector('.invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Add new feedback if needed
    if (!isValid && message) {
        const newFeedback = document.createElement('div');
        newFeedback.className = 'invalid-feedback';
        newFeedback.textContent = message;
        
        // Add feedback after the input or input group
        if (inputElement.closest('.input-group')) {
            inputElement.closest('.input-group').parentNode.appendChild(newFeedback);
        } else {
            inputElement.parentNode.appendChild(newFeedback);
        }
    }
    
    // Update input classes
    if (isValid) {
        inputElement.classList.remove('is-invalid');
        inputElement.classList.add('is-valid');
    } else {
        inputElement.classList.remove('is-valid');
        inputElement.classList.add('is-invalid');
    }
}

/**
 * Setup password show/hide toggle
 */
function setupPasswordToggle() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordField = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (passwordField && passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
                
                // Auto-hide password after 3 seconds
                setTimeout(() => {
                    passwordField.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }, 3000);
            } else if (passwordField) {
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
}

/**
 * Setup alerts with auto-dismiss and animations
 */
function setupAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
    alerts.forEach(function(alert, index) {
        // Delay appearance for staggered effect
        setTimeout(() => {
            alert.style.opacity = '1';
            alert.style.transform = 'translateY(0)';
        }, index * 150);
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000 + (index * 150));
    });
    
    // Setup close buttons
    const closeButtons = document.querySelectorAll('.btn-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            }
        });
    });
}

/**
 * Setup tooltips and interactive elements
 */
function setupInteractiveElements() {
    // Animate cards on hover
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = 'var(--shadow-md)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--shadow)';
        });
    });
    
    // Add subtle hover effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add input focus effects
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentNode.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentNode.classList.remove('input-focused');
        });
    });
}

// Add animation keyframes to the document
const style = document.createElement('style');
style.textContent = `
    /* Animations */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    
    .shake {
        animation: shake 0.5s ease-in-out;
    }
    
    .auth-form {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }
    
    .input-focused {
        transform: translateY(-2px);
        transition: transform 0.3s ease;
    }
`;

document.head.appendChild(style);
