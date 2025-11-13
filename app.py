# app.py
import os, json, datetime
from flask import Flask, render_template, request, redirect, jsonify, session, url_for, flash
from functools import wraps
import gps
import mail
from datetime import datetime, timedelta, timezone, date

app = Flask(__name__)
app.secret_key = "super-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ATTEND_FILE = os.path.join(DATA_DIR, "attendance.json")

os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([
            {"id": "A001", "name": "admin", "role": "admin", "password": "admin"},
            {"id": "S001", "name": "staff1", "role": "staff", "email": "test@gmail.com", "password": "1234"},
        ], f, indent=2)

if not os.path.exists(ATTEND_FILE):
    with open(ATTEND_FILE, "w") as f:
        json.dump([], f, indent=2)

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("login"))
            if role and session["user"]["role"] != role:
                return redirect(url_for("logout"))
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route("/")
def index():
    if "user" in session:
        if session["user"]["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("staff_dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form.get("userid")
        pwd = request.form.get("password")

        users = read_json(USERS_FILE)
        user = next((u for u in users if (u["id"] == uid or u["name"] == uid) and u["password"] == pwd), None)

        if user:
            session["user"] = user
            return redirect(url_for("admin_dashboard") if user["role"] == "admin" else url_for("staff_dashboard"))

        flash("Invalid Login", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------- GPS API --------
@app.route("/validate_gps", methods=["POST"])
@login_required("staff")
def validate_gps():
    data = request.get_json()
    lat = float(data.get("lat"))
    lng = float(data.get("lng"))

    valid, distance = gps.is_inside_allowed_area(lat, lng)

    return jsonify({
        "success": valid,
        "distance": distance,
        "message": "Inside allowed area" if valid else f"Outside area by {distance:.2f} meters"
    })

# -------- Staff Dashboard --------
@app.route("/staff")
@login_required("staff")
def staff_dashboard():
    return render_template("staff_dashboard.html")

# -------- OTP --------
@app.route("/send_otp", methods=["POST"])
@login_required("staff")
def send_otp():
    otp = str(mail.generate_otp())
    # Store OTP with expiry for security
    session["otp"] = {
        "value": otp,
        "expires": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()

    }
    user_email = session["user"].get("email", "test@gmail.com")
    mail.send_otp_email(user_email, otp)
    return jsonify({"message": "OTP Sent Successfully"})

@app.route("/verify_otp", methods=["POST"])
@login_required("staff")
def verify_otp():
    entered = request.form.get("otp")
    otp_obj = session.get("otp")
    if not otp_obj or "value" not in otp_obj or "expires" not in otp_obj:
        return jsonify({"success": False, "message": "OTP not found/expired"})
    # Expiry check
    if datetime.now(timezone.utc) > datetime.fromisoformat(otp_obj["expires"]):
        return jsonify({"success": False, "message": "OTP expired"})
    
    if str(entered) == str(otp_obj["value"]):
        session["otp_verified"] = True
        return jsonify({"success": True, "message": "OTP verified"})
    return jsonify({"success": False, "message": "Invalid OTP"})

# -------- Attendance --------
@app.route("/mark_attendance", methods=["POST"])
@login_required("staff")
def mark_attendance():
    if not session.get("otp_verified"):
        return jsonify({"message": "OTP not verified"}), 400

    data = request.get_json()
    gps_loc = data.get("gps_location")
    if not gps_loc:
        return jsonify({"message": "GPS location missing"}), 400

    valid, distance = gps.is_inside_allowed_area(gps_loc["lat"], gps_loc["lng"])
    if not valid:
        return jsonify({"message": f"Outside allowed area ({distance}m)"}), 403

    records = read_json(ATTEND_FILE)
    today = datetime.now().date().isoformat()
    staff = session["user"]["id"]

    # Find existing record
    existing_record = next((r for r in records if r["staff_id"] == staff and r["date"] == today), None)

    def format_time(t):
        if not t:
            return ""
        # parse an input time in "HH:MM:SS" or "HH:MM:SS AM/PM"
        try:
            # Try to parse 24hr time
            dt_obj = datetime.strptime(t, "%H:%M:%S")
        except ValueError:
            try:
                # Try to parse 12hr time with AM/PM
                dt_obj = datetime.strptime(t, "%I:%M:%S %p")
            except ValueError:
                # If parsing fails, store as is
                return t
        # convert to desired format like "3:16:29 PM"
        return dt_obj.strftime("%I:%M:%S %p").lstrip("0")

    in_time = format_time(data.get("in_time"))
    out_time = format_time(data.get("out_time"))

    if existing_record:
        if in_time:
            existing_record["in_time"] = in_time
        if out_time:
            existing_record["out_time"] = out_time
        existing_record["distance"] = distance
    else:
        new_record = {
            "staff_id": staff,
            "date": today,
            "in_time": in_time,
            "out_time": out_time,
            "distance": distance
        }
        records.append(new_record)

    write_json(ATTEND_FILE, records)
    session["otp_verified"] = False

    return jsonify({"message": "Attendance Marked"})


# -------- Admin --------
@app.route("/admin")
@login_required("admin")
def admin_dashboard():
    users = read_json(USERS_FILE)
    return render_template("admin_dashboard.html", users=users)

@app.route("/attendance_report", methods=["GET"])
@login_required("admin")
def attendance_report():
    data = read_json(ATTEND_FILE)
    date_filter = request.args.get("date")
    staff_filter = request.args.get("staff_id")
    in_time_filter = request.args.get("in_time_marked")
    out_time_filter = request.args.get("out_time_marked")

    if date_filter:
        data = [r for r in data if r["date"] == date_filter]
    if staff_filter:
        data = [r for r in data if staff_filter.lower() in r["staff_id"].lower()]

    if in_time_filter == "true":
        data = [r for r in data if r.get("in_time")]

    if out_time_filter == "true":
        data = [r for r in data if r.get("out_time")]

    return render_template(
        "attendance_report.html", attendance_data=data, current_year=datetime.datetime.now().year
    )
@app.route("/admin/add_staff", methods=["POST"])
@login_required("admin")
def add_staff():
    users = read_json(USERS_FILE)
    data = request.form.to_dict()

    new_staff = {
        "id": data.get("id") or f"S{len(users) + 1:03}",  # Generate if empty
        "name": data.get("name"),
        "phone": data.get("phone"),
        "email": data.get("email"),
        "role": "staff",
        "password": data.get("password") or "1234"
    }

    # Basic validation example
    if not new_staff["name"] or not new_staff["phone"] or not new_staff["email"]:
        flash("Name, phone, and email are required", "danger")
        return redirect(url_for("admin_dashboard"))

    users.append(new_staff)
    write_json(USERS_FILE, users)

    flash("Staff added successfully", "success")
    return redirect(url_for("admin_dashboard"))
@app.route("/admin/delete_staff/<staff_id>", methods=["POST"])
@login_required("admin")
def delete_staff(staff_id):
    users = read_json(USERS_FILE)
    # Remove the user with the given staff_id
    users = [u for u in users if u["id"] != staff_id]
    write_json(USERS_FILE, users)
    flash("Staff deleted successfully", "success")
    return redirect(url_for("admin_dashboard"))

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

