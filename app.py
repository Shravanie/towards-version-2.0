from flask import Flask
import mysql.connector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


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