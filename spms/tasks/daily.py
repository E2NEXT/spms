

import frappe
from datetime import datetime, timedelta


def print_hello():
    print("every min scheduler works")
    
    
def calculate_overtime_and_create_salary_doc():
    # Get all employees
    employees = frappe.db.get_list('Employee',
        filters={
            'custom_employee_type': ["!=", "Salesperson"],
            'status': 'Active'
        },
        fields=["name", "company"],
    )
    
    # Get overtime salary component from SPMS settings
    overtime_component = frappe.db.get_single_value('SPMS Settings', 'overtime_salary_component')
    
    if not overtime_component:
        frappe.throw("Overtime salary component not found in SPMS Settings")
    
    # Iterate through each employee
    for employee in employees:
        # Get employee check-in documents for today
        checkin_documents = frappe.db.get_list("Employee Checkin", filters={"employee": employee.name, "time": datetime.today()}, fields=["time"])
        
        if len(checkin_documents) >= 2:
            # Get the check-in times
            frappe.msgprint(f"two logs founded for empolyee{employee.name}")
            checkin_time1 = checkin_documents[0]["time"]
            checkin_time2 = checkin_documents[1]["time"]

            # Calculate the working hours
            working_hours = abs(checkin_time2 - checkin_time1)

            # Define the standard work hour variable (in seconds)
            standard_work_hour = 8 * 60 * 60  # Assuming 8 hours as standard work hour
            standard_work_hour += 30 * 60  # Adding 30 minutes as buffer

            # If working hours exceed the standard work hour
            if working_hours > standard_work_hour:
                frappe.msgprint(working_hours)
                # Create additional salary document
                salary_doc = frappe.get_doc({
                    "doctype": "Additional Salary",
                    "employee": employee.name,
                    "company": employee.company,
                    "payroll_date": datetime.today(),
                    "salary_component": overtime_component,
                    "amount": 10000  # 10000 IQD as additional salary for overtime
                })
                salary_doc.insert()
        else:
            frappe.msgprint(f"No or insufficient check-in records found for employee {employee.name} today")
            frappe.throw(f"cannot complete the operation - {len(checkin_documents)}")
