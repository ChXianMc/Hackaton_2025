from flask import redirect, url_for, flash, request, get_flashed_messages
from flask_login import current_user, login_required
from app import app, db
from models import User, Message
from dynamic_views import View
from datetime import datetime


@app.route('/messages')
@login_required
def view_messages():
    """Muestra los mensajes del usuario"""
    # Obtener mensajes recibidos
    received_messages = current_user.received_messages.order_by(Message.timestamp.desc()).all()
    
    # Obtener mensajes enviados
    sent_messages = current_user.sent_messages.order_by(Message.timestamp.desc()).all()
    
    # Obtener mensajes flash
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Contenido para la vista
    content = f"""
    <div class="container">
        <h1 class="mb-4">Mensajes</h1>
        
        <div class="d-flex justify-content-between align-items-center mb-4">
            <ul class="nav nav-tabs" id="messagesTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="received-tab" data-bs-toggle="tab" data-bs-target="#received" type="button" role="tab" aria-controls="received" aria-selected="true">
                        Recibidos <span class="badge bg-primary">{len([m for m in received_messages if not m.read])}</span>
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="sent-tab" data-bs-toggle="tab" data-bs-target="#sent" type="button" role="tab" aria-controls="sent" aria-selected="false">Enviados</button>
                </li>
            </ul>
            
            <a href="/messages/new" class="btn btn-primary">
                <i class="fas fa-paper-plane me-1"></i> Nuevo Mensaje
            </a>
        </div>
        
        <div class="tab-content" id="messagesTabsContent">
            <div class="tab-pane fade show active" id="received" role="tabpanel" aria-labelledby="received-tab">
                <div class="card">
                    <div class="card-body p-0">
                        <div class="list-group list-group-flush">
    """
    
    # Generar elementos para mensajes recibidos
    if received_messages:
        for message in received_messages:
            read_status = '<span class="badge bg-danger ms-2">Nuevo</span>' if not message.read else ''
            content += f"""
            <a href="/messages/{message.id}" class="list-group-item list-group-item-action {'unread' if not message.read else ''}">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">
                            <strong>{message.subject}</strong> {read_status}
                        </h6>
                        <p class="mb-1 text-muted">De: {message.sender.username}</p>
                    </div>
                    <small class="text-muted">{message.timestamp.strftime('%d/%m/%Y %H:%M')}</small>
                </div>
            </a>
            """
    else:
        content += """
        <div class="list-group-item text-center">
            <p class="mb-0 text-muted">No tienes mensajes recibidos</p>
        </div>
        """
    
    content += """
                        </div>
                    </div>
                </div>
            </div>
            <div class="tab-pane fade" id="sent" role="tabpanel" aria-labelledby="sent-tab">
                <div class="card">
                    <div class="card-body p-0">
                        <div class="list-group list-group-flush">
    """
    
    # Generar elementos para mensajes enviados
    if sent_messages:
        for message in sent_messages:
            read_status = '<span class="badge bg-success ms-2">Leído</span>' if message.read else '<span class="badge bg-secondary ms-2">No leído</span>'
            content += f"""
            <a href="/messages/{message.id}" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">
                            <strong>{message.subject}</strong> {read_status}
                        </h6>
                        <p class="mb-1 text-muted">Para: {message.recipient.username}</p>
                    </div>
                    <small class="text-muted">{message.timestamp.strftime('%d/%m/%Y %H:%M')}</small>
                </div>
            </a>
            """
    else:
        content += """
        <div class="list-group-item text-center">
            <p class="mb-0 text-muted">No tienes mensajes enviados</p>
        </div>
        """
    
    content += """
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Mensajes', content, current_user)


@app.route('/messages/new', methods=['GET', 'POST'])
@login_required
def new_message():
    """Crear un nuevo mensaje"""
    # Determinar los destinatarios disponibles según el rol
    if current_user.role == 'patient':
        # Los pacientes solo pueden enviar mensajes a los doctores
        recipients = User.query.filter_by(role='doctor').all()
    elif current_user.role == 'doctor':
        # Los doctores pueden enviar mensajes a pacientes y otros doctores
        recipients = User.query.filter(User.role.in_(['patient', 'doctor']), User.id != current_user.id).all()
    else:  # admin
        # Los administradores pueden enviar mensajes a cualquier usuario
        recipients = User.query.filter(User.id != current_user.id).all()
    
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        body = request.form.get('body')
        
        if not all([recipient_id, subject, body]):
            flash('Por favor completa todos los campos requeridos.', 'danger')
            return redirect(url_for('new_message'))
        
        try:
            # Crear nuevo mensaje
            new_msg = Message()
            new_msg.subject = subject
            new_msg.body = body
            new_msg.sender_id = current_user.id
            new_msg.recipient_id = recipient_id
            new_msg.timestamp = datetime.now()
            new_msg.read = False
            
            db.session.add(new_msg)
            db.session.commit()
            
            flash('Mensaje enviado exitosamente.', 'success')
            return redirect(url_for('view_messages'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al enviar el mensaje: {str(e)}', 'danger')
            return redirect(url_for('new_message'))
    
    # Si es GET, mostrar formulario
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Generar opciones de destinatarios
    recipient_options = ""
    for recipient in recipients:
        role_label = "" if current_user.role == 'admin' else f" (Dr.)" if recipient.role == 'doctor' else ""
        recipient_options += f'<option value="{recipient.id}">{recipient.username}{role_label}</option>'
    
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="mb-0">Nuevo Mensaje</h3>
                    </div>
                    <div class="card-body">
                        <form method="POST" action="/messages/new">
                            <div class="mb-3">
                                <label for="recipient_id" class="form-label">Destinatario</label>
                                <select class="form-select" id="recipient_id" name="recipient_id" required>
                                    <option value="" disabled selected>Selecciona un destinatario</option>
                                    {recipient_options}
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label for="subject" class="form-label">Asunto</label>
                                <input type="text" class="form-control" id="subject" name="subject" required>
                            </div>
                            
                            <div class="mb-3">
                                <label for="body" class="form-label">Mensaje</label>
                                <textarea class="form-control" id="body" name="body" rows="6" required></textarea>
                            </div>
                            
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/messages" class="btn btn-outline-secondary me-md-2">Cancelar</a>
                                <button type="submit" class="btn btn-primary">Enviar Mensaje</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Nuevo Mensaje', content, current_user)


@app.route('/messages/<int:message_id>')
@login_required
def view_message(message_id):
    """Ver un mensaje específico"""
    message = Message.query.get_or_404(message_id)
    
    # Verificar que el usuario tenga permiso para ver este mensaje
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('No tienes permiso para ver este mensaje.', 'danger')
        return redirect(url_for('view_messages'))
    
    # Marcar como leído si el usuario es el destinatario y el mensaje no ha sido leído
    if message.recipient_id == current_user.id and not message.read:
        message.read = True
        db.session.commit()
    
    # Determinar si el usuario actual es el remitente o el destinatario
    is_sender = message.sender_id == current_user.id
    
    # Preparar la vista de detalles
    # Badge de tipo de mensaje
    badge_class = "secondary" if is_sender else "primary"
    badge_text = "Enviado" if is_sender else "Recibido"
    
    # Información de remitente o destinatario
    label = "De" if not is_sender else "Para"
    username = message.sender.username if not is_sender else message.recipient.username
    
    # Fecha formateada
    formatted_date = message.timestamp.strftime('%d/%m/%Y %H:%M')
    
    # Parte inicial del contenido
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h3 class="mb-0">Mensaje</h3>
                        <span class="badge bg-{badge_class}">
                            {badge_text}
                        </span>
                    </div>
                    <div class="card-body">
                        <div class="mb-4">
                            <h5 class="border-bottom pb-2">{message.subject}</h5>
                            <p>
                                <strong>{label}:</strong> 
                                {username}
                            </p>
                            <p><strong>Fecha:</strong> {formatted_date}</p>
                        </div>
                        
                        <div class="message-body mb-4 p-3 bg-light rounded">
                            {message.body}
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
    """
    
    # Mostrar botones según el contexto
    if not is_sender:
        content += f"""
        <a href="/messages/reply/{message.id}" class="btn btn-primary me-md-2">
            <i class="fas fa-reply me-1"></i> Responder
        </a>
        """
    
    content += """
                            <a href="/messages" class="btn btn-outline-secondary">Volver</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Ver Mensaje', content, current_user)


@app.route('/messages/reply/<int:message_id>', methods=['GET', 'POST'])
@login_required
def reply_message(message_id):
    """Responder a un mensaje"""
    original_message = Message.query.get_or_404(message_id)
    
    # Verificar que el usuario sea el destinatario del mensaje original
    if original_message.recipient_id != current_user.id:
        flash('No tienes permiso para responder a este mensaje.', 'danger')
        return redirect(url_for('view_messages'))
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        body = request.form.get('body')
        
        if not all([subject, body]):
            flash('Por favor completa todos los campos requeridos.', 'danger')
            return redirect(url_for('reply_message', message_id=message_id))
        
        try:
            # Crear mensaje de respuesta
            reply = Message()
            reply.subject = subject
            reply.body = body
            reply.sender_id = current_user.id
            reply.recipient_id = original_message.sender_id
            reply.timestamp = datetime.now()
            reply.read = False
            
            db.session.add(reply)
            db.session.commit()
            
            flash('Respuesta enviada exitosamente.', 'success')
            return redirect(url_for('view_messages'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al enviar la respuesta: {str(e)}', 'danger')
            return redirect(url_for('reply_message', message_id=message_id))
    
    # Si es GET, mostrar formulario
    flashed_messages = get_flashed_messages(with_categories=True)
    
    # Preparar asunto y cuerpo para respuesta
    reply_subject = f"Re: {original_message.subject}" if not original_message.subject.startswith('Re:') else original_message.subject
    
    content = f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="mb-0">Responder Mensaje</h3>
                    </div>
                    <div class="card-body">
                        <div class="original-message p-3 bg-light rounded mb-4">
                            <p><strong>Mensaje original de {original_message.sender.username}:</strong></p>
                            <p>{original_message.body}</p>
                        </div>
                        
                        <form method="POST" action="/messages/reply/{message_id}">
                            <div class="mb-3">
                                <label for="recipient" class="form-label">Destinatario</label>
                                <input type="text" class="form-control" id="recipient" value="{original_message.sender.username}" disabled>
                            </div>
                            
                            <div class="mb-3">
                                <label for="subject" class="form-label">Asunto</label>
                                <input type="text" class="form-control" id="subject" name="subject" value="{reply_subject}" required>
                            </div>
                            
                            <div class="mb-3">
                                <label for="body" class="form-label">Mensaje</label>
                                <textarea class="form-control" id="body" name="body" rows="6" required></textarea>
                            </div>
                            
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/messages" class="btn btn-outline-secondary me-md-2">Cancelar</a>
                                <button type="submit" class="btn btn-primary">Enviar Respuesta</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return View.render_base_template('Responder Mensaje', content, current_user)