from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# it is way to secure and compare passwords
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
# this func will run whenever we go to "/login" root
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # finding information about user
        user = User.query.filter_by(email=email).first()

        # after server finds user we must check if
        # input password is correct for this user
        if user:
            # this function is checking passwords
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                # server going to remember that this user is logged in
                # and user don't need to log in every single time he
                # goes on the website until user clears browser history
                # or server restarts
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
# checking if user logs in
@login_required
# this func will run whenever we go to "/logout" root
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
# this func will run whenever we go to "/sign-up" root
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email is already exists.", category="error")
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # after successfully sign up server redirects user to home page
            # I can just use /home but if I change home url I must change this redirect too
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
