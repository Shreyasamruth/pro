from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemedicine.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'  # Secret key for JWT token
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'

# Initialize instances
db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

# Database Models

# Patient Model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)


appointments = db.relationship('Appointment', backref='patient', lazy=True)

# Doctor Model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    available_slots = db.relationship('AvailableSlot', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

# Available Slot Model (Doctor's available time slots)
class AvailableSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Scheduled')  # Scheduled, Completed, Canceled

# Notification Model (for sending reminders)
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes

# Patient Registration Route
@app.route('/register_patient', methods=['POST'])
def register_patient():
    data = request.get_json()
    new_patient = Patient(name=data['name'], age=data['age'], medical_history=data.get('medical_history', ''), email=data['email'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient registered successfully!"}), 201

# Doctor Registration Route
@app.route('/register_doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()
    new_doctor = Doctor(name=data['name'], specialty=data['specialty'])
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({"message": "Doctor registered successfully!"}), 201

# Login Route (Doctor or Patient)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_type = data.get("user_type")  # 'patient' or 'doctor'
    username = data['username']
    password = data['password']  # For simplicity, we assume no password hash in this example.

    if user_type == "patient":
        patient = Patient.query.filter_by(email=username).first()
        if patient:  # Add your password check here
            access_token = create_access_token(identity=patient.id)
            return jsonify(access_token=access_token)
        return jsonify({"message": "Invalid patient credentials!"}), 401

    elif user_type == "doctor":
        doctor = Doctor.query.filter_by(name=username).first()
        if doctor:  # Add your password check here
            access_token = create_access_token(identity=doctor.id)
            return jsonify(access_token=access_token)
        return jsonify({"message": "Invalid doctor credentials!"}), 401

    return jsonify({"message": "Invalid user type!"}), 400

# Schedule an Appointment Route
@app.route('/schedule_appointment', methods=['POST'])
@jwt_required()
def schedule_appointment():
    data = request.get_json()
    patient_id = data['patient_id']
    doctor_id = data['doctor_id']
    appointment_time = datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M:%S')

    # Check if the doctor is available at the requested time
    available_slots = AvailableSlot.query.filter_by(doctor_id=doctor_id).all()
    is_available = any(slot.start_time <= appointment_time <= slot.end_time for slot in available_slots)

    if not is_available:
        return jsonify({"message": "The doctor is not available at this time."}), 400

    new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_time=appointment_time)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment scheduled successfully!"}), 201

# Get Appointments for a Patient
@app.route('/get_appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    patient_id = request.args.get('patient_id')
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    appointments_list = []
    for appointment in appointments:
        appointments_list.append({
            "doctor": appointment.doctor.name,
            "specialty": appointment.doctor.specialty,
            "appointment_time": appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            "status": appointment.status
        })
    return jsonify(appointments_list)

# Send Appointment Reminder Notifications
@app.route('/send_appointments_reminder', methods=['POST'])
@jwt_required()
def send_appointments_reminder():
    data = request.get_json()
    patient_id = data['patient_id']
    appointment_id = data['appointment_id']

    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment or appointment.patient_id != patient_id:
        return jsonify({"message": "Appointment not found for this patient!"}), 404

    time_left = appointment.appointment_time - datetime.utcnow()
    if time_left > timedelta(hours=1):
        reminder_message = f"Reminder: You have an appointment with Dr. {appointment.doctor.name} at {appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S')}"
        new_notification = Notification(patient_id=patient_id, message=reminder_message)
        db.session.add(new_notification)
        db.session.commit()

        send_email(patient_id, reminder_message)
        return jsonify({"message": "Reminder sent successfully!"})

    return jsonify({"message": "Appointment is too close to send a reminder."}), 400

# Function to send email reminder
def send_email(patient_id, message):
    patient = Patient.query.get(patient_id)
    msg = Message("Appointment Reminder", sender="your-email@gmail.com", recipients=[patient.email])
    msg.body = message
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

# Initialize the database - Ensure this method works correctly
#@app.before_first_request
def create_tables():
    print("Initializing the database...")
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=False)
    app.run(port=5001)
