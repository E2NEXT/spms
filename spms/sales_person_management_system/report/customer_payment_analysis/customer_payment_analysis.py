import frappe
from frappe import _
from erpnext.accounts.doctype.payment_entry.payment_entry import get_party_details


def execute(filters=None):
    columns = [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120,
        },
        {
            "fieldname": "last_payment_date",
            "label": _("Last Payment Date"),
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "last_payment_amount",
            "label": _("Last Payment Amount"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "customer_account_balance",
            "label": _("Customer Account Balance"),
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "fieldname": "report_time",
            "label": _("Report Time"),
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "report_date",
            "label": _("Report Date"),
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "days_from_last_payment",
            "label": _("Days from Last Payment"),
            "fieldtype": "Int",
            "width": 150,
        },
    ]

    data = []

    if not filters:
        return columns, data

    # Fetching customer data based on filters (including Customer Group filter)
    if filters.get("customer"):
        customers = frappe.get_list(
            "Customer",
            filters={
                "customer_name": filters.get("customer"),
                "customer_group": filters.get("customer_group"),
            },
            fields=["name"],
        )
    else:
        if filters.get("customer_group"):
            customers = frappe.get_list(
                "Customer",
                filters={"customer_group": filters.get("customer_group")},
                fields=["name"],
            )
        else:
            customers = frappe.get_list("Customer", fields=["name"])

    # Get current date and time
    current_datetime_str = frappe.utils.now()
    current_datetime = frappe.utils.get_datetime(current_datetime_str)
    current_date = current_datetime.date()
    current_time = current_datetime.strftime("%H:%M:%S")  # Extracting time portion

    # Populating 'data' list with customer data
    for customer in customers:
        # last_payment_entry = frappe.get_all("Payment Entry",
        # 									filters={"party_type": "Customer",
        # 											"party": customer.name,
        # 											"docstatus": 1,
        # 											"posting_date": (">=", filters.get("from_date")),
        # 											"posting_date": ("<=", filters.get("to_date"))},
        # 									fields=["posting_date", "base_paid_amount"],
        # 									order_by="posting_date desc",
        # 									limit=1)
        last_payment_entry = frappe.get_all(
            "Payment Entry",
            filters={
                "party_type": "Customer",
                "party": customer.name,
                "docstatus": 1,
            },
            fields=["posting_date", "base_paid_amount"],
            order_by="posting_date desc",
            limit=1,
        )
        last_payment_date = (
            last_payment_entry[0].posting_date if last_payment_entry else None
        )
        last_payment_amount = (
            last_payment_entry[0].total_amount if last_payment_entry else None
        )
        days_from_last_payment = (
            (current_date - last_payment_date).days if last_payment_date else None
        )

        balance = get_party_details(
            company=filters.get("company"),
            party_type="Customer",
            party=customer.name,
            date=current_date,
        )
        print(balance)

        if filters.get("show_zeros") == 1:
            data.append(
                {
                    "customer": customer.name,
                    "last_payment_date": last_payment_date,
                    "last_payment_amount": last_payment_amount,
                    "customer_account_balance": balance[
                        "account_balance"
                    ],  # You need to implement this logic
                    "report_time": current_time,
                    "report_date": current_date,
                    "days_from_last_payment": days_from_last_payment,  # Calculated days from last payment
                }
            )
        elif balance["account_balance"] != 0.0:
            data.append(
                {
                    "customer": customer.name,
                    "last_payment_date": last_payment_date,
                    "last_payment_amount": last_payment_amount,
                    "customer_account_balance": balance[
                        "account_balance"
                    ],  # You need to implement this logic
                    "report_time": current_time,
                    "report_date": current_date,
                    "days_from_last_payment": days_from_last_payment,  # Calculated days from last payment
                }
            )

    return columns, data
