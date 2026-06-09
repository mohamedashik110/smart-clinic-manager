# 🏥 Smart Clinic Manager

> A production-ready Clinic Management System built on the **Frappe Framework** — featuring multi-doctor scheduling, queue management, duplicate booking prevention, REST APIs, reports, and role-based access control.

---

## 📌 Overview

Smart Clinic Manager is a full-featured clinic appointment and queue management application. It was built as an extension of a basic appointment booking app, evolving it into a robust system that can handle real-world clinic operations — multiple doctors, shifts, patient queues, and admin reporting.

---

## ✨ Features

### 🩺 Core Appointment System
- Book appointments for patients with a specific doctor, shift, date, and clinic
- Each appointment is automatically added to the correct **queue** (matched by doctor + shift + date + clinic)
- Patients receive a **queue number** on successful booking

### 👨‍⚕️ Multi-Doctor Support
- Appointments are linked to individual doctors
- Each doctor has their own independent queue per shift and date
- Doctor-wise reporting available

### 🚫 Duplicate Booking Prevention
- System checks if the same patient has already booked the same doctor on the same date and shift
- Blocks duplicate bookings with a clear error response

### 📋 Queue Management
- View and filter the appointment queue by date and shift
- Track appointment status (Booked, Ongoing, Completed)
- Queue auto-updates when new appointments are created

### 📊 Reports
- Daily appointment report — all bookings for a given date
- Doctor-wise appointment summary — total count per doctor

### 🔐 Role-Based Permissions
- **Admin** — full access to all modules and reports
- **Receptionist** — can create and manage appointments
- **Doctor** — can view their own appointment queue

### 🌐 REST API (Whitelisted Endpoints)
- All major operations are exposed as clean REST API endpoints
- Suitable for integration with external frontends or mobile apps

---

## 🗂️ Module Structure

| DocType | Description |
|---|---|
| `Appointments` | Core appointment document — patient, doctor, shift, date, clinic |
| `Appointment Queue` | Daily queue per doctor/shift/clinic |
| `Appointment Queue Item` | Individual slot in the queue with status tracking |
| `Doctor` | Doctor master data |
| `Clinic` | Clinic master data |
| `Schedule Shift` | Shift definitions (Morning, Evening, etc.) |

---

## 🌐 API Endpoints

All endpoints are Frappe whitelisted and accessible via `/api/method/`.

| Endpoint | Method | Description |
|---|---|---|
| `get_daily_appointments` | GET | Fetch all appointments for a given date |
| `get_doctor_wise_appointments` | GET | Total appointment count grouped by doctor |
| `book_appointment` | POST | Book a new appointment |
| `check_duplicate` | GET | Check if a booking already exists |
| `get_queue` | GET | Get queue filtered by date and/or shift |

### Example — Book an Appointment
```http
POST /api/method/appointments_app.api.book_appointment
Content-Type: application/json

{
  "patient_name": "John Doe",
  "doctor": "Dr. Smith",
  "shift": "Morning",
  "date": "2025-06-15",
  "clinic": "City Clinic"
}
```

### Example — Check for Duplicate
```http
GET /api/method/appointments_app.api.check_duplicate
  ?patient_name=John Doe
  &doctor=Dr. Smith
  &shift=Morning
  &date=2025-06-15
```

---

## 🏗️ Architecture

```
Patient Request
      │
      ▼
  book_appointment()   ──►  check_duplicate()
      │                          │
      │  (no duplicate)          │  (duplicate found)
      ▼                          ▼
 Appointments DocType      ❌ Error returned
      │
      ▼ (after_insert hook)
 add_to_appointment_queue()
      │
      ▼
 Appointment Queue  ──►  Queue Number assigned
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Backend logic, DocType controllers, API |
| **Frappe Framework** | App framework, ORM, permissions, REST |
| **JavaScript** | Client-side form scripts and validations |
| **MariaDB** | Database (via Frappe ORM) |
| **HTML/Jinja** | Web portal templates |

---

## ⚙️ Installation

### Prerequisites
- [Frappe Bench](https://github.com/frappe/bench) installed
- Python 3.10+
- Node.js 18+

### Steps

```bash
# 1. Go to your bench directory
cd ~/frappe-bench

# 2. Get the app
bench get-app https://github.com/mohamedashik110/smart-clinic-manager

# 3. Install on your site
bench --site your-site-name install-app appointments_app

# 4. Run migrations
bench --site your-site-name migrate

# 5. Start the server
bench start
```

---

## 🧪 Running Tests

```bash
bench --site your-site-name run-tests --app appointments_app
```

Tests are written for all major DocTypes:
- `test_appointment.py`
- `test_clinic.py`
- `test_doctor.py`
- `test_schedule_shift.py`
- `test_appointment_queue_item.py`

---

## 🔧 Development Setup

This app uses `pre-commit` for code quality. After cloning:

```bash
cd apps/appointments_app
pip install pre-commit
pre-commit install
```

Tools configured:
- **ruff** — Python linting & formatting
- **eslint** — JavaScript linting
- **prettier** — Code formatting
- **pyupgrade** — Python syntax upgrades

---

## 📁 Project Structure

```
smart-clinic-manager/
├── appointments_app/
│   ├── appointments_app/
│   │   ├── doctype/
│   │   │   ├── appointments/
│   │   │   ├── appointment_queue/
│   │   │   ├── appointment_queue_item/
│   │   │   ├── doctor/
│   │   │   ├── clinic/
│   │   │   └── schedule_shift/
│   │   └── ...
├── api.py                  # Public REST API endpoints
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

---

## 🚀 What I Learned Building This

- Frappe DocType lifecycle hooks (`after_insert`, `validate`)
- Building and exposing REST APIs with `@frappe.whitelist()`
- Role-based permission design in Frappe
- Writing unit tests in the Frappe test framework
- Duplicate prevention logic at the application layer
- Queue data structure implementation for real-world scheduling

---

## 📄 License

This project is licensed under the **MIT License** — see [license.txt](./license.txt) for details.

---

## 👤 Author

**Mohamed Ashik**
- GitHub: [@mohamedashik110](https://github.com/mohamedashik110)

---

> ⭐ If you found this project useful, consider giving it a star!

