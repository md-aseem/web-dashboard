from flask import Blueprint
from flask_login import login_required
from . import dash_app

dash_bp = Blueprint('dashboard', __name__)


@dash_bp.route("/")
@login_required
def render_dashboard():
    return dash_app.index()
