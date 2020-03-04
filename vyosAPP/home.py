import functools
from .vyCNTRL import RouterMGMT, vyos
import pexpect
import vymgmt

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/home')
def home():

	return render_template('home.html')
