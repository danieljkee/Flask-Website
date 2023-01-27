# this file is going to store
# all of main views or the
# url endpoints for functioning
# of front-end aspect of website

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
# checking if user logs in
@login_required
# this func will run whenever we go to "/" root
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
# it is going to look for the note id that was sent to server
def delete_note():
    # it is going to take the request data from post request
    # and turn this information into python dictionary object
    note = json.loads(request.data)
    noteId = note['noteId']
    # finding this note from database
    note = Note.query.get(noteId)
    # checking if this note exists
    if note:
        # checking if this logged-in user owns this note
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    # returning an empty response
    return jsonify({})
