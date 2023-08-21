from flask import Blueprint
from flask_login import login_required
from .controllers import config_services_info_controller, config_services_list_controller, config_services_grid_controller

services = Blueprint('services_info',__name__)


@services.route("/config/services/info", methods=['GET', 'POST'])
@login_required
def config_services_info():
    return config_services_info_controller()

@services.route("/config/services", methods=['GET', 'POST'])
@login_required
def config_services_list():
    return config_services_list_controller()


@services.route("/config", methods=['GET', 'POST'])
@login_required
def config_services_grid():
    return config_services_grid_controller()

