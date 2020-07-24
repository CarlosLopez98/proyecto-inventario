from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
#from flask_login import login_user, logout_user, login_required, current_user
#from . import login_manager

page = Blueprint('page', __name__)


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@page.route('/')
def index():
    return render_template('index.html', title='Inicio')
