from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models.user import User
from app.auth.forms import LoginForm, RegistrationForm
from app import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.rol == 'administrador':
                return redirect(url_for('admin.dashboard'))
            elif user.rol == 'profesor':
                return redirect(url_for('profesor.dashboard'))
            else:
                return redirect(url_for('estudiante.dashboard'))
        
        flash('Email o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            rol='estudiante'
        )
        user.password = form.password.data
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario. Por favor intente nuevamente.', 'error')
            
    return render_template('auth/register.html', form=form)