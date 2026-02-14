from flask import Flask, render_template, request, jsonify
import os
import datetime

from flask_mail import Mail, Message

app = Flask(__name__, template_folder='.')

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alert', methods=['POST'])
def receive_alert():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        message = data.get('message', 'No message provided')
        trusted_contact = data.get('trusted_contact', 'Unknown')
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{timestamp}] EMERGENCY ALERT RECEIVED!")
        print(f"Location: {latitude}, {longitude}")
        print(f"Message: {message}")
        print(f"Trusted Contact to notify: {trusted_contact}")
        print("-" * 30)
        
        # Send Email
        if trusted_contact and '@' in trusted_contact:
            try:
                msg = Message("EMERGENCY ALERT!", recipients=[trusted_contact])
                google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude and longitude else "Location not available"
                
                msg.body = f"""
                EMERGENCY ALERT triggered at {timestamp}
                
                Message: {message}
                Location: {latitude}, {longitude}
                Map: {google_maps_link}
                
                Please help immediately.
                """
                mail.send(msg)
                print(f"Email sent to {trusted_contact}")
            except Exception as e:
                print(f"Failed to send email: {e}")
                
        return jsonify({"status": "success", "message": "Alert received"}), 200
    except Exception as e:
        print(f"CRITICAL ERROR handling alert: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == '__main__':
    # SSL context is needed for Geolocation APIs on some browsers if not localhost.
    # For local dev, simple run is fine.
    app.run(debug=True, host='0.0.0.0', port=5000)
