import os

from flask import Flask, flash, redirect, render_template, request, session, url_for

from database.db import create_user, get_db, get_user_by_email, get_user_by_email_with_password, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", name="", email="", error=None)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", name=name, email=email, error="Name is required.")

    if "@" not in email or "." not in email.split("@")[-1]:
        return render_template("register.html", name=name, email=email, error="Please enter a valid email address.")

    if len(password) < 8:
        return render_template("register.html", name=name, email=email, error="Password must be at least 8 characters.")

    if get_user_by_email(email):
        return render_template("register.html", name=name, email=email, error="An account with this email already exists.")

    create_user(name, email, password)
    flash("Account created successfully! Please sign in.")
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        flash("Email address is required.")
        return render_template("login.html", email="", error="Email address is required.")

    if not password:
        flash("Password is required.")
        return render_template("login.html", email=email, error="Password is required.")

    user = get_user_by_email_with_password(email, password)
    if user:
        # Store user info in session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        flash("Logged in successfully!")
        return redirect(url_for("landing"))
    else:
        flash("Invalid email or password.")
        return render_template("login.html", email=email, error="Invalid email or password.")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
