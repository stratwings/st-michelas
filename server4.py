from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define sender and receiver email
EMAIL = "smsslg.saraswati@gmail.com"  # Replace with your email
PASSWORD = "qpls kljk cdte npag"  # Use an app password, not your normal password
TO_EMAIL = "felixfurtado809@gmail.com"  # Recipient email

app = Flask(__name__)
CORS(app, resources={r"/send-email": {"origins": "*"}})  # Allow requests from any origin

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        fname = data.get("fname", "").strip()
        lname = data.get("lname", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("Phone", "").strip()
        address = data.get("address", "").strip()
        city = data.get("city", "").strip()
        country = data.get("country", "").strip()
        zip_code = data.get("zip", "").strip()
        datepicker = data.get("data", "").strip()
        message = data.get("msg", "").strip()

        if not fname or not email:
            return jsonify({"error": "First Name and Email are required!"}), 400

        subject = "New Form Submission"
        body = f"""
        You have received a new form submission:

        First Name: {fname}
        Last Name: {lname}
        Email: {email}
        Phone: {phone}
        Address: {address}
        City: {city}
        Country: {country}
        Zip Code: {zip_code}
        Selected Date: {datepicker}
        Message: {message}
        """

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
            server.quit()
            return jsonify({"message": "Data stored successfully!"}), 200

        except smtplib.SMTPAuthenticationError as e:
            return jsonify({"error": "Authentication failed! Check email/password or enable App Passwords.", "details": str(e)}), 401
        
        except smtplib.SMTPConnectError as e:
            return jsonify({"error": "Failed to connect to the email server.", "details": str(e)}), 500
        
        except smtplib.SMTPException as e:
            return jsonify({"error": "SMTP error occurred.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5051)