from flask import Blueprint

competition_bp = Blueprint(
    'competition',
    __name__,
    url_prefix='/competition',
    template_folder='templates'
)

from . import routes
