from flask import flash, request, render_template, redirect, session, send_from_directory, abort, jsonify, json
from flask_app import app
from flask_app.models.user import User
from flask_app.models.experiences import Experiences
import os


@app.route('/experiences/add_experience/<int:user_id>', methods=['GET', 'POST'])
def add_experience(user_id):
    # Check if the user is logged in
    if not session.get('user_id') or session['user_id'] != user_id:
        flash("You must be logged in to add experience.", 'error')
        return redirect("/users/user_login")

    if request.method == 'POST':
        ongoing = request.form.get('ongoing')
        experience_data = {
            "user_id": user_id,
            "position": request.form['position'],
            "company_name": request.form['company_name'],
            "description": request.form['description'],
            "start_date": request.form['start_date'],
            "end_date": None if ongoing else request.form['end_date']
        }
        result = Experiences.add_experience(experience_data)

        if result:
            flash("Experience added successfully!", 'success')
        else:
            flash("Failed to add experience.", 'error')

        return redirect(f'/users/user_dashboard/{user_id}')

    # Handle GET request
    user_info = User.get_user_by_id(user_id)
    return render_template('/experiences/add_experience.html', user_info=user_info)


@app.route('/experiences/edit/<int:experience_id>', methods=['GET'])
def edit_experience(experience_id):
    # Retrieve the experience by ID
    experience = Experiences.get_experience_by_id(experience_id)

    # Render the edit page with the experience data
    return render_template('/experiences/edit_experience.html', experience=experience)
