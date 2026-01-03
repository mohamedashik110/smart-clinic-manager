# Copyright (c) 2025, Ashik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Appointments(Document):

    def validate(self):
        self.validate_required_fields()
        self.validate_doctor_shift()
        self.prevent_duplicate_booking()
        self.set_default_status()
        self.handle_queue()
    
    def validate_required_fields(self):
        required = ["patient_name", "doctor", "shift", "date", "clinic"]
        missing = [f for f in required if not self.get(f)]
        if missing:
            frappe.throw("Missing required fields: " + ", ".join(missing))

    def validate_doctor_shift(self):
        doctor = frappe.get_doc("Doctor", self.doctor)
        shifts = doctor.get("available_shifts") or []
        if not shifts:
            frappe.throw("Doctor availability not configured")

        allowed_shifts = [row.shift for row in shifts]
        if self.shift not in allowed_shifts:
            frappe.throw("Doctor not available for selected shift. Please choose another shift")
    
    def prevent_duplicate_booking(self):
        if not self.patient_name:
            return
        if frappe.db.exists(
            "Appointments",
            {
                "patient_name": self.patient_name,
                "doctor": self.doctor,
                "date": self.date,
                "shift": self.shift,
                "name": ["!=", self.name]
            }
        ):
            frappe.throw("Duplicate booking is not allowed for the same patient, doctor, date, and shift")

    def set_default_status(self):
        if self.is_new() and not self.status:
            self.status = "Booked"

    def handle_queue(self):
        if self.status != "Checked-In":
            return
        if frappe.db.exists(
            "Appointment Queue",
            {"appointments": self.name}
        ):
            return
        self.add_to_queue()

    def add_to_queue(self):
        queue_no = frappe.db.count(
            "Appointment Queue",
            {
                "date": self.date,
                "shift": self.shift,
                "status": "Ongoing"
            }
        ) + 1

        queue = frappe.get_doc({
            "doctype": "Appointment Queue",
            "date": self.date,
            "shift": self.shift,
            "clinic": self.clinic,
            "queue": queue_no,
            "appointments": self.name,
            "status": "Ongoing"
        })
        queue.insert(ignore_permissions=True)
        return queue_no

       
