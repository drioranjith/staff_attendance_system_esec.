# Staff Attendance System

A web-based staff attendance tracking app built with Python Flask. It supports secure staff login, GPS-based location validation, OTP email verification, and CSV export for attendance records.

## Features

- Staff and admin authentication
- Staff attendance marking (requires location and OTP)
- Admin dashboard to add, view, and delete staff
- Attendance report page with date & staff filters, CSV export, and charts
- OTP email verification for staff (uses SendGrid when hosted)
- GPS validation with distance calculation
- Fully responsive (Bootstrap + Tailwind)

## Tech Stack

- Python 3.12+
- Flask
- Bootstrap 5, Tailwind CSS (frontend)
- JavaScript, jQuery, Chart.js (report visualization)
- JSON file for data storage (local/dev only)
- SendGrid API for outbound email on cloud

## Folder Structure

<img width="846" height="605" alt="123" src="https://github.com/user-attachments/assets/f69d04d7-7d13-43e0-9289-2f143d541828" />
```

## Setup & Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/yourusername/staff_attendance_system.git
   cd staff_attendance_system
   ```

2. **Create a virtualenv and install dependencies**

   ```bash
   python -m venv venv
   On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run locally**

   ```bash
   python app.py
   ## OR for cloud hosting (Render, Vercel, Heroku)
   export PORT=8000
   python app.py
   ```

4. **Access in browser**

   ```
   http://localhost:8000
   http://127.0.0.1:8000
   ```
   > Note: GPS-based attendance only works on HTTPS or localhost.( working on realtime GPS-validation )

## Deployment

- Local: Just run with python and access on localhost
- Cloud/Host: Push code to a Git repo and deploy on Render, Vercel, or similar (see respective docs).
- Use an actual database instead of JSON storage for real deployments.

## Usage

- **Staff:** Log in, validate GPS, get OTP on email, verify OTP, mark attendance (In/Out).
- **Admin:** Log in, view/add/delete staff, view/download attendance report.

## Limitations

- JSON file storage is not persistent on most cloud hosts—use SQLite, Postgres, or other DB for production.
- GPS and OTP require browser permissions and mail configuration.

## Contributing

Pull requests are welcome! For major changes, open an issue first to discus
s.

## License

This project is for educational purposes.
