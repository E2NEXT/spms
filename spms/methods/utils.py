import qrcode
import frappe
from frappe.utils import cstr
from random import randint
from datetime import date

from frappe import _

@frappe.whitelist()
def get_base_url():
    return frappe.utils.get_url()

@frappe.whitelist()
def current_site_name():
    return cstr(frappe.local.site)


def generate_qrcode(site_name, route_name):
    """
    It generates a QR code image and saves it to the public folder of the site

    :param site_name: The name of the site
    :param route_name: The name of the route you want to generate a QR code for
    :return: The path to the file.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(f'{site_name}/{route_name}')

    file_name = f'{randint(1, 100000)}-{date.today()}'
    img = qr.make_image(fill_color="black", back_color="white")

    current_site_name = cstr(frappe.local.site)
    img.save(f"{current_site_name}/public/files/{file_name}.png")

    return f"/files/{file_name}.png"


def update_doctor_productivity(visiting, operation):
    """
    It updates the doctor's productivity table with the visit count and the operation count

    :param visiting: The visiting object
    :param operation: This is the operation that is being performed on the visiting
    """
    visit_goal_doc = get_visit_goal(
        visiting.visited_by, visiting.date, visiting.company)
    if (
        visit_goal_doc.parent_visit_goal
        and visit_goal_doc.parent_visit_goal != ""
    ):
        parent_visit_goal_doc = frappe.get_doc(
            'Visit Goal', visit_goal_doc.parent_visit_goal
        )
    else:
        parent_visit_goal_doc = None

    update_doctors_table(visiting, operation, visit_goal_doc)

    # Updating the achievement of the parent sales person in the visit goal document
    if parent_visit_goal_doc != None:
        update_doctors_table(visiting, operation, parent_visit_goal_doc)


def update_doctors_table(visiting, operation, visit_goal_doc):
    """
    It updates the achievement of a doctor in the visit goal document

    :param visiting: the visiting object
    :param operation: This is the operation to be performed on the table
    :param visit_goal_doc: The document that contains the table of doctors and their productivity
    """
    for row in visit_goal_doc.productivity:
        if row.doctor == visiting.doctor_name:
            row.verified_visits += operation
            row.achievement = round(
                row.verified_visits / row.number_of_visits * 100)

    visit_goal_doc.save(ignore_permissions=True)


def get_visit_goal(sales_person, date, company):
    """
    Get the visit goal for the given sales person and company for the given date

    :param doc: The current document that is being saved
    :return: A dictionary with the name of the visit goal
    """
    visit_goal_name = frappe.db.get_value("Visit Goal", {
        "sales_person": sales_person,
        "company": company,
        "from": ["<=", date],
        "to": [">=", date]
    }, ["name"], as_dict=1)

    return frappe.get_doc("Visit Goal", visit_goal_name)


def update_sales_person_target(sales_invoice, method, operator) -> None:
    """
    يقوم بتحديث تفاصيل الهدف للبائع وبائع الأم في جدول Sales Team

    :param sales_invoice: وثيقة Sales Invoice
    :param method: اسم الدالة في الهوك
    :param operator: +1 أو -1
    :return: لا شيء
    """
    if not sales_invoice.sales_team:
        return

    for sales_person in sales_invoice.sales_team:
        if not sales_person.sales_person or sales_person.sales_person == "":
            continue

        visit_goal_doc = get_visit_goal(
            sales_person.sales_person,
            sales_invoice.posting_date,
            sales_invoice.company
        )

        if (
                visit_goal_doc.parent_visit_goal
                and visit_goal_doc.parent_visit_goal != ""
        ):
            parent_visit_goal_doc = frappe.get_doc(
                'Visit Goal', visit_goal_doc.parent_visit_goal
            )
        else:
            parent_visit_goal_doc = None

        # تحديث تفاصيل الهدف للبائع وبائع الأم
        update_target_breakdown(sales_invoice, visit_goal_doc, operator, sales_person_row=sales_person)
        if parent_visit_goal_doc:
            update_target_breakdown(
                sales_invoice, parent_visit_goal_doc, operator, sales_person_row=sales_person
            )


def update_target_breakdown(sales_invoice, visit_goal_doc, operator, sales_person_row):
    """
    For each item in the sales invoice, if the item code matches the item code in the target breakdown,
    then update the sold quantity based on contribution percentage

    :param sales_invoice: The sales invoice document that is being saved
    :param visit_goal_doc: The visit goal document that you want to update
    :param operator: 1 for adding, -1 for subtracting
    :param sales_person_row: The row of the salesperson in the Sales Team table
    """
    total_contribution_percentage = sum(row.allocated_percentage for row in sales_invoice.sales_team)
    
    for row in visit_goal_doc.target_breakdown:
        for item in sales_invoice.items:
            if item.item_code == row.item:
                contribution_percentage = sales_person_row.allocated_percentage / total_contribution_percentage
                row.sold += operator * item.qty * contribution_percentage
                break

    contribution = sales_person_row.allocated_amount
    visit_goal_doc.achieved += operator * contribution
    visit_goal_doc.save(ignore_permissions=True)






def calculate_fixed_target(doc, collects_goal_doc, operation):
    """
    It takes the amount of the payment and adds it to the total collected amount of the collects goal

    :param doc: The document that is being saved
    :param collects_goal_doc: The document that is being updated
    :param operation: 1 for addition, -1 for subtraction
    """
    collects_goal_doc.total_collected += frappe.utils.flt(
        doc.amount_other_currency * operation)
    calculate_incentives(collects_goal_doc)
    collects_goal_doc.save(ignore_permissions=True)


def update_customer_table(doc, collects_goal_doc, operation):
    """
    It updates the customer collects goal table in the collects goal document

    :param doc: The document that is being saved
    :param collects_goal_doc: The collects goal document that will be updated
    :param operation: 1 for insert, -1 for delete
    """
    # Checking if the customer is in the table. If it is, then it will update the table. If it is not,
    # then it will add the amount to the additional collected.
    customer_not_found = True
    for row in collects_goal_doc.customer_collects_goal:
        if (row.customer == doc.customer):
            row.verified_collects += (doc.amount_other_currency * operation)
            row.verified_visits += operation
            customer_not_found = False
            break

    # If the customer is not found in the table, then it will add the amount to the additional collected.
    if customer_not_found:
        collects_goal_doc.additional_collected += (
            doc.amount_other_currency * operation)

    # Adding the verified collects of each customer in the customer collects goal table and adding it to
    # the additional collected.
    total = sum(
        i.verified_collects for i in collects_goal_doc.customer_collects_goal)
    total += collects_goal_doc.additional_collected

    # Updating the total collected and calculating the incentives.
    collects_goal_doc.total_collected = frappe.utils.flt(total)
    calculate_incentives(collects_goal_doc)
    collects_goal_doc.save(ignore_permissions=True)


def update_collects_goal(doc, operation):
    """
    It updates the target of the collects goal and the parent collects goal if the parent exists

    :param doc: The document that is being saved
    :param operation: 1 for add, -1 for subtract
    """
    collects_goal_doc = get_collects_goal_doc(doc)
    if (
        collects_goal_doc.parent_collects_goal
        and collects_goal_doc.parent_collects_goal != ""
    ):
        parent_collects_goal_doc = frappe.get_doc(
            'Collects Goal', collects_goal_doc.parent_collects_goal
        )
    else:
        parent_collects_goal_doc = None

    # Checking if the target type is fixed target, then it will calculate the fixed target.
    if collects_goal_doc.target_type == "Fixed Target":
        calculate_fixed_target(doc, collects_goal_doc, operation)
        if parent_collects_goal_doc:
            if parent_collects_goal_doc.target_type != "Fixed Target":
                frappe.throw(
                    "Parent and Child must have the same target type.")
            calculate_fixed_target(doc, parent_collects_goal_doc, operation)

    # Updating the customer collects goal table in the collects goal document
    elif collects_goal_doc.target_type == "Customer Debt-based Target":
        update_customer_table(doc, collects_goal_doc, operation)
        if parent_collects_goal_doc:
            if parent_collects_goal_doc.target_type != "Customer Debt-based Target":
                frappe.throw(
                    "Parent and Child must have the same target type.")
            update_customer_table(doc, parent_collects_goal_doc, operation)


def get_collects_goal_doc(doc):
    """
    It gets the name of the Collects Goal that is active for the Sales Person on the date of the Visit
    :return: The name of the Collects Goal
    """
    collect_goal_name = frappe.db.get_value('Collects Goal', {
        'sales_person': doc.visited_by,
        'company': doc.company,
        'from': ['<=', doc.date],
        'to': ['>=', doc.date]
    }, ['name'], as_dict=1)

    # Get objects for Specific Collects Goal
    return frappe.get_doc('Collects Goal', collect_goal_name)


def calculate_incentives(collects_goal_doc):
    """
    If the total collected is greater than or equal to the total targets, then the total incentives is
    equal to the commission percentage of the total collected

    :param collects_goal_doc: The document object of the Collect Goal
    """
    total_incentives = 0
    if len(collects_goal_doc.commissions_range) != 0:
        target_percentage = (collects_goal_doc.total_collected /
                             collects_goal_doc.total_targets) * 100
        for i in collects_goal_doc.commissions_range:
            if target_percentage >= i.from_ and target_percentage <= i.to_:
                total_incentives = (i.commission / 100) * \
                    collects_goal_doc.total_collected
                break
    collects_goal_doc.incentives = frappe.utils.flt(total_incentives)
    collects_goal_doc.save(ignore_permissions=True)
