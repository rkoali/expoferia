from flask import render_template
from flask_login import login_required
from . import profesor

@profesor.route('/dashboard')
@login_required
def dashboard():
    return render_template('profesor/dashboard.html')