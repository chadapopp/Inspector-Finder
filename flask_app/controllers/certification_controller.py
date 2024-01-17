from flask import flash, request, render_template, redirect, session, send_from_directory, abort, jsonify, json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.certification import Certification
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

@app.route('/certs/add_cert/<int:user_id>', methods=['GET', 'POST'])
def add_cert(user_id):
    # Check if the user is logged in
    if not session.get('user_id') or session['user_id'] != user_id:
        flash("You must be logged in to add a cert.", 'error')
        return redirect("/users/user_login")

    if request.method == 'POST':
        cert_data = {
            "user_id": user_id,
            "certification_expiration_date": request.form['certification_expiration_date'],
            "certification_number": request.form['certification_number']
        }

        result = Certification.add_cert(cert_data)

        if result:
            flash("Cert added successfully!", 'success')
        else:
            flash("Failed to add cert.", 'error')

        return redirect(f'/users/user_dashboard/{user_id}')

    # Handle GET request
    user_info = User.get_user_by_id(user_id)
    return render_template('/users/add_cert.html', user_info=user_info)

