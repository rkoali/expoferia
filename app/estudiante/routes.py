from flask import render_template
from flask_login import login_required
from . import estudiante

@estudiante.route('/dashboard')
@login_required
def dashboard():
    return render_template('estudiante/dashboard.html')