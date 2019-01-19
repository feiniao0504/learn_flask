from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db


bp = Blueprint('blog', __name__, url_prefix='/')

@bp.route("/")
def index():
    return render_template("blog/index.html")
