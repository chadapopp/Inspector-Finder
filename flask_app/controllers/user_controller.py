from flask import flash, request, render_template, redirect, session, send_from_directory, abort, jsonify, json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.certification import Certification
from flask_app.models.experiences import Experiences
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

bcrypt = Bcrypt(app)
app.secret_key = 'whatever_you_want'

def get_file_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension.lower()

@app.route('/users/user_dashboard/<int:user_id>')
def user_dashboard_page(user_id):
    user_info = User.get_user_by_id(user_id)
    certs = Certification.get_user_certs(user_id)
    experiences = Experiences.get_user_experience(user_id)
    return render_template('/users/user_dashboard.html', user_info = user_info, certs = certs, experiences = experiences )

@app.route('/user/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == "POST":
        pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')  # Decode the password hash to a string
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
        }
        new_user_id = User.create_user(data)
        return redirect(f'/users/user_dashboard/{new_user_id}')
    return render_template("/login_register.html")

@app.route('/users/user_login')
def user_login_form():
    return render_template('/users/user_login.html')

@app.route('/users/login', methods=['POST'])
def login_authenticate():
    data = {"email": request.form["email"]}
    user_in_db = User.get_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'error')
        return redirect("/users/user_login")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'error')
        return redirect('/users/user_login')

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect(f"/users/user_dashboard/{user_in_db.id}")


@app.route('/users/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Check if the user is logged in
    if not session.get('user_id') or session['user_id'] != user_id:
        flash("You must be logged in to edit your profile.", 'error')
        return redirect("/users/user_login")
    
    states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
        'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
        'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
        'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
        'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
        'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
        'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ]

    if request.method == 'POST':
        actual_password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(actual_password)
        data = {
            "id": user_id,
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "phone_number": request.form['phone_number'],
            "city": request.form['city'],
            "state": request.form['state'],
            "password": pw_hash,
        }

        if "profile_picture" in request.files:
            photo = request.files["profile_picture"]
            if photo.filename != '':
                filename = secure_filename(photo.filename)
                file_path = os.path.join(app.config['UPLOAD_DIR'], filename)
                photo.save(file_path)
                data['profile_picture'] = file_path

        User.update_user(data)
        flash("Profile updated successfully!", 'success')
        return redirect(f'/users/user_dashboard/{user_id}')

    # Handle GET request
    user_info = User.get_user_by_id(user_id)
    return render_template('/users/edit_user.html', user_info=user_info, states = states)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.instance_path, "uploads"), filename, as_attachment=False)


@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):   
    User.delete_user(user_id)
    return redirect(f'/users/all_users/{session["company_id"]}')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')