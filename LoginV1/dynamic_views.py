from markupsafe import Markup
from datetime import datetime

class View:
    """Clase base para generar vistas dinámicas en Python sin necesidad de archivos HTML"""
    
    @staticmethod
    def render_base_template(title, content, user=None):
        """Renderiza la plantilla base con el contenido proporcionado"""
        current_year = datetime.now().year
        
        # Header y navegación
        navbar = f"""
        <nav class="navbar navbar-expand-lg">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <img src="/static/imgs/healthcare-logo.svg" alt="NoName Logo">
                    No<span>Name</span>
                </a>
                {'<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>' if user else ''}
        """
        
        # Añadir menú de navegación si el usuario está autenticado
        if user:
            navbar += f"""
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/dashboard">
                                <i class="fas fa-tachometer-alt me-1"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <i class="fas fa-user me-1"></i> Profile
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/logout">
                                <i class="fas fa-sign-out-alt me-1"></i> Logout
                            </a>
                        </li>
                    </ul>
                </div>
            """
        
        navbar += """
            </div>
        </nav>
        """
        
        # Footer
        footer = f"""
        <footer class="footer">
            <div class="container">
                <p>&copy; {current_year} NoName System. All rights reserved.</p>
            </div>
        </footer>
        """
        
        # Scripts comunes
        scripts = """
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        
        <!-- Custom JS -->
        <script src="/static/js/script.js"></script>
        """
        
        # Estructura completa de la página
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - NoName System</title>
            
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            
            <!-- Font Awesome -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            
            <!-- Google Fonts -->
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
            
            <!-- Custom CSS -->
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            {navbar}
            
            <div class="main-container">
                <div class="container">
                    {content}
                </div>
            </div>
            
            {footer}
            
            {scripts}
        </body>
        </html>
        """
        
        return Markup(html)

    @staticmethod
    def render_login_form(form, flashed_messages=None):
        """Renderiza el formulario de login"""
        
        # Flash messages
        flash_html = ""
        if flashed_messages:
            for category, message in flashed_messages:
                flash_html += f"""
                <div class="alert alert-{category} alert-dismissible fade show" role="alert">
                    {message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                """
        
        # Formulario de login
        form_html = f"""
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="auth-form login-form">
                    <div class="logo-container">
                        <img src="/static/imgs/healthcare-logo.svg" alt="NoName Logo" class="mb-2">
                        <h2>NoName Login</h2>
                    </div>
                    
                    <form id="login-form" method="POST" action="/login">
                        {form.hidden_tag()}
                        
                        <div class="mb-3">
                            {form.username.label(class_="form-label")}
                            {form.username(class_="form-control", placeholder="Enter your username", id="username")}
                            {"".join([f'<div class="invalid-feedback d-block">{error}</div>' for error in form.username.errors])}
                        </div>
                        
                        <div class="mb-3">
                            {form.password.label(class_="form-label")}
                            <div class="input-group">
                                {form.password(class_="form-control", placeholder="Enter your password", id="password")}
                                <button class="btn btn-outline-secondary password-toggle" type="button">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </div>
                            {"".join([f'<div class="invalid-feedback d-block">{error}</div>' for error in form.password.errors])}
                        </div>
                        
                        <div class="mb-3 form-check">
                            {form.remember_me(class_="form-check-input", id="remember-me")}
                            {form.remember_me.label(class_="form-check-label", for_="remember-me")}
                        </div>
                        
                        <div class="d-grid gap-2">
                            {form.submit(class_="btn btn-primary btn-lg")}
                        </div>
                        
                        <div class="auth-links">
                            <p>Forgot your password? <a href="/forgot-password">Reset it here</a></p>
                        </div>
                    </form>
                    
                    <div class="mt-4">
                        <div class="card border-0 bg-light">
                            <div class="card-body p-3">
                                <h6 class="card-title mb-2"><i class="fas fa-info-circle text-primary me-2"></i>Demo Accounts</h6>
                                <div class="small text-muted">
                                    <p class="mb-1"><strong>Admin:</strong> admin / password123</p>
                                    <p class="mb-1"><strong>Doctor:</strong> doctor / password123</p>
                                    <p class="mb-1"><strong>Patient:</strong> patient / password123</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return flash_html + form_html

    @staticmethod
    def render_forgot_password_form(form, flashed_messages=None):
        """Renderiza el formulario de recuperación de contraseña"""
        
        # Flash messages
        flash_html = ""
        if flashed_messages:
            for category, message in flashed_messages:
                flash_html += f"""
                <div class="alert alert-{category} alert-dismissible fade show" role="alert">
                    {message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                """
        
        # Formulario de recuperación de contraseña
        form_html = f"""
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="auth-form forgot-password">
                    <div class="logo-container">
                        <img src="/static/imgs/healthcare-logo.svg" alt="NoName Logo" class="mb-2">
                        <h2>Reset Your Password</h2>
                    </div>
                    
                    <p class="text-center text-muted mb-4">Enter your email address and we'll send you a link to reset your password.</p>
                    
                    <form id="forgot-password-form" method="POST" action="/forgot-password">
                        {form.hidden_tag()}
                        
                        <div class="mb-4">
                            {form.email.label(class_="form-label")}
                            {form.email(class_="form-control", placeholder="Enter your email address", id="email")}
                            {"".join([f'<div class="invalid-feedback d-block">{error}</div>' for error in form.email.errors])}
                        </div>
                        
                        <div class="d-grid gap-2 mb-3">
                            {form.submit(class_="btn btn-primary btn-lg")}
                        </div>
                        
                        <div class="auth-links">
                            <p>Remember your password? <a href="/login">Back to Login</a></p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        """
        
        return flash_html + form_html

    @staticmethod
    def render_reset_password_form(form, flashed_messages=None):
        """Renderiza el formulario de restablecimiento de contraseña"""
        
        # Flash messages
        flash_html = ""
        if flashed_messages:
            for category, message in flashed_messages:
                flash_html += f"""
                <div class="alert alert-{category} alert-dismissible fade show" role="alert">
                    {message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                """
        
        # Formulario de restablecimiento de contraseña
        form_html = f"""
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="auth-form reset-password">
                    <div class="logo-container">
                        <img src="/static/imgs/healthcare-logo.svg" alt="NoName Logo" class="mb-2">
                        <h2>Reset Your Password</h2>
                    </div>
                    
                    <form method="POST">
                        {form.hidden_tag()}
                        <div class="mb-3">
                            {form.password.label(class_="form-label")}
                            {form.password(class_="form-control")}
                            {"".join([f'<div class="invalid-feedback d-block">{error}</div>' for error in form.password.errors])}
                        </div>
                        <div class="mb-3">
                            {form.confirm_password.label(class_="form-label")}
                            {form.confirm_password(class_="form-control")}
                            {"".join([f'<div class="invalid-feedback d-block">{error}</div>' for error in form.confirm_password.errors])}
                        </div>
                        <div class="d-grid">
                            {form.submit(class_="btn btn-primary btn-lg")}
                        </div>
                    </form>
                    
                    <div class="auth-links">
                        <p>Remember your password? <a href="/login">Back to Login</a></p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return flash_html + form_html

    @staticmethod
    def render_dashboard(user, flashed_messages=None, appointments=None, medications=None, messages=None):
        """Renderiza el panel de control adaptado al rol del usuario"""
        
        # Flash messages
        flash_html = ""
        if flashed_messages:
            for category, message in flashed_messages:
                flash_html += f"""
                <div class="alert alert-{category} alert-dismissible fade show" role="alert">
                    {message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                """
        
        # Contenido según el rol del usuario
        content = ""
        
        # Dashboard para pacientes
        if user.role == 'patient':
            content = View._render_patient_dashboard(user, appointments, medications, messages)
        
        # Dashboard para doctores
        elif user.role == 'doctor':
            content = View._render_doctor_dashboard(user, appointments, medications, messages)
        
        # Dashboard para administradores
        elif user.role == 'admin':
            content = View._render_admin_dashboard(user, appointments, medications, messages)
        
        return flash_html + content
    
    @staticmethod
    def _render_patient_dashboard(user, appointments=None, medications=None, messages=None):
        """Renderiza el dashboard específico para pacientes"""
        from datetime import datetime
        current_date = datetime.now().strftime("%d de %B, %Y")
        
        # Encabezado del dashboard
        header = f"""
        <div class="dashboard-header mb-4">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="h3 mb-0" data-translate="dashboard">Panel de Paciente</h1>
                    <p class="text-muted" data-translate="welcome">¡Bienvenido, {user.username}! <span class="badge role-{user.role}">{user.role.title()}</span></p>
                    <p class="text-muted small">{current_date}</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <a href="/messages" class="btn btn-sm btn-outline-primary me-2">
                        <i class="fas fa-envelope me-1"></i> <span class="badge bg-danger">{len([m for m in messages if not m.read]) if messages else 0}</span>
                    </a>
                    <a href="/profile" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-cog me-1"></i> <span data-translate="settings">Perfil</span>
                    </a>
                </div>
            </div>
        </div>
        """
        
        # Estadísticas de paciente
        stats = f"""
        <!-- Tarjetas de estadísticas para pacientes -->
        <div class="dashboard-stats mb-4">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <h3>{len(appointments) if appointments else 0}</h3>
                <p data-translate="appointments">Citas Pendientes</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-pills"></i>
                </div>
                <h3>{len(medications) if medications else 0}</h3>
                <p data-translate="medications">Medicamentos Activos</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-envelope"></i>
                </div>
                <h3>{len([m for m in messages if not m.read]) if messages else 0}</h3>
                <p data-translate="newMessages">Mensajes Nuevos</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-heartbeat"></i>
                </div>
                <h3>98%</h3>
                <p>Estado de Salud</p>
            </div>
        </div>
        """
        
        # Próximas citas
        appointment_items = ""
        if appointments and len(appointments) > 0:
            for appt in appointments[:3]:  # Solo las 3 más próximas
                appointment_items += f"""
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-0">{appt.title}</h6>
                        <small class="text-muted">Dr. {appt.doctor.username}</small>
                    </div>
                    <div class="text-end">
                        <div class="badge bg-primary mb-1">{appt.date.strftime('%H:%M')}</div>
                        <div class="d-block text-muted small">{appt.date.strftime('%d/%m/%Y')}</div>
                    </div>
                </li>
                """
        else:
            appointment_items = """
            <li class="list-group-item text-center">
                <p class="text-muted mb-0">No tienes citas programadas</p>
            </li>
            """
        
        # Medicamentos activos
        medication_items = ""
        if medications and len(medications) > 0:
            for med in medications[:3]:  # Solo los 3 más recientes
                medication_items += f"""
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-0">{med.name} {med.dosage}</h6>
                        <small class="text-muted">{med.frequency}</small>
                    </div>
                    <div class="text-end">
                        <span class="badge bg-success">Activo</span>
                    </div>
                </li>
                """
        else:
            medication_items = """
            <li class="list-group-item text-center">
                <p class="text-muted mb-0">No tienes medicamentos activos</p>
            </li>
            """
        
        # Contenido principal
        content = f"""
        {header}
        {stats}
        
        <div class="row">
            <!-- Citas próximas -->
            <div class="col-lg-6 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-calendar-check me-2"></i> Próximas Citas
                        </h5>
                        <a href="/appointments" class="btn btn-sm btn-primary">
                            <i class="fas fa-plus me-1"></i> Nueva Cita
                        </a>
                    </div>
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush">
                            {appointment_items}
                        </ul>
                    </div>
                    <div class="card-footer text-end">
                        <a href="/appointments" class="btn btn-link btn-sm text-decoration-none">Ver todas <i class="fas fa-arrow-right ms-1"></i></a>
                    </div>
                </div>
            </div>
            
            <!-- Medicamentos activos -->
            <div class="col-lg-6 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-pills me-2"></i> Medicamentos Activos
                        </h5>
                    </div>
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush">
                            {medication_items}
                        </ul>
                    </div>
                    <div class="card-footer text-end">
                        <a href="/medications" class="btn btn-link btn-sm text-decoration-none">Ver todos <i class="fas fa-arrow-right ms-1"></i></a>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return content
    
    @staticmethod
    def _render_doctor_dashboard(user, appointments=None, medications=None, messages=None):
        """Renderiza el dashboard específico para doctores"""
        from datetime import datetime
        current_date = datetime.now().strftime("%d de %B, %Y")
        
        # Encabezado del dashboard
        header = f"""
        <div class="dashboard-header mb-4">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="h3 mb-0" data-translate="dashboard">Panel de Doctor</h1>
                    <p class="text-muted" data-translate="welcome">¡Bienvenido, Dr. {user.username}! <span class="badge role-{user.role}">{user.role.title()}</span></p>
                    <p class="text-muted small">{current_date}</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <a href="/doctor/messages" class="btn btn-sm btn-outline-primary me-2">
                        <i class="fas fa-envelope me-1"></i> <span class="badge bg-danger">{len([m for m in messages if not m.read]) if messages else 0}</span>
                    </a>
                    <a href="/doctor/profile" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-cog me-1"></i> <span data-translate="settings">Perfil</span>
                    </a>
                </div>
            </div>
        </div>
        """
        
        # Estadísticas de doctor
        stats = f"""
        <!-- Tarjetas de estadísticas para doctores -->
        <div class="dashboard-stats mb-4">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <h3>{len(appointments) if appointments else 0}</h3>
                <p data-translate="appointments">Citas del Día</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-user-injured"></i>
                </div>
                <h3>15</h3>
                <p data-translate="patients">Pacientes</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-envelope"></i>
                </div>
                <h3>{len([m for m in messages if not m.read]) if messages else 0}</h3>
                <p data-translate="newMessages">Mensajes Nuevos</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-prescription"></i>
                </div>
                <h3>{len(medications) if medications else 0}</h3>
                <p data-translate="prescriptions">Recetas</p>
            </div>
        </div>
        """
        
        # Citas del día
        appointment_items = ""
        if appointments and len(appointments) > 0:
            for appt in appointments[:5]:  # Solo las 5 más próximas
                appointment_items += f"""
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-0">{appt.title}</h6>
                        <small class="text-muted">Paciente: {appt.patient.username}</small>
                    </div>
                    <div class="text-end">
                        <div class="badge bg-primary mb-1">{appt.date.strftime('%H:%M')}</div>
                        <div class="d-block text-muted small">{appt.date.strftime('%d/%m/%Y')}</div>
                    </div>
                </li>
                """
        else:
            appointment_items = """
            <li class="list-group-item text-center">
                <p class="text-muted mb-0">No tienes citas programadas para hoy</p>
            </li>
            """
        
        # Contenido principal
        content = f"""
        {header}
        {stats}
        
        <div class="row">
            <!-- Citas del día -->
            <div class="col-lg-8 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-calendar-day me-2"></i> Agenda del Día
                        </h5>
                        <div>
                            <a href="/doctor/appointments/new" class="btn btn-sm btn-primary">
                                <i class="fas fa-plus me-1"></i> Nueva Cita
                            </a>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush">
                            {appointment_items}
                        </ul>
                    </div>
                    <div class="card-footer text-end">
                        <a href="/doctor/appointments" class="btn btn-link btn-sm text-decoration-none">Ver agenda completa <i class="fas fa-arrow-right ms-1"></i></a>
                    </div>
                </div>
            </div>
            
            <!-- Acciones rápidas -->
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-user-md me-2"></i> Acciones Rápidas
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <a href="/doctor/prescriptions/new" class="btn btn-outline-primary">
                                <i class="fas fa-prescription me-1"></i> Nueva Receta
                            </a>
                            <a href="/doctor/messages/new" class="btn btn-outline-primary">
                                <i class="fas fa-envelope me-1"></i> Enviar Mensaje
                            </a>
                            <a href="/doctor/patients" class="btn btn-outline-primary">
                                <i class="fas fa-users me-1"></i> Mis Pacientes
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <!-- Mensajes recientes -->
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-envelope me-2"></i> Mensajes Recientes
                        </h5>
                    </div>
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush">
                """
        
        # Mensajes recientes
        if messages and len(messages) > 0:
            for msg in messages[:3]:  # Solo los 3 más recientes
                read_status = "" if msg.read else '<span class="badge bg-danger ms-2">Nuevo</span>'
                content += f"""
                <li class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-0">{msg.subject} {read_status}</h6>
                            <small class="text-muted">De: {msg.sender.username}</small>
                        </div>
                        <div class="text-end">
                            <small class="text-muted">{msg.timestamp.strftime('%d/%m/%Y %H:%M')}</small>
                        </div>
                    </div>
                </li>
                """
        else:
            content += """
                <li class="list-group-item text-center">
                    <p class="text-muted mb-0">No tienes mensajes nuevos</p>
                </li>
            """
        
        content += """
                        </ul>
                    </div>
                    <div class="card-footer text-end">
                        <a href="/doctor/messages" class="btn btn-link btn-sm text-decoration-none">Ver todos <i class="fas fa-arrow-right ms-1"></i></a>
                    </div>
                </div>
            </div>
            
            <!-- Recetas recientes -->
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-prescription me-2"></i> Recetas Recientes
                        </h5>
                    </div>
                    <div class="card-body p-0">
                        <ul class="list-group list-group-flush">
                """
        
        # Medicamentos recientes
        if medications and len(medications) > 0:
            for med in medications[:3]:  # Solo los 3 más recientes
                content += f"""
                <li class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-0">{med.name} {med.dosage}</h6>
                            <small class="text-muted">Para: {med.patient.username}</small>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-success">Activo</span>
                        </div>
                    </div>
                </li>
                """
        else:
            content += """
                <li class="list-group-item text-center">
                    <p class="text-muted mb-0">No has recetado medicamentos recientemente</p>
                </li>
            """
        
        content += """
                        </ul>
                    </div>
                    <div class="card-footer text-end">
                        <a href="/doctor/prescriptions" class="btn btn-link btn-sm text-decoration-none">Ver todas <i class="fas fa-arrow-right ms-1"></i></a>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return content
    
    @staticmethod
    def _render_admin_dashboard(user, appointments=None, medications=None, messages=None):
        """Renderiza el dashboard específico para administradores"""
        from datetime import datetime
        current_date = datetime.now().strftime("%d de %B, %Y")
        
        # Encabezado del dashboard
        header = f"""
        <div class="dashboard-header mb-4">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="h3 mb-0" data-translate="dashboard">Panel de Administración</h1>
                    <p class="text-muted" data-translate="welcome">¡Bienvenido, {user.username}! <span class="badge role-{user.role}">{user.role.title()}</span></p>
                    <p class="text-muted small">{current_date}</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <a href="/admin/messages" class="btn btn-sm btn-outline-primary me-2">
                        <i class="fas fa-envelope me-1"></i> <span class="badge bg-danger">{len([m for m in messages if not m.read]) if messages else 0}</span>
                    </a>
                    <a href="/admin/profile" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-cog me-1"></i> <span data-translate="settings">Configuración</span>
                    </a>
                </div>
            </div>
        </div>
        """
        
        # Estadísticas de administrador
        stats = """
        <!-- Tarjetas de estadísticas para administradores -->
        <div class="dashboard-stats mb-4">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-users"></i>
                </div>
                <h3>45</h3>
                <p data-translate="totalUsers">Usuarios Totales</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-user-md"></i>
                </div>
                <h3>12</h3>
                <p data-translate="doctors">Doctores</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-user-injured"></i>
                </div>
                <h3>32</h3>
                <p data-translate="patients">Pacientes</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <h3>28</h3>
                <p data-translate="todayAppointments">Citas Hoy</p>
            </div>
        </div>
        """
        
        # Opciones de administración
        admin_options = """
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-cogs me-2"></i> Acciones Administrativas
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-3">
                                <a href="/admin/users" class="card h-100 text-decoration-none border-0 bg-light">
                                    <div class="card-body text-center">
                                        <i class="fas fa-user-plus fa-2x mb-3 text-primary"></i>
                                        <h5 class="card-title">Gestión de Usuarios</h5>
                                        <p class="card-text small text-muted">Administrar usuarios y permisos</p>
                                    </div>
                                </a>
                            </div>
                            
                            <div class="col-md-3">
                                <a href="/admin/appointments" class="card h-100 text-decoration-none border-0 bg-light">
                                    <div class="card-body text-center">
                                        <i class="fas fa-calendar-alt fa-2x mb-3 text-success"></i>
                                        <h5 class="card-title">Gestión de Citas</h5>
                                        <p class="card-text small text-muted">Administrar citas y horarios</p>
                                    </div>
                                </a>
                            </div>
                            
                            <div class="col-md-3">
                                <a href="/admin/medications" class="card h-100 text-decoration-none border-0 bg-light">
                                    <div class="card-body text-center">
                                        <i class="fas fa-pills fa-2x mb-3 text-info"></i>
                                        <h5 class="card-title">Medicamentos</h5>
                                        <p class="card-text small text-muted">Gestionar catálogo de medicamentos</p>
                                    </div>
                                </a>
                            </div>
                            
                            <div class="col-md-3">
                                <a href="/admin/reports" class="card h-100 text-decoration-none border-0 bg-light">
                                    <div class="card-body text-center">
                                        <i class="fas fa-chart-line fa-2x mb-3 text-warning"></i>
                                        <h5 class="card-title">Reportes</h5>
                                        <p class="card-text small text-muted">Ver estadísticas y reportes</p>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Usuarios recientes
        users_table = """
        <div class="row">
            <div class="col-lg-12 mb-4">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-users me-2"></i> Usuarios Recientes
                        </h5>
                        <a href="/admin/users/new" class="btn btn-sm btn-primary">
                            <i class="fas fa-user-plus me-1"></i> Nuevo Usuario
                        </a>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Usuario</th>
                                        <th>Email</th>
                                        <th>Rol</th>
                                        <th>Fecha Registro</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>admin</td>
                                        <td>admin@noname.org</td>
                                        <td><span class="badge role-admin">Admin</span></td>
                                        <td>01/05/2025</td>
                                        <td>
                                            <a href="/admin/users/1/edit" class="btn btn-sm btn-outline-primary me-1"><i class="fas fa-edit"></i></a>
                                            <a href="/admin/users/1" class="btn btn-sm btn-outline-info"><i class="fas fa-eye"></i></a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>doctor</td>
                                        <td>doctor@noname.org</td>
                                        <td><span class="badge role-doctor">Doctor</span></td>
                                        <td>01/05/2025</td>
                                        <td>
                                            <a href="/admin/users/2/edit" class="btn btn-sm btn-outline-primary me-1"><i class="fas fa-edit"></i></a>
                                            <a href="/admin/users/2" class="btn btn-sm btn-outline-info"><i class="fas fa-eye"></i></a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>patient</td>
                                        <td>patient@noname.org</td>
                                        <td><span class="badge role-patient">Paciente</span></td>
                                        <td>01/05/2025</td>
                                        <td>
                                            <a href="/admin/users/3/edit" class="btn btn-sm btn-outline-primary me-1"><i class="fas fa-edit"></i></a>
                                            <a href="/admin/users/3" class="btn btn-sm btn-outline-info"><i class="fas fa-eye"></i></a>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="card-footer text-end">
                        <a href="/admin/users" class="btn btn-link btn-sm text-decoration-none">Ver todos <i class="fas fa-arrow-right ms-1"></i></a>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Contenido principal
        content = f"""
        {header}
        {stats}
        {admin_options}
        {users_table}
        """
        
        return content
        
        # Obtener la fecha y hora actual para mostrar
        from datetime import datetime
        current_date = datetime.now().strftime("%d de %B, %Y")
        
        # Contenido del dashboard mejorado con cards de estadísticas
        content = f"""
        <div class="dashboard-header mb-4">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="h3 mb-0" data-translate="dashboard">Panel de Control</h1>
                    <p class="text-muted" data-translate="welcome">¡Bienvenido, {user.username}! <span class="badge role-{user.role}">{user.role.title()}</span></p>
                    <p class="text-muted small">{current_date}</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <button class="btn btn-sm btn-outline-primary me-2">
                        <i class="fas fa-bell me-1"></i> <span class="badge bg-danger">3</span>
                    </button>
                    <button class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-cog me-1"></i> <span data-translate="settings">Configuración</span>
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Tarjetas de estadísticas -->
        <div class="dashboard-stats">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <h3>8</h3>
                <p data-translate="appointments">Citas Pendientes</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-file-medical"></i>
                </div>
                <h3>24</h3>
                <p data-translate="medicalHistory">Registros Médicos</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-pills"></i>
                </div>
                <h3>5</h3>
                <p data-translate="medications">Medicamentos Activos</p>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-heartbeat"></i>
                </div>
                <h3>98%</h3>
                <p>Estado de Salud</p>
            </div>
        </div>
        
        <!-- Contenido principal -->
        <div class="row">
            <!-- Perfil del usuario -->
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-user-circle me-2 text-primary"></i>
                            <span data-translate="profile">Tu Perfil</span>
                        </h5>
                        <div class="text-center mb-4">
                            <div class="avatar-placeholder mb-3">
                                <span>{user.username[0].upper()}</span>
                            </div>
                            <h6>{user.username}</h6>
                            <span class="badge role-{user.role}">{user.role.title()}</span>
                        </div>
                        <ul class="list-group list-group-flush mb-3">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="fas fa-envelope me-2 text-secondary"></i> Email</span>
                                <span>{user.email}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="fas fa-clock me-2 text-secondary"></i> Miembro desde</span>
                                <span>{user.created_at.strftime('%d/%m/%Y') if user.created_at else 'N/A'}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <span><i class="fas fa-shield-alt me-2 text-secondary"></i> Estado</span>
                                <span class="badge bg-success">Activo</span>
                            </li>
                        </ul>
                        <div class="d-grid">
                            <a href="#" class="btn btn-outline-primary">
                                <i class="fas fa-edit me-2"></i> Editar Perfil
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Acciones rápidas -->
            <div class="col-lg-8 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-clipboard-list me-2 text-primary"></i>
                            Acciones Rápidas
                        </h5>
                        <div class="row g-3 mb-4">
                            <div class="col-md-6">
                                <a href="#" class="quick-action-card d-block p-3 bg-light rounded text-decoration-none">
                                    <i class="fas fa-calendar-plus text-primary mb-2 d-block fs-4"></i>
                                    <h6 class="mb-1">Agendar Cita</h6>
                                    <p class="small text-muted mb-0">Programa tu próxima consulta</p>
                                </a>
                            </div>
                            <div class="col-md-6">
                                <a href="#" class="quick-action-card d-block p-3 bg-light rounded text-decoration-none">
                                    <i class="fas fa-file-prescription text-info mb-2 d-block fs-4"></i>
                                    <h6 class="mb-1">Ver Recetas</h6>
                                    <p class="small text-muted mb-0">Accede a tus recetas médicas</p>
                                </a>
                            </div>
                            <div class="col-md-6">
                                <a href="#" class="quick-action-card d-block p-3 bg-light rounded text-decoration-none">
                                    <i class="fas fa-notes-medical text-success mb-2 d-block fs-4"></i>
                                    <h6 class="mb-1">Historial Médico</h6>
                                    <p class="small text-muted mb-0">Revisa tu historial completo</p>
                                </a>
                            </div>
                            <div class="col-md-6">
                                <a href="#" class="quick-action-card d-block p-3 bg-light rounded text-decoration-none">
                                    <i class="fas fa-comment-medical text-warning mb-2 d-block fs-4"></i>
                                    <h6 class="mb-1">Mensajes</h6>
                                    <p class="small text-muted mb-0">Contacta a tu médico</p>
                                </a>
                            </div>
                        </div>
                        
                        <h6 class="mt-4 mb-3">Actividad Reciente</h6>
                        <div class="activity-feed">
                            <div class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-calendar-check"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">Cita agendada con Dr. García</div>
                                    <div class="activity-time">Hace 2 días</div>
                                </div>
                            </div>
                            <div class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-pills"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">Renovación de medicamento prescrita</div>
                                    <div class="activity-time">Hace 1 semana</div>
                                </div>
                            </div>
                            <div class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-file-medical"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">Resultados de análisis disponibles</div>
                                    <div class="activity-time">Hace 2 semanas</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return flash_html + content