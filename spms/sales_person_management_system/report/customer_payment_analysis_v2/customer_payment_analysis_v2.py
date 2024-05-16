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
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"fieldname": "customer_account_balance",
			"label": _("Customer Account Balance"),
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"fieldname": "last_customer_account_balance",
			"label": _("Last Customer Balance"),
			"fieldtype": "Currency",
			"width": 180,
		},
	]

	data = []
	total_balance = 0.0  # Variable to store the total balance

	if not filters:
		return columns, data

	if filters.get("customer"):
		customers = frappe.get_list(
			"Customer",
			filters={
				"customer_name": filters.get("customer"),
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

	current_datetime = frappe.utils.get_datetime(frappe.utils.now())
	current_date = current_datetime.date()

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	t1=0
	t2=0
	t3=0
	t4=0
	t5=0
	t6=0
	t7=0
	t8=0

	# Populating 'data' list with customer data
	for customer in customers:
		last_party_balance = get_balance_on(party_type="Customer",  party=customer.name,date=filters.get("from_date"))
		all_payments = frappe.get_all(
			"Payment Entry",
			filters={
				"party_type": "Customer",
				"party": customer.name,
				"posting_date": ["between", [from_date, to_date]],
				"docstatus": 1,
			},
			fields=["posting_date", "base_paid_amount","custom_total_paid"],
			order_by="posting_date desc",
		)
		total_payments = 0
		for p in all_payments:
			total_payments += p.custom_total_paid


		all_non_returned_sales = frappe.get_all(
			"Sales Invoice",
			filters={
				"customer": customer.name,
				"posting_date": ["between", [from_date, to_date]],
				"status":["!=","Returned"],
				# "is_return":1,
				"docstatus": 1,
			},
			fields=["total"],
			order_by="posting_date desc",
		)
		total_non_returned_sales = 0
		for p in all_non_returned_sales:
			total_non_returned_sales += p.total

		all_returned_sales = frappe.get_all(
			"Sales Invoice",
			filters={
				"customer": customer.name,
				"posting_date": ["between", [from_date, to_date]],
				"status":["=","Return"],
				"is_return":1,
				"docstatus": 1,
			},
			fields=["net_total"],
			order_by="posting_date desc",
		)
		total_returned_sales = 0
		for p in all_returned_sales:
			total_returned_sales += p.net_total

		all_discounted_sales = frappe.get_all(
			"Sales Invoice",
			filters={
				"customer": customer.name,
				"posting_date": ["between", [from_date, to_date]],
				"docstatus": 1,
			},
			fields=["discount_amount"],
			order_by="posting_date desc",
		)
		total_discount_amount = 0
		for p in all_discounted_sales:
			total_discount_amount += p.discount_amount

		net_sales = total_non_returned_sales+total_returned_sales-total_discount_amount
		# total = 

		balance = get_party_details(
			company=filters.get("company"),
			party_type="Customer",
			party=customer.name,
			date=current_date,
		)

		total_balance += balance.get("party_balance", 0.0)  # Add balance to total

		t1+=total_payments
		t2+=total_non_returned_sales
		t3+=total_returned_sales
		t4+=total_discount_amount
		t5+=net_sales
		t6+=net_sales
		t7+=last_party_balance
		t8+= balance["party_balance"]

		data.append(
			{
				"customer": customer.name,
				"total_payments": total_payments,
				"total_sales": total_non_returned_sales,
				"total_returned": total_returned_sales,
				"total_discounts": total_discount_amount,
				"net_sales":net_sales,
				"total":net_sales,
				"last_customer_account_balance": last_party_balance, 
				"customer_account_balance": balance["party_balance"],
			}
		)

	# Append total row to data
	data.append({
		"customer": "total",
		"total_payments": t1,
		"total_sales": t2,
		"total_returned": t3,
		"total_discounts": t4,
		"net_sales":t5,
		"total":t6,
		"last_customer_account_balance": t7, 
		"customer_account_balance": t8,
	})

	return columns, data
