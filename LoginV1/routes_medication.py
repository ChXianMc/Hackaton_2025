from flask import redirect, url_for, flash, request, get_flashed_messages
from flask_login import current_user, login_required
from app import app, db
from models import User, Medication
from dynamic_views import View
from datetime import datetime


# ---- Rutas para pacientes ----

@app.route('/medications')
@login_required
def patient_medications():
    """Muestra la lista de medicamentos del paciente"""
    if current_user.role != 'patient':
        flash('Acceso denegado. No tienes permisos de paciente.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener todos los medicamentos del paciente
    active_medications = current_user.medications.filter_by(active=True).all()
    inactive_medications = current_user.medications.filter_by(active=False).all()
    
    # Obtener mensajes flash
    flashed_messages = get_flashed_messages(with_categories=True)
    
    content = f"""
    <div class="container">
        <h1 class="mb-4">Mis Medicamentos</h1>
        
        <h3>Medicamentos Activos</h3>
        <div class="card mb-5">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Medicamento</th>
                                <th>Dosis</th>
                                <th>Frecuencia</th>
                                <th>Fecha Inicio</th>
                                <th>Fecha Fin</th>
                                <th>Recetado por</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Generar filas para medicamentos activos
    if active_medications:
        for medication in active_medications:
            end_date = medication.end_date.strftime('%d/%m/%Y') if medication.end_date else "No especificada"
            content += f"""
            <tr>
                <td>{medication.name}</td>
                <td>{medication.dosage}</td>
                <td>{medication.frequency}</td>
                <td>{medication.start_date.strftime('%d/%m/%Y')}</td>
                <td>{end_date}</td>
                <td>Dr. {medication.doctor.username}</td>
                <td>
                    <a href="/medications/{medication.id}" class="btn btn-sm btn-outline-info">
                        <i class="fas fa-eye"></i>
                    </a>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="7" class="text-center">No tienes medicamentos activos</td>
        </tr>
        """
    
    content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <h3>Historial de Medicamentos</h3>
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Medicamento</th>
                                <th>Dosis</th>
                                <th>Frecuencia</th>
                                <th>Fecha Inicio</th>
                                <th>Fecha Fin</th>
                                <th>Recetado por</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Generar filas para medicamentos inactivos
    if inactive_medications:
        for medication in inactive_medications:
            end_date = medication.end_date.strftime('%d/%m/%Y') if medication.end_date else "No especificada"
            content += f"""
            <tr>
                <td>{medication.name}</td>
                <td>{medication.dosage}</td>
                <td>{medication.frequency}</td>
                <td>{medication.start_date.strftime('%d/%m/%Y')}</td>
                <td>{end_date}</td>
                <td>Dr. {medication.doctor.username}</td>
                <td>
                    <a href="/medications/{medication.id}" class="btn btn-sm btn-outline-info">
                        <i class="fas fa-eye"></i>
                    </a>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="7" class="text-center">No tienes historial de medicamentos</td>
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
    
    return View.render_base_template('Mis Medicamentos', content, current_user)


@app.route('/medications/<int:medication_id>')
@login_required
def view_medication(medication_id):
    """Ver detalles de un medicamento específico"""
    medication = Medication.query.get_or_404(medication_id)
    
    # Verificar permisos según el rol
    if current_user.role == 'patient' and medication.patient_id != current_user.id:
        flash('No tienes permiso para ver este medicamento.', 'danger')
        return redirect(url_for('patient_medications'))
    
    if current_user.role == 'doctor' and medication.prescribed_by != current_user.id:
        flash('No tienes permiso para ver este medicamento.', 'danger')
        return redirect(url_for('doctor_prescriptions'))
    
    # Preparar la vista de detalles
    end_date = medication.end_date.strftime('%d/%m/%Y') if medication.end_date else "No especificada"
    status = "Activo" if medication.active else "Inactivo"
    status_class = "success" if medication.active else "secondary"
    
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h3 class="mb-0">Detalles del Medicamento</h3>
                        <span class="badge bg-{status_class}">{status}</span>
                    </div>
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <h5>Información General</h5>
                                <p><strong>Nombre:</strong> {medication.name}</p>
                                <p><strong>Dosis:</strong> {medication.dosage}</p>
                                <p><strong>Frecuencia:</strong> {medication.frequency}</p>
                                <p><strong>Fecha de inicio:</strong> {medication.start_date.strftime('%d/%m/%Y')}</p>
                                <p><strong>Fecha de finalización:</strong> {end_date}</p>
                            </div>
                            <div class="col-md-6">
                                <h5>Detalles de Prescripción</h5>
                                <p><strong>Paciente:</strong> {medication.patient.username}</p>
                                <p><strong>Médico:</strong> Dr. {medication.doctor.username}</p>
                                <p><strong>Recetado el:</strong> {medication.start_date.strftime('%d/%m/%Y')}</p>
                            </div>
                        </div>
                        
                        <div class="mb-4">
                            <h5>Instrucciones</h5>
                            <div class="p-3 bg-light rounded">
                                {medication.instructions or "No hay instrucciones específicas."}
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
    """
    
    # Mostrar botones según el rol
    if current_user.role == 'doctor' and medication.active:
        content += f"""
        <a href="/doctor/prescriptions/{medication.id}/deactivate" class="btn btn-warning me-2">Desactivar</a>
        <a href="/doctor/prescriptions/{medication.id}/edit" class="btn btn-primary me-2">Editar</a>
        """
    
    content += f"""
                            <a href="{'/' + ('doctor/prescriptions' if current_user.role == 'doctor' else 'medications')}" class="btn btn-outline-secondary">Volver</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Detalles de Medicamento', content, current_user)


# ---- Rutas para doctores ----

@app.route('/doctor/prescriptions')
@login_required
def doctor_prescriptions():
    """Muestra las recetas médicas realizadas por el doctor"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener todas las recetas realizadas por el doctor
    medications = Medication.query.filter_by(prescribed_by=current_user.id).order_by(Medication.start_date.desc()).all()
    
    # Separar medicamentos activos e inactivos
    active_medications = [m for m in medications if m.active]
    inactive_medications = [m for m in medications if not m.active]
    
    # Obtener mensajes flash
    flashed_messages = get_flashed_messages(with_categories=True)
    
    content = f"""
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Medicamentos Prescritos</h1>
            <a href="/doctor/prescriptions/new" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i> Nueva Prescripción
            </a>
        </div>
        
        <ul class="nav nav-tabs mb-4" id="prescriptionsTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="active-tab" data-bs-toggle="tab" data-bs-target="#active" type="button" role="tab" aria-controls="active" aria-selected="true">Activos</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="inactive-tab" data-bs-toggle="tab" data-bs-target="#inactive" type="button" role="tab" aria-controls="inactive" aria-selected="false">Historial</button>
            </li>
        </ul>
        
        <div class="tab-content" id="prescriptionsTabsContent">
            <div class="tab-pane fade show active" id="active" role="tabpanel" aria-labelledby="active-tab">
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Medicamento</th>
                                        <th>Dosis</th>
                                        <th>Paciente</th>
                                        <th>Inicio</th>
                                        <th>Fin</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
    """
    
    # Generar filas para medicamentos activos
    if active_medications:
        for medication in active_medications:
            end_date = medication.end_date.strftime('%d/%m/%Y') if medication.end_date else "No especificado"
            content += f"""
            <tr>
                <td>{medication.name}</td>
                <td>{medication.dosage}</td>
                <td>{medication.patient.username}</td>
                <td>{medication.start_date.strftime('%d/%m/%Y')}</td>
                <td>{end_date}</td>
                <td>
                    <div class="btn-group" role="group">
                        <a href="/medications/{medication.id}" class="btn btn-sm btn-outline-info me-1">
                            <i class="fas fa-eye"></i>
                        </a>
                        <a href="/doctor/prescriptions/{medication.id}/edit" class="btn btn-sm btn-outline-primary me-1">
                            <i class="fas fa-edit"></i>
                        </a>
                        <a href="/doctor/prescriptions/{medication.id}/deactivate" class="btn btn-sm btn-outline-warning">
                            <i class="fas fa-ban"></i>
                        </a>
                    </div>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="6" class="text-center">No hay medicamentos activos prescritos</td>
        </tr>
        """
    
    content += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tab-pane fade" id="inactive" role="tabpanel" aria-labelledby="inactive-tab">
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Medicamento</th>
                                        <th>Dosis</th>
                                        <th>Paciente</th>
                                        <th>Inicio</th>
                                        <th>Fin</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
    """
    
    # Generar filas para medicamentos inactivos
    if inactive_medications:
        for medication in inactive_medications:
            end_date = medication.end_date.strftime('%d/%m/%Y') if medication.end_date else "No especificado"
            content += f"""
            <tr>
                <td>{medication.name}</td>
                <td>{medication.dosage}</td>
                <td>{medication.patient.username}</td>
                <td>{medication.start_date.strftime('%d/%m/%Y')}</td>
                <td>{end_date}</td>
                <td>
                    <a href="/medications/{medication.id}" class="btn btn-sm btn-outline-info">
                        <i class="fas fa-eye"></i>
                    </a>
                </td>
            </tr>
            """
    else:
        content += """
        <tr>
            <td colspan="6" class="text-center">No hay historial de medicamentos prescritos</td>
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
    
    return View.render_base_template('Prescripciones Médicas', content, current_user)


@app.route('/doctor/prescriptions/new', methods=['GET', 'POST'])
@login_required
def new_prescription():
    """Crear una nueva prescripción médica"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener lista de pacientes
    patients = User.query.filter_by(role='patient').all()
    
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        name = request.form.get('name')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        instructions = request.form.get('instructions')
        
        if not all([patient_id, name, dosage, frequency]):
            flash('Por favor completa todos los campos requeridos.', 'danger')
            return redirect(url_for('new_prescription'))
        
        try:
            # Convertir fechas
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else datetime.now()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
            
            # Crear nueva prescripción
            new_med = Medication()
            new_med.name = name
            new_med.dosage = dosage
            new_med.frequency = frequency
            new_med.start_date = start_date
            new_med.end_date = end_date
            new_med.instructions = instructions
            new_med.patient_id = patient_id
            new_med.prescribed_by = current_user.id
            new_med.active = True
            
            db.session.add(new_med)
            db.session.commit()
            
            flash('Prescripción médica creada exitosamente.', 'success')
            return redirect(url_for('doctor_prescriptions'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la prescripción: {str(e)}', 'danger')
            return redirect(url_for('new_prescription'))
    
    # Si es GET, mostrar formulario
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Generar opciones de pacientes
    patient_options = ""
    for patient in patients:
        patient_options += f'<option value="{patient.id}">{patient.username}</option>'
    
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="mb-0">Nueva Prescripción Médica</h3>
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/doctor/prescriptions/new">
                            <div class="mb-3">
                                <label for="patient_id" class="form-label">Paciente</label>
                                <select class="form-select" id="patient_id" name="patient_id" required>
                                    <option value="" disabled selected>Selecciona un paciente</option>
                                    {patient_options}
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label for="name" class="form-label">Medicamento</label>
                                <input type="text" class="form-control" id="name" name="name" required>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="dosage" class="form-label">Dosis</label>
                                    <input type="text" class="form-control" id="dosage" name="dosage" required placeholder="Ej: 500mg">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="frequency" class="form-label">Frecuencia</label>
                                    <input type="text" class="form-control" id="frequency" name="frequency" required placeholder="Ej: Cada 8 horas">
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="start_date" class="form-label">Fecha de inicio</label>
                                    <input type="date" class="form-control" id="start_date" name="start_date" value="{datetime.now().strftime('%Y-%m-%d')}">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="end_date" class="form-label">Fecha de finalización (opcional)</label>
                                    <input type="date" class="form-control" id="end_date" name="end_date">
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="instructions" class="form-label">Instrucciones</label>
                                <textarea class="form-control" id="instructions" name="instructions" rows="3"></textarea>
                            </div>
                            
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/doctor/prescriptions" class="btn btn-outline-secondary me-md-2">Cancelar</a>
                                <button type="submit" class="btn btn-primary">Guardar Prescripción</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Nueva Prescripción', content, current_user)


@app.route('/doctor/prescriptions/<int:medication_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_prescription(medication_id):
    """Editar una prescripción médica existente"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    medication = Medication.query.get_or_404(medication_id)
    
    # Verificar que la receta pertenezca al doctor actual
    if medication.prescribed_by != current_user.id:
        flash('No tienes permiso para editar esta prescripción.', 'danger')
        return redirect(url_for('doctor_prescriptions'))
    
    if request.method == 'POST':
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        end_date_str = request.form.get('end_date')
        instructions = request.form.get('instructions')
        
        if not all([dosage, frequency]):
            flash('Por favor completa todos los campos requeridos.', 'danger')
            return redirect(url_for('edit_prescription', medication_id=medication_id))
        
        try:
            # Actualizar medicamento
            medication.dosage = dosage
            medication.frequency = frequency
            medication.end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
            medication.instructions = instructions
            
            db.session.commit()
            
            flash('Prescripción médica actualizada exitosamente.', 'success')
            return redirect(url_for('doctor_prescriptions'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la prescripción: {str(e)}', 'danger')
            return redirect(url_for('edit_prescription', medication_id=medication_id))
    
    # Si es GET, mostrar formulario con datos actuales
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Formatear fechas para el formulario
    start_date = medication.start_date.strftime('%Y-%m-%d')
    end_date = medication.end_date.strftime('%Y-%m-%d') if medication.end_date else ""
    
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="mb-0">Editar Prescripción Médica</h3>
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/doctor/prescriptions/{medication_id}/edit">
                            <div class="mb-3">
                                <label for="patient" class="form-label">Paciente</label>
                                <input type="text" class="form-control" id="patient" value="{medication.patient.username}" disabled>
                            </div>
                            
                            <div class="mb-3">
                                <label for="name" class="form-label">Medicamento</label>
                                <input type="text" class="form-control" id="name" value="{medication.name}" disabled>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="dosage" class="form-label">Dosis</label>
                                    <input type="text" class="form-control" id="dosage" name="dosage" value="{medication.dosage}" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="frequency" class="form-label">Frecuencia</label>
                                    <input type="text" class="form-control" id="frequency" name="frequency" value="{medication.frequency}" required>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="start_date" class="form-label">Fecha de inicio</label>
                                    <input type="date" class="form-control" id="start_date" value="{start_date}" disabled>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="end_date" class="form-label">Fecha de finalización (opcional)</label>
                                    <input type="date" class="form-control" id="end_date" name="end_date" value="{end_date}">
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="instructions" class="form-label">Instrucciones</label>
                                <textarea class="form-control" id="instructions" name="instructions" rows="3">{medication.instructions or ""}</textarea>
                            </div>
                            
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/doctor/prescriptions" class="btn btn-outline-secondary me-md-2">Cancelar</a>
                                <button type="submit" class="btn btn-primary">Guardar Cambios</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Editar Prescripción', content, current_user)


@app.route('/doctor/prescriptions/<int:medication_id>/deactivate')
@login_required
def deactivate_prescription(medication_id):
    """Desactivar una prescripción médica"""
    if current_user.role != 'doctor':
        flash('Acceso denegado. No tienes permisos de doctor.', 'danger')
        return redirect(url_for('dashboard'))
    
    medication = Medication.query.get_or_404(medication_id)
    
    # Verificar que la receta pertenezca al doctor actual
    if medication.prescribed_by != current_user.id:
        flash('No tienes permiso para desactivar esta prescripción.', 'danger')
        return redirect(url_for('doctor_prescriptions'))
    
    # Verificar que el medicamento esté activo
    if not medication.active:
        flash('Este medicamento ya está inactivo.', 'warning')
        return redirect(url_for('doctor_prescriptions'))
    
    try:
        medication.active = False
        if not medication.end_date:
            medication.end_date = datetime.now()
        db.session.commit()
        flash('Prescripción desactivada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desactivar la prescripción: {str(e)}', 'danger')
    
    return redirect(url_for('doctor_prescriptions'))