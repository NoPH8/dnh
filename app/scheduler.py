from flask import Blueprint

from app.tasks import update_domain_ip_task

scheduler_bp = Blueprint('scheduler', __name__)


@scheduler_bp.record
def record(state):
    state.app.scheduler.add_job(
        update_domain_ip_task,
        trigger='interval',
        args=[state.app],
        minutes=state.app.config['DOMAIN_UPDATE_INTERVAL']
    )
