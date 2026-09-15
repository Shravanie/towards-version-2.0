from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    current_app,
    request
)

import mysql.connector

from services.analytics import calculate_analytics


mentor_bp = Blueprint(
    "mentor",
    __name__,
    url_prefix="/mentor"
)


# =========================================================
# MENTOR DASHBOARD
# =========================================================

@mentor_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "mentor":
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
                users.id,
                users.name,
                users.email,

                COUNT(activity_logs.id) AS total_logs,

                COALESCE(
                    SUM(
                        CASE
                            WHEN activity_logs.completed = TRUE
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS completed_logs,

                COALESCE(
                    SUM(activity_logs.time_spent),
                    0
                ) AS total_minutes

            FROM mentor_student

            JOIN users
                ON mentor_student.student_id = users.id

            LEFT JOIN activity_logs
                ON activity_logs.student_id = users.id

            WHERE mentor_student.mentor_id = %s

            GROUP BY
                users.id,
                users.name,
                users.email

            ORDER BY users.name ASC
            """,
            (session["user_id"],)
        )

        students = cursor.fetchall()

        for student in students:

            total_logs = student["total_logs"]
            completed_logs = student["completed_logs"]

            if total_logs > 0:
                student["completion_rate"] = round(
                    (completed_logs / total_logs) * 100
                )
            else:
                student["completion_rate"] = 0

            student["total_hours"] = round(
                student["total_minutes"] / 60,
                1
            )

        return render_template(
            "mentor/dashboard.html",
            name=session.get("name"),
            students=students
        )

    except mysql.connector.Error:

        flash(
            "Something went wrong while loading the mentor dashboard.",
            "error"
        )

        return redirect(url_for("auth.login"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# STUDENT DETAIL
# =========================================================

@mentor_bp.route("/student/<int:student_id>")
def student_detail(student_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "mentor":
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

        # Make sure this student is assigned to this mentor
        cursor.execute(
            """
            SELECT
                users.id,
                users.name,
                users.email,
                users.created_at
            FROM mentor_student
            JOIN users
                ON mentor_student.student_id = users.id
            WHERE mentor_student.mentor_id = %s
              AND mentor_student.student_id = %s
            """,
            (
                session["user_id"],
                student_id
            )
        )

        student = cursor.fetchone()

        if student is None:

            flash(
                "Student not found or not assigned to you.",
                "error"
            )

            return redirect(url_for("mentor.dashboard"))

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
            (student_id,)
        )

        activities = cursor.fetchall()

        # Get student's logs
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
            (student_id,)
        )

        logs = cursor.fetchall()

        analytics = calculate_analytics(logs)

        # Get feedback
        cursor.execute(
            """
            SELECT
                feedback.id,
                feedback.feedback_text,
                feedback.created_at,
                activities.title AS activity_title
            FROM feedback
            LEFT JOIN activities
                ON feedback.activity_id = activities.id
            WHERE feedback.mentor_id = %s
              AND feedback.student_id = %s
            ORDER BY feedback.created_at DESC
            """,
            (
                session["user_id"],
                student_id
            )
        )

        feedback = cursor.fetchall()

        return render_template(
            "mentor/student_detail.html",
            student=student,
            activities=activities,
            analytics=analytics,
            feedback=feedback
        )

    except mysql.connector.Error:

        flash(
            "Something went wrong while loading the student profile.",
            "error"
        )

        return redirect(url_for("mentor.dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADD FEEDBACK
# =========================================================

@mentor_bp.route(
    "/student/<int:student_id>/feedback",
    methods=["POST"]
)
def add_feedback(student_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "mentor":
        flash("Access denied.", "error")
        return redirect(url_for("auth.login"))

    feedback_text = request.form.get(
        "feedback_text",
        ""
    ).strip()

    activity_id = request.form.get(
        "activity_id"
    ) or None

    if not feedback_text:

        flash(
            "Please enter some feedback.",
            "error"
        )

        return redirect(
            url_for(
                "mentor.student_detail",
                student_id=student_id
            )
        )

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

        # Verify that the student is assigned to this mentor
        cursor.execute(
            """
            SELECT id
            FROM mentor_student
            WHERE mentor_id = %s
              AND student_id = %s
            """,
            (
                session["user_id"],
                student_id
            )
        )

        assignment = cursor.fetchone()

        if assignment is None:

            flash(
                "You are not assigned to this student.",
                "error"
            )

            return redirect(url_for("mentor.dashboard"))

        # If an activity was selected, verify it belongs to the student
        if activity_id:

            cursor.execute(
                """
                SELECT id
                FROM activities
                WHERE id = %s
                  AND student_id = %s
                """,
                (
                    activity_id,
                    student_id
                )
            )

            activity = cursor.fetchone()

            if activity is None:

                flash(
                    "Invalid activity selected.",
                    "error"
                )

                return redirect(
                    url_for(
                        "mentor.student_detail",
                        student_id=student_id
                    )
                )

        # Save feedback
        cursor.execute(
            """
            INSERT INTO feedback
            (
                mentor_id,
                student_id,
                activity_id,
                feedback_text
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                session["user_id"],
                student_id,
                activity_id,
                feedback_text
            )
        )

        connection.commit()

        flash(
            "Feedback added successfully!",
            "success"
        )

        return redirect(
            url_for(
                "mentor.student_detail",
                student_id=student_id
            )
        )

    except mysql.connector.Error:

        if connection:
            connection.rollback()

        flash(
            "Something went wrong while adding feedback.",
            "error"
        )

        return redirect(
            url_for(
                "mentor.student_detail",
                student_id=student_id
            )
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# EDIT FEEDBACK
# =========================================================

@mentor_bp.route(
    "/feedback/<int:feedback_id>/edit",
    methods=["POST"]
)
def edit_feedback(feedback_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "mentor":
        flash("Access denied.", "error")
        return redirect(url_for("auth.login"))

    feedback_text = request.form.get(
        "feedback_text",
        ""
    ).strip()

    if not feedback_text:
        flash(
            "Feedback cannot be empty.",
            "error"
        )
        return redirect(url_for("mentor.dashboard"))

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

        # Verify that this feedback belongs to the logged-in mentor
        cursor.execute(
            """
            SELECT
                id,
                student_id
            FROM feedback
            WHERE id = %s
              AND mentor_id = %s
            """,
            (
                feedback_id,
                session["user_id"]
            )
        )

        feedback = cursor.fetchone()

        if feedback is None:

            flash(
                "Feedback not found or access denied.",
                "error"
            )

            return redirect(
                url_for("mentor.dashboard")
            )

        # Update feedback
        cursor.execute(
            """
            UPDATE feedback
            SET feedback_text = %s
            WHERE id = %s
              AND mentor_id = %s
            """,
            (
                feedback_text,
                feedback_id,
                session["user_id"]
            )
        )

        connection.commit()

        flash(
            "Feedback updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "mentor.student_detail",
                student_id=feedback["student_id"]
            )
        )

    except mysql.connector.Error:

        if connection:
            connection.rollback()

        flash(
            "Something went wrong while updating feedback.",
            "error"
        )

        return redirect(
            url_for("mentor.dashboard")
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# DELETE FEEDBACK
# =========================================================

@mentor_bp.route(
    "/feedback/<int:feedback_id>/delete",
    methods=["POST"]
)
def delete_feedback(feedback_id):

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("auth.login"))

    if session.get("role") != "mentor":
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

        # Verify ownership and get student ID
        cursor.execute(
            """
            SELECT
                id,
                student_id
            FROM feedback
            WHERE id = %s
              AND mentor_id = %s
            """,
            (
                feedback_id,
                session["user_id"]
            )
        )

        feedback = cursor.fetchone()

        if feedback is None:

            flash(
                "Feedback not found or access denied.",
                "error"
            )

            return redirect(
                url_for("mentor.dashboard")
            )

        # Delete feedback
        cursor.execute(
            """
            DELETE FROM feedback
            WHERE id = %s
              AND mentor_id = %s
            """,
            (
                feedback_id,
                session["user_id"]
            )
        )

        connection.commit()

        flash(
            "Feedback deleted successfully!",
            "success"
        )

        return redirect(
            url_for(
                "mentor.student_detail",
                student_id=feedback["student_id"]
            )
        )

    except mysql.connector.Error:

        if connection:
            connection.rollback()

        flash(
            "Something went wrong while deleting feedback.",
            "error"
        )

        return redirect(
            url_for("mentor.dashboard")
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()