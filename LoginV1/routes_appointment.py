from flask import redirect, url_for, flash, request, get_flashed_messages
from flask_login import current_user, login_required
from app import app, db
from models import User, Appointment
from dynamic_views import View
from datetime import datetime, timedelta


# ---- Rutas para pacientes ----

@app.route('/appointments')
@login_required
def patient_appointments():
    """Muestra la lista de citas del paciente"""
    if current_user.role != 'patient':
        flash('Acceso denegado. No tienes permisos de paciente.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener todas las citas del paciente
    appointments = current_user.appointments_as_patient.order_by(Appointment.date).all()
    
    # Preparar datos para la plantilla
    pending_appointments = [a for a in appointments if a.date > datetime.now()]
    past_appointments = [a for a in appointments if a.date <= datetime.now()]
    
    # Obtener mensajes flash
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Contenido para la vista
    content = f"""
    <div class="container">
        <h1 class="mb-4">Mis Citas</h1>
        
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3>Citas Pendientes</h3>
            <a href="/appointments/new" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i> Agendar Nueva Cita
            </a>
        </div>
        
        <div class="card mb-5">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Hora</th>
                                <th>Médico</th>
                                <th>Motivo</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Generar filas para citas pendientes
    if pending_appointments:
        for appointment in pending_appointments:
            content += f"""
            <tr>
                <td>{appointment.date.strftime('%d/%m/%Y')}</td>
                <td>{appointment.date.strftime('%H:%M')}</td>
                <td>Dr. {appointment.doctor.username}</td>
                <td>{appointment.title}</td>
                <td><span class="badge bg-{"primary" if appointment.status == "pending" else "success" if appointment.status == "confirmed" else "secondary"}">{appointment.status.title()}</span></td>
                <td>
                    <a href="/appointments/{appointment.id}" class="btn btn-sm btn-outline-info me-1">
                        <i class="fas fa-eye"></i>
                    </a>
                    <a href="/appointments/{appointment.id}/cancel" class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-times"></i>
                    </a>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="6" class="text-center">No tienes citas pendientes</td>
        </tr>
        """
    
    content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <h3 class="mb-4">Historial de Citas</h3>
        
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Hora</th>
                                <th>Médico</th>
                                <th>Motivo</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Generar filas para citas pasadas
    if past_appointments:
        for appointment in past_appointments:
            content += f"""
            <tr>
                <td>{appointment.date.strftime('%d/%m/%Y')}</td>
                <td>{appointment.date.strftime('%H:%M')}</td>
                <td>Dr. {appointment.doctor.username}</td>
                <td>{appointment.title}</td>
                <td><span class="badge bg-{"success" if appointment.status == "completed" else "secondary"}">{appointment.status.title()}</span></td>
                <td>
                    <a href="/appointments/{appointment.id}" class="btn btn-sm btn-outline-info">
                        <i class="fas fa-eye"></i>
                    </a>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="6" class="text-center">No tienes citas en el historial</td>
        </tr>
        """
    
    content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Mis Citas', content, current_user)


@app.route('/appointments/new', methods=['GET', 'POST'])
@login_required
def new_appointment():
    """Crea una nueva cita para el paciente"""
    if current_user.role != 'patient':
        flash('Acceso denegado. No tienes permisos de paciente.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener lista de doctores disponibles
    doctors = User.query.filter_by(role='doctor').all()
    
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        title = request.form.get('title')
        notes = request.form.get('notes')
        
        if not all([doctor_id, date_str, time_str, title]):
            flash('Por favor completa todos los campos requeridos.', 'danger')
            return redirect(url_for('new_appointment'))
        
        try:
            # Combinar fecha y hora
            date_time_str = f"{date_str} {time_str}"
            appointment_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            
            # Validar que la fecha no sea en el pasado
            if appointment_date < datetime.now():
                flash('No puedes programar citas en el pasado.', 'danger')
                return redirect(url_for('new_appointment'))
            
            # Crear nueva cita
            new_appt = Appointment()
            new_appt.title = title
            new_appt.date = appointment_date
            new_appt.notes = notes
            new_appt.patient_id = current_user.id
            new_appt.doctor_id = doctor_id
            new_appt.status = 'pending'
            
            db.session.add(new_appt)
            db.session.commit()
            
            flash('¡Cita programada exitosamente! Está pendiente de confirmación.', 'success')
            return redirect(url_for('patient_appointments'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al programar la cita: {str(e)}', 'danger')
            return redirect(url_for('new_appointment'))
    
    # Si es GET, mostrar formulario
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Generar opciones de doctores
    doctor_options = ""
    for doctor in doctors:
        doctor_options += f'<option value="{doctor.id}">Dr. {doctor.username}</option>'
    
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="mb-0">Agendar Nueva Cita</h3>
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/appointments/new">
                            <div class="mb-3">
                                <label for="doctor_id" class="form-label">Médico</label>
                                <select class="form-select" id="doctor_id" name="doctor_id" required>
                                    <option value="" disabled selected>Selecciona un médico</option>
                                    {doctor_options}
                                </select>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="date" class="form-label">Fecha</label>
                                    <input type="date" class="form-control" id="date" name="date" required min="{datetime.now().strftime('%Y-%m-%d')}">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="time" class="form-label">Hora</label>
                                    <input type="time" class="form-control" id="time" name="time" required>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="title" class="form-label">Motivo de la consulta</label>
                                <input type="text" class="form-control" id="title" name="title" required>
                            </div>
                            
                            <div class="mb-3">
                                <label for="notes" class="form-label">Notas adicionales</label>
                                <textarea class="form-control" id="notes" name="notes" rows="3"></textarea>
                            </div>
                            
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/appointments" class="btn btn-outline-secondary me-md-2">Cancelar</a>
                                <button type="submit" class="btn btn-primary">Programar Cita</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Nueva Cita', content, current_user)


@app.route('/appointments/<int:appointment_id>')
@login_required
def view_appointment(appointment_id):
    """Ver detalles de una cita específica"""
    # Verificar que la cita pertenezca al usuario actual
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if current_user.role == 'patient' and appointment.patient_id != current_user.id:
        flash('No tienes permiso para ver esta cita.', 'danger')
        return redirect(url_for('patient_appointments'))
    
    if current_user.role == 'doctor' and appointment.doctor_id != current_user.id:
        flash('No tienes permiso para ver esta cita.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    # Preparar la vista de detalles
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h3 class="mb-0">Detalles de la Cita</h3>
                        <span class="badge bg-{"primary" if appointment.status == "pending" else "success" if appointment.status == "confirmed" else "secondary"}">
                            {appointment.status.title()}
                        </span>
                    </div>
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <h5>Información General</h5>
                                <p><strong>Fecha:</strong> {appointment.date.strftime('%d/%m/%Y')}</p>
                                <p><strong>Hora:</strong> {appointment.date.strftime('%H:%M')}</p>
                                <p><strong>Duración:</strong> {appointment.duration} minutos</p>
                                <p><strong>Motivo:</strong> {appointment.title}</p>
                            </div>
                            <div class="col-md-6">
                                <h5>Participantes</h5>
                                <p><strong>Paciente:</strong> {appointment.patient.username}</p>
                                <p><strong>Médico:</strong> Dr. {appointment.doctor.username}</p>
                            </div>
                        </div>
                        
                        <div class="mb-4">
                            <h5>Notas</h5>
                            <div class="p-3 bg-light rounded">
                                {appointment.notes or "No hay notas disponibles."}
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
    """
    
    # Mostrar botones según el rol y estado de la cita
    if current_user.role == 'patient':
        if appointment.status == 'pending':
            content += f"""
            <a href="/appointments/{appointment.id}/cancel" class="btn btn-danger">Cancelar Cita</a>
            """
    elif current_user.role == 'doctor':
        if appointment.status == 'pending':
            content += f"""
            <a href="/doctor/appointments/{appointment.id}/confirm" class="btn btn-success me-md-2">Confirmar</a>
            <a href="/doctor/appointments/{appointment.id}/cancel" class="btn btn-danger">Rechazar</a>
            """
        elif appointment.status == 'confirmed' and appointment.date <= datetime.now():
            content += f"""
            <a href="/doctor/appointments/{appointment.id}/complete" class="btn btn-primary">Marcar como Completada</a>
            """
    
    content += f"""
                            <a href="{'/' + ('doctor/appointments' if current_user.role == 'doctor' else 'appointments')}" class="btn btn-outline-secondary {'ms-md-2' if current_user.role == 'doctor' else ''}">Volver</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Detalles de Cita', content, current_user)


@app.route('/appointments/<int:appointment_id>/cancel')
@login_required
def cancel_patient_appointment(appointment_id):
    """Cancelar una cita como paciente"""
    if current_user.role != 'patient':
        flash('Acceso denegado. No tienes permisos de paciente.', 'danger')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verificar que la cita pertenezca al paciente
    if appointment.patient_id != current_user.id:
        flash('No tienes permiso para cancelar esta cita.', 'danger')
        return redirect(url_for('patient_appointments'))
    
    # Verificar que la cita esté pendiente o confirmada
    if appointment.status not in ['pending', 'confirmed']:
        flash('No se puede cancelar una cita que ya ha sido completada o cancelada.', 'warning')
        return redirect(url_for('patient_appointments'))
    
    try:
        appointment.status = 'cancelled'
        db.session.commit()
        flash('La cita ha sido cancelada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('patient_appointments'))


# ---- Rutas para doctores ----

@app.route('/doctor/appointments')
@login_required
def doctor_appointments():
    """Muestra la lista de citas del doctor"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener todas las citas del doctor
    appointments = current_user.appointments_as_doctor.order_by(Appointment.date).all()
    
    # Filtrar citas pendientes y pasadas
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    upcoming_appointments = [a for a in appointments if a.date.date() >= today.date()]
    past_appointments = [a for a in appointments if a.date.date() < today.date()]
    
    # Obtener mensajes flash
    flashed_messages = get_flashed_messages(with_categories=True)
    
    content = f"""
    <div class="container">
        <h1 class="mb-4">Agenda de Consultas</h1>
        
        <ul class="nav nav-tabs mb-4" id="appointmentsTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="upcoming-tab" data-bs-toggle="tab" data-bs-target="#upcoming" type="button" role="tab" aria-controls="upcoming" aria-selected="true">Próximas Citas</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="past-tab" data-bs-toggle="tab" data-bs-target="#past" type="button" role="tab" aria-controls="past" aria-selected="false">Historial</button>
            </li>
        </ul>
        
        <div class="tab-content" id="appointmentsTabsContent">
            <div class="tab-pane fade show active" id="upcoming" role="tabpanel" aria-labelledby="upcoming-tab">
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Fecha</th>
                                        <th>Hora</th>
                                        <th>Paciente</th>
                                        <th>Motivo</th>
                                        <th>Estado</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
    """
    
    # Generar filas para citas futuras
    if upcoming_appointments:
        for appointment in upcoming_appointments:
            content += f"""
            <tr>
                <td>{appointment.date.strftime('%d/%m/%Y')}</td>
                <td>{appointment.date.strftime('%H:%M')}</td>
                <td>{appointment.patient.username}</td>
                <td>{appointment.title}</td>
                <td><span class="badge bg-{"primary" if appointment.status == "pending" else "success" if appointment.status == "confirmed" else "danger" if appointment.status == "cancelled" else "secondary"}">{appointment.status.title()}</span></td>
                <td>
                    <div class="btn-group" role="group">
                        <a href="/appointments/{appointment.id}" class="btn btn-sm btn-outline-info me-1">
                            <i class="fas fa-eye"></i>
                        </a>
                        {f'<a href="/doctor/appointments/{appointment.id}/confirm" class="btn btn-sm btn-outline-success me-1"><i class="fas fa-check"></i></a>' if appointment.status == 'pending' else ''}
                        {f'<a href="/doctor/appointments/{appointment.id}/complete" class="btn btn-sm btn-outline-primary me-1"><i class="fas fa-clipboard-check"></i></a>' if appointment.status == 'confirmed' and appointment.date.date() <= datetime.now().date() else ''}
                        {f'<a href="/doctor/appointments/{appointment.id}/cancel" class="btn btn-sm btn-outline-danger"><i class="fas fa-times"></i></a>' if appointment.status in ['pending', 'confirmed'] else ''}
                    </div>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="6" class="text-center">No hay citas programadas</td>
        </tr>
        """
    
    content += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tab-pane fade" id="past" role="tabpanel" aria-labelledby="past-tab">
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Fecha</th>
                                        <th>Hora</th>
                                        <th>Paciente</th>
                                        <th>Motivo</th>
                                        <th>Estado</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
    """
    
    # Generar filas para citas pasadas
    if past_appointments:
        for appointment in past_appointments:
            content += f"""
            <tr>
                <td>{appointment.date.strftime('%d/%m/%Y')}</td>
                <td>{appointment.date.strftime('%H:%M')}</td>
                <td>{appointment.patient.username}</td>
                <td>{appointment.title}</td>
                <td><span class="badge bg-{"success" if appointment.status == "completed" else "danger" if appointment.status == "cancelled" else "secondary"}">{appointment.status.title()}</span></td>
                <td>
                    <a href="/appointments/{appointment.id}" class="btn btn-sm btn-outline-info">
                        <i class="fas fa-eye"></i>
                    </a>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="6" class="text-center">No hay citas en el historial</td>
        </tr>
        """
    
    content += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Agenda de Consultas', content, current_user)


@app.route('/doctor/appointments/<int:appointment_id>/confirm')
@login_required
def confirm_appointment(appointment_id):
    """Confirmar una cita como doctor"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verificar que la cita esté asignada al doctor actual
    if appointment.doctor_id != current_user.id:
        flash('No tienes permiso para confirmar esta cita.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    # Verificar que la cita esté pendiente
    if appointment.status != 'pending':
        flash('Solo se pueden confirmar citas pendientes.', 'warning')
        return redirect(url_for('doctor_appointments'))
    
    try:
        appointment.status = 'confirmed'
        db.session.commit()
        flash('La cita ha sido confirmada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al confirmar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('doctor_appointments'))


@app.route('/doctor/appointments/<int:appointment_id>/cancel')
@login_required
def cancel_doctor_appointment(appointment_id):
    """Cancelar una cita como doctor"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verificar que la cita esté asignada al doctor actual
    if appointment.doctor_id != current_user.id:
        flash('No tienes permiso para cancelar esta cita.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    # Verificar que la cita esté pendiente o confirmada
    if appointment.status not in ['pending', 'confirmed']:
        flash('No se puede cancelar una cita que ya ha sido completada o cancelada.', 'warning')
        return redirect(url_for('doctor_appointments'))
    
    try:
        appointment.status = 'cancelled'
        db.session.commit()
        flash('La cita ha sido cancelada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('doctor_appointments'))


@app.route('/doctor/appointments/<int:appointment_id>/complete')
@login_required
def complete_appointment(appointment_id):
    """Marcar una cita como completada"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verificar que la cita esté asignada al doctor actual
    if appointment.doctor_id != current_user.id:
        flash('No tienes permiso para completar esta cita.', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    # Verificar que la cita esté confirmada
    if appointment.status != 'confirmed':
        flash('Solo se pueden completar citas confirmadas.', 'warning')
        return redirect(url_for('doctor_appointments'))
    
    try:
        appointment.status = 'completed'
        db.session.commit()
        flash('La cita ha sido marcada como completada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al completar la cita: {str(e)}', 'danger')
    
    return redirect(url_for('doctor_appointments'))