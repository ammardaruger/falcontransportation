from flask import Flask, render_template, send_file, request, jsonify
from utils.email_configs import send_contact_email
import asyncio
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "app/templates"),
    static_folder=os.path.join(BASE_DIR, "app/static"),
    static_url_path="/static",
)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/old")
def old_home():
    return render_template("homeold.html")


@app.route("/catalog")
def catalog():
    return render_template("pdfContent.html")


@app.route("/catalog.json")
def get_catalog():
    return send_file(
        os.path.join(BASE_DIR, "app/static/catalog.json"),
        mimetype="application/json"
    )


@app.route("/catalog.pdf")
def get_pdf():
    return send_file(
        os.path.join(BASE_DIR, "app/static/catalog.pdf"),
        mimetype="application/pdf"
    )


@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json(silent=True)

        if data:
            name = data.get("name", "")
            email = data.get("email", "")
            note = data.get("note", "")
        else:
            name = request.form.get("name", "")
            email = request.form.get("email", "")
            note = request.form.get("note", "")

        if not name or not email or not note:
            return jsonify({
                "success": False,
                "message": "Please complete all required fields."
            }), 400

        result = asyncio.run(
            send_contact_email(
                user_name=name,
                user_email=email,
                user_message=note
            )
        )

        return jsonify(result)

    except Exception:
        return jsonify({
            "success": False,
            "message": "An error occurred while sending your message."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)