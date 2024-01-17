from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

from flask import session

@app.route('/')
def main_page():
    user_info = None  # Set user_info to None by default

    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        user_info = User.get_user_by_id(user_id)

    return render_template('/welcome.html', user_info=user_info)
