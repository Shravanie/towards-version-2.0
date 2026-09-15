from flask import Flask
import mysql.connector

from config import Config
from routes.auth import auth_bp
from routes.student import student_bp
from routes.mentor import mentor_bp

app = Flask(__name__)

app.config.from_object(Config)


# Register route blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(mentor_bp)


@app.route("/")
def home():
    return "Towards Version 2.0 is running!"


@app.route("/test-db")
def test_db():

    connection = mysql.connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"],
        port=app.config["DB_PORT"]
    )

    connection.close()

    return "MySQL connection successful!"


if __name__ == "__main__":
    app.run(debug=True)