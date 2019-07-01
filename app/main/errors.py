from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


@main.app_errorhandler(401)
def unauthorized(e):
    return render_template('error/401.html'), 401
