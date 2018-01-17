from flask import render_template

from .front import front
from .admin import admin
from .user import user
from .company import company
from .job import job


def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(company)
    app.register_blueprint(job)

def register_errors(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def permisson_denied(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

