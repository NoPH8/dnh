from flask import Blueprint

from app.api.v1.views import api_v1

api_bp = Blueprint('api', __name__, url_prefix='/api')
api_bp.register_blueprint(api_v1)
