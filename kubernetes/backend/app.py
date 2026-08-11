from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection
db_config = {
    "host": "mysql-service",
    "user": "myuser",
    "password": "MyPassword@123",
    "database": "myapp"
}


# Home page
@app.route("/")
def home():
    return "Hello from Python"


# Contact API
@app.route("/contact", methods=["POST"])
def contact():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({
            "error": "name, email and message are required"
        }), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = """
        INSERT INTO messages (name, email, message)
        VALUES (%s, %s, %s)
        """

        values = (name, email, message)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Contact saved successfully"
        }), 201

    except mysql.connector.Error as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
