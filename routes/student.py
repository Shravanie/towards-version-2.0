from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request,
    current_app
)

import mysql.connector

from services.analytics import calculate_analytics


student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@student_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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

        # Get student's activities
        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                category,
                frequency,
                target,
                unit,
                start_date,
                end_date,
                priority,
                status
            FROM activities
            WHERE student_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        activities = cursor.fetchall()

        # Get student's activity logs
        cursor.execute(
            """
            SELECT
                activity_logs.log_date,
                activity_logs.completed,
                activity_logs.actual_value,
                activity_logs.time_spent,
                activities.title,
                activities.category
            FROM activity_logs
            JOIN activities
                ON activity_logs.activity_id = activities.id
            WHERE activity_logs.student_id = %s
            ORDER BY activity_logs.log_date DESC
            """,
            (session["user_id"],)
        )

        logs = cursor.fetchall()

        # Calculate analytics
        analytics = calculate_analytics(logs)

        # Get mentor feedback
        cursor.execute(
            """
            SELECT
                feedback.feedback_text,
                feedback.created_at,
                activities.title AS activity_title,
                users.name AS mentor_name
            FROM feedback
            JOIN users
                ON feedback.mentor_id = users.id
            LEFT JOIN activities
                ON feedback.activity_id = activities.id
            WHERE feedback.student_id = %s
            ORDER BY feedback.created_at DESC
            """,
            (session["user_id"],)
        )

        feedback = cursor.fetchall()

        return render_template(
            "student/dashboard.html",
            name=session.get("name"),
            activities=activities,
            analytics=analytics,
            feedback=feedback
        )

    except mysql.connector.Error:

        flash(
            "Something went wrong while loading your dashboard.",
            "error"
        )

        return redirect(url_for("auth.login"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADD ACTIVITY
# =========================================================

@student_bp.route("/activities/add", methods=["GET", "POST"])
def add_activity():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "")
        frequency = request.form.get("frequency", "")
        target = request.form.get("target") or None
        unit = request.form.get("unit", "").strip()
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date") or None
        priority = request.form.get("priority", "medium")

        if not title or not category or not frequency or not start_date:

            flash(
                "Please fill in all required fields.",
                "error"
            )

            return redirect(url_for("student.add_activity"))

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

            query = """
                INSERT INTO activities
                (
                    student_id,
                    title,
                    description,
                    category,
                    frequency,
                    target,
                    unit,
                    start_date,
                    end_date,
                    priority
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    session["user_id"],
                    title,
                    description,
                    category,
                    frequency,
                    target,
                    unit,
                    start_date,
                    end_date,
                    priority
                )
            )

            connection.commit()

            flash(
                "Activity created successfully!",
                "success"
            )

            return redirect(url_for("student.dashboard"))

        except mysql.connector.Error:

            if connection:
                connection.rollback()

            flash(
                "Something went wrong while creating the activity.",
                "error"
            )

            return redirect(url_for("student.add_activity"))

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("student/add_activity.html")


# =========================================================
# VIEW ACTIVITIES
# =========================================================

@student_bp.route("/activities")
def activities():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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
            SELECT
                id,
                title,
                description,
                category,
                frequency,
                priority,
                status,
                start_date,
                end_date
            FROM activities
            WHERE student_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        activities = cursor.fetchall()

        return render_template(
            "student/activities.html",
            name=session.get("name"),
            activities=activities
        )

    except mysql.connector.Error:

        flash(
            "Unable to load your activities.",
            "error"
        )

        return render_template(
            "student/activities.html",
            name=session.get("name"),
            activities=[]
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# EDIT ACTIVITY
# =========================================================

@student_bp.route(
    "/activities/edit/<int:activity_id>",
    methods=["GET", "POST"]
)
def edit_activity(activity_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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

        # Get only this student's activity
        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                category,
                frequency,
                target,
                unit,
                start_date,
                end_date,
                priority,
                status
            FROM activities
            WHERE id = %s AND student_id = %s
            """,
            (activity_id, session["user_id"])
        )

        activity = cursor.fetchone()

        if activity is None:

            flash(
                "Activity not found.",
                "error"
            )

            return redirect(url_for("student.activities"))

        if request.method == "POST":

            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            category = request.form.get("category", "")
            frequency = request.form.get("frequency", "")
            target = request.form.get("target") or None
            unit = request.form.get("unit", "").strip()
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date") or None
            priority = request.form.get("priority", "medium")

            if not title or not category or not frequency or not start_date:

                flash(
                    "Please fill in all required fields.",
                    "error"
                )

                return redirect(
                    url_for(
                        "student.edit_activity",
                        activity_id=activity_id
                    )
                )

            cursor.execute(
                """
                UPDATE activities
                SET
                    title = %s,
                    description = %s,
                    category = %s,
                    frequency = %s,
                    target = %s,
                    unit = %s,
                    start_date = %s,
                    end_date = %s,
                    priority = %s
                WHERE id = %s AND student_id = %s
                """,
                (
                    title,
                    description,
                    category,
                    frequency,
                    target,
                    unit,
                    start_date,
                    end_date,
                    priority,
                    activity_id,
                    session["user_id"]
                )
            )

            connection.commit()

            flash(
                "Activity updated successfully!",
                "success"
            )

            return redirect(url_for("student.activities"))

        return render_template(
            "student/edit_activity.html",
            activity=activity
        )

    except mysql.connector.Error:

        if connection:
            connection.rollback()

        flash(
            "Something went wrong while updating the activity.",
            "error"
        )

        return redirect(url_for("student.activities"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# DELETE ACTIVITY
# =========================================================

@student_bp.route(
    "/activities/delete/<int:activity_id>",
    methods=["POST"]
)
def delete_activity(activity_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM activities
            WHERE id = %s AND student_id = %s
            """,
            (activity_id, session["user_id"])
        )

        connection.commit()

        if cursor.rowcount == 0:

            flash(
                "Activity not found.",
                "error"
            )

        else:

            flash(
                "Activity deleted successfully.",
                "success"
            )

        return redirect(url_for("student.activities"))

    except mysql.connector.Error:

        if connection:
            connection.rollback()

        flash(
            "Something went wrong while deleting the activity.",
            "error"
        )

        return redirect(url_for("student.activities"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# TRACK ACTIVITY
# =========================================================

@student_bp.route(
    "/activities/<int:activity_id>/track",
    methods=["GET", "POST"]
)
def track_activity(activity_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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

        # Make sure the activity belongs to the logged-in student
        cursor.execute(
            """
            SELECT *
            FROM activities
            WHERE id = %s AND student_id = %s
            """,
            (activity_id, session["user_id"])
        )

        activity = cursor.fetchone()

        if activity is None:

            flash(
                "Activity not found.",
                "error"
            )

            return redirect(url_for("student.activities"))

        if request.method == "POST":

            log_date = request.form.get(
                "log_date",
                ""
            ).strip()

            completed = request.form.get(
                "completed"
            ) == "yes"

            actual_value = request.form.get(
                "actual_value",
                "0"
            ).strip()

            time_spent = request.form.get(
                "time_spent",
                "0"
            ).strip()

            if not log_date:

                flash(
                    "Please select a date.",
                    "error"
                )

                return redirect(
                    url_for(
                        "student.track_activity",
                        activity_id=activity_id
                    )
                )

            try:

                actual_value = float(actual_value)
                time_spent = int(time_spent)

                if actual_value < 0 or time_spent < 0:
                    raise ValueError

            except ValueError:

                flash(
                    "Please enter valid progress values.",
                    "error"
                )

                return redirect(
                    url_for(
                        "student.track_activity",
                        activity_id=activity_id
                    )
                )

            # Prevent duplicate logs for the same activity/date
            cursor.execute(
                """
                SELECT id
                FROM activity_logs
                WHERE activity_id = %s
                  AND student_id = %s
                  AND log_date = %s
                """,
                (
                    activity_id,
                    session["user_id"],
                    log_date
                )
            )

            existing_log = cursor.fetchone()

            if existing_log:

                flash(
                    "You have already logged this activity for that date.",
                    "error"
                )

                return redirect(
                    url_for(
                        "student.track_activity",
                        activity_id=activity_id
                    )
                )

            # Save activity log
            cursor.execute(
                """
                INSERT INTO activity_logs
                (
                    activity_id,
                    student_id,
                    log_date,
                    completed,
                    actual_value,
                    time_spent
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    activity_id,
                    session["user_id"],
                    log_date,
                    completed,
                    actual_value,
                    time_spent
                )
            )

            connection.commit()

            flash(
                "Activity progress logged successfully!",
                "success"
            )

            return redirect(url_for("student.activities"))

        return render_template(
            "student/activity_tracking.html",
            activity=activity
        )

    except mysql.connector.Error:

        if connection:
            connection.rollback()

        flash(
            "Something went wrong while saving your progress.",
            "error"
        )

        return redirect(
            url_for(
                "student.track_activity",
                activity_id=activity_id
            )
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ACTIVITY HISTORY
# =========================================================

@student_bp.route("/activity-history")
def activity_history():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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
            SELECT
                activity_logs.id,
                activity_logs.log_date,
                activity_logs.completed,
                activity_logs.actual_value,
                activity_logs.time_spent,
                activities.title,
                activities.category,
                activities.unit
            FROM activity_logs
            JOIN activities
                ON activity_logs.activity_id = activities.id
            WHERE activity_logs.student_id = %s
            ORDER BY
                activity_logs.log_date DESC,
                activity_logs.id DESC
            """,
            (session["user_id"],)
        )

        logs = cursor.fetchall()

        return render_template(
            "student/activity_history.html",
            logs=logs
        )

    except mysql.connector.Error:

        flash(
            "Something went wrong while loading your activity history.",
            "error"
        )

        return redirect(url_for("student.dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# GROWTH ANALYTICS
# =========================================================

@student_bp.route("/growth")
def growth():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Access denied.", "error")
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

        # Get all activity logs for this student
        cursor.execute(
            """
            SELECT
                activity_logs.log_date,
                activity_logs.completed,
                activity_logs.actual_value,
                activity_logs.time_spent,
                activities.title,
                activities.category
            FROM activity_logs
            JOIN activities
                ON activity_logs.activity_id = activities.id
            WHERE activity_logs.student_id = %s
            ORDER BY activity_logs.log_date ASC
            """,
            (session["user_id"],)
        )

        logs = cursor.fetchall()

        # Calculate all analytics
        analytics = calculate_analytics(logs)

        return render_template(
            "student/growth.html",
            analytics=analytics,
            logs=logs
        )

    except mysql.connector.Error:

        flash(
            "Something went wrong while loading your growth data.",
            "error"
        )

        return redirect(url_for("student.dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()