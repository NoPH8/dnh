import datetime
import zoneinfo
from functools import cached_property
from typing import Optional

from flask import current_app, render_template
from turbo_flask import Turbo

from app.logging import DashboardFIFOStream, dashboard_handler

turbo = Turbo()


class Dashboard:
    started: datetime.datetime
    records_last_updated_at: Optional[datetime.datetime] = None
    timezone: zoneinfo.ZoneInfo

    def __init__(self, app=None):
        self.app = app

    @property
    def has_logs(self) -> bool:
        return bool(self.log_stream.storage)

    @property
    def log(self):
        return self.log_stream.show()

    @property
    def log_length(self):
        return self.log_stream.MAX_SIZE

    @cached_property
    def log_stream(self):  # pragma: no cover
        handler = next(
            x for x in current_app.logger.handlers if isinstance(x.stream, DashboardFIFOStream)
        )
        return handler.stream

    @staticmethod
    def get_timezone(app):
        return zoneinfo.ZoneInfo(app.config['USER_TIMEZONE'])

    @property
    def update_interval(self):
        return current_app.config["DNS_UPDATE_INTERVAL"]

    def clear_logs(self):
        self.log_stream.clear()
        self.update_dashboard()

    def init_app(self, app):
        self.app = app
        self.timezone = self.get_timezone(app)
        self.started = datetime.datetime.now(tz=self.timezone)
        app.logger.addHandler(dashboard_handler)

        @app.context_processor
        def inject_dashboard():
            return {
                'dashboard': self,
                'datetime_format': app.config['DATETIME_FORMAT'],
            }

    def update_dashboard(self):
        with self.app.app_context():
            turbo.push(
                turbo.replace(
                    render_template('admin/dashboard.html'),
                    'dashboard',
                )
            )

    def refresh_records_last_updated_at_value(self):
        self.records_last_updated_at = datetime.datetime.now(tz=self.timezone)
        self.update_dashboard()


dashboard = Dashboard()
