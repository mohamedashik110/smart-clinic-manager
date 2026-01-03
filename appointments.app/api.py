import frappe
from frappe import _

@frappe.whitelist()
def get_daily_appointments(date=None):
    if not date:
        date = frappe.utils.getdate()

    data = frappe.db.sql("""
        SELECT patient_name, doctor, shift, date, status, clinic
        FROM `tabAppointments`
        WHERE date = %s
        ORDER BY creation DESC
    """, date, as_dict=True)

    return data


@frappe.whitelist()
def get_doctor_wise_appointments():
    data = frappe.db.sql("""
        SELECT doctor, COUNT(name) AS total
        FROM `tabAppointments`
        GROUP BY doctor
        ORDER BY total DESC
    """, as_dict=True)

    return data


@frappe.whitelist()
def book_appointment(patient_name, doctor, shift, date, clinic, status=None):
    doc = frappe.get_doc({
        "doctype": "Appointments",
        "patient_name": patient_name,
        "doctor": doctor,
        "shift": shift,
        "date": date,
        "clinic": clinic,
        "status": status or "Booked"
    })
    doc.insert(ignore_permissions=True)
    return {"message": _("Appointment booked successfully"), "appointment": doc.name}


@frappe.whitelist()
def check_duplicate(patient_name, doctor, shift, date):
    exists = frappe.db.exists("Appointments", {
        "patient_name": patient_name,
        "doctor": doctor,
        "shift": shift,
        "date": date
    })
    return {"duplicate": True if exists else False}


@frappe.whitelist()
def get_queue(date=None, shift=None):
    filters = {}
    if date:
        filters["date"] = date
    if shift:
        filters["shift"] = shift

    data = frappe.get_all("Appointment Queue",
        fields=["appointments", "queue", "status", "clinic", "date", "shift"],
        filters=filters,
        order_by="queue asc"
    )

    return data


