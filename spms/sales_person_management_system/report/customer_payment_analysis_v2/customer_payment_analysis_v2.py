import frappe
from frappe import _
from erpnext.accounts.doctype.payment_entry.payment_entry import get_party_details
import frappe.defaults
from erpnext.accounts.utils import get_balance_on

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
            "fieldname": "last_customer_account_balance",
            "label": _("Last Customer Balance"),
            "fieldtype": "Currency",
            "width": 180,
        },
        {
            "fieldname": "total_sales",
            "label": _("Total Sales"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "total_returned",
            "label": _("Total Returned"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "total_discounts",
            "label": _("Total Discounts"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "net_sales",
            "label": _("Net Sales"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "total_payments",
            "label": _("Net Payments"),
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "fieldname": "customer_account_balance",
            "label": _("Customer Account Balance"),
            "fieldtype": "Currency",
            "width": 180,
        },
    ]

    data = []
    total_balance = 0.0  # Variable to store the total balance

    if not filters:
        return columns, data

    company = filters.get("company")
    
    customers = []
    if filters.get("customer"):
        customers = frappe.get_list(
            "Customer",
            filters={"customer_name": filters.get("customer")},
            fields=["name"],
        )
    elif filters.get("customer_group"):
        customers = frappe.get_list(
            "Customer",
            filters={"customer_group": filters.get("customer_group")},
            fields=["name"],
        )
    else:
        customers = frappe.get_list("Customer", fields=["name"])

    current_date = frappe.utils.get_datetime(frappe.utils.now()).date()

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    t1 = t2 = t3 = t4 = t5 = t7 = t8 = 0

    # Collect all payment entries and sales invoices first
    customer_names = [customer['name'] for customer in customers]

    payments = frappe.get_all(
        "Payment Entry",
        filters={
            "company": company,
            "party_type": "Customer",
            "party": ["in", customer_names],
            "posting_date": ["between", [from_date, to_date]],
            "docstatus": 1,
        },
        fields=["party", "custom_total_paid"],
    )

    sales_invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "company": company,
            "customer": ["in", customer_names],
            "posting_date": ["between", [from_date, to_date]],
            "docstatus": 1,
        },
        fields=["customer", "base_total", "net_total", "status", "discount_amount", "is_return"],
    )

    # Organize data by customer
    customer_payments = {}
    customer_sales = {}
    customer_returns = {}
    customer_discounts = {}

    for payment in payments:
        customer_payments.setdefault(payment['party'], 0)
        customer_payments[payment['party']] += payment['custom_total_paid']

    for invoice in sales_invoices:
        if invoice['status'] != "Return":
            customer_sales.setdefault(invoice['customer'], 0)
            customer_sales[invoice['customer']] += invoice['base_total']
        if invoice['is_return']:
            customer_returns.setdefault(invoice['customer'], 0)
            customer_returns[invoice['customer']] += invoice['net_total']
        customer_discounts.setdefault(invoice['customer'], 0)
        customer_discounts[invoice['customer']] += invoice['discount_amount']

    for customer in customers:
        customer_name = customer['name']
        last_party_balance = get_balance_on(party_type="Customer", party=customer_name, date=filters.get("from_date"), company=company)

        total_payments = customer_payments.get(customer_name, 0)
        total_non_returned_sales = customer_sales.get(customer_name, 0)
        total_returned_sales = customer_returns.get(customer_name, 0)
        total_discount_amount = customer_discounts.get(customer_name, 0)

        net_sales = total_non_returned_sales + total_returned_sales - total_discount_amount

        balance = get_party_details(
            company=company,
            party_type="Customer",
            party=customer_name,
            date=current_date,
        )

        total_balance += balance.get("party_balance", 0.0)

        t1 += total_payments
        t2 += total_non_returned_sales
        t3 += total_returned_sales
        t4 += total_discount_amount
        t5 += net_sales
        t7 += last_party_balance
        t8 += balance["party_balance"]

        data.append({
            "customer": customer_name,
            "total_payments": total_payments,
            "total_sales": total_non_returned_sales,
            "total_returned": total_returned_sales,
            "total_discounts": total_discount_amount,
            "net_sales": net_sales,
            "last_customer_account_balance": last_party_balance,
            "customer_account_balance": net_sales - total_payments
        })

    data.append({
        "customer": "total",
        "total_payments": t1,
        "total_sales": t2,
        "total_returned": t3,
        "total_discounts": t4,
        "net_sales": t5,
        "last_customer_account_balance": t7,
        "customer_account_balance": t8,
    })

    return columns, data
