from flask import Blueprint, request, redirect, url_for, flash, render_template, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        if not name or not email or not password or not role:
            flash("Please fill in all the fields.", "error")
            return redirect(url_for("auth.register"))

        if role not in ["student", "mentor"]:
            flash("Please select a valid role.", "error")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for("auth.register"))

        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=current_app.config["DB_HOST"],
                user=current_app.config["DB_USER"],
                password=current_app.config["DB_PASSWORD"],
                database=current_app.config["DB_NAME"],
                port=current_app.config["DB_PORT"]
            )

            cursor = connection.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                flash(
                    "An account with this email already exists.",
                    "error"
                )
                return redirect(url_for("auth.register"))

            password_hash = generate_password_hash(password)

            query = """
                INSERT INTO users
                (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (name, email, password_hash, role)
            )

            connection.commit()

            flash(
                "Registration successful! Your account has been created.",
                "success"
            )

            return redirect(url_for("auth.register"))

        except mysql.connector.Error:

            if connection:
                connection.rollback()

            flash(
                "Something went wrong while creating your account.",
                "error"
            )

            return redirect(url_for("auth.register"))

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash(
                "Please enter your email and password.",
                "error"
            )
            return redirect(url_for("auth.login"))

        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=current_app.config["DB_HOST"],
                user=current_app.config["DB_USER"],
                password=current_app.config["DB_PASSWORD"],
                database=current_app.config["DB_NAME"],
                port=current_app.config["DB_PORT"]
            )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT id, name, email, password_hash, role
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

            if user is None:
                flash(
                    "Invalid email or password.",
                    "error"
                )
                return redirect(url_for("auth.login"))

            if not check_password_hash(
                user["password_hash"],
                password
            ):
                flash(
                    "Invalid email or password.",
                    "error"
                )
                return redirect(url_for("auth.login"))

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            flash("Login successful!", "success")

            if user["role"] == "student":
                return redirect(url_for("student.dashboard"))

            return redirect(url_for("mentor.dashboard"))

        except mysql.connector.Error:

            flash(
                "Something went wrong while logging in.",
                "error"
            )

            return redirect(url_for("auth.login"))

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))