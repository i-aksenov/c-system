import string

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from limit import limiter
from models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # check first letter
        prefix = password[0]
        if prefix.isdigit() or prefix in string.punctuation:
            return render_template("login.html")

        # check that password is not palindrome
        reversed_password = password[::-1]
        if password == reversed_password:
            return render_template("login.html")

        # check password length
        if not (8 <= len(password) <= 16):
            return render_template("login.html")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("main.index"))

    return render_template("login.html")


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/recover", methods=["GET", "POST"])
@limiter.limit("3 per 5 minutes")
def recover_password():
    if request.method == "POST":
        username = request.form.get("username")
        secret_answer = request.form.get("secret_answer").lower()

        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template("recover.html")

        if not user.question_answer:
            return render_template("recover.html")

        if user.question_answer.lower() == secret_answer:
            flash(f"Пароль восстановлен: {user.password}")

    return render_template("recover.html")
