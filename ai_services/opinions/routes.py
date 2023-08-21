from flask import Blueprint, request
from flask_login import login_required
from .controllers import opinions

opinions_bp = Blueprint('opinions',__name__)


@opinions_bp.route("/opinions", methods=['GET', 'POST'])
@login_required
def config_services_info():
    return opinions(request)