import frappe
from frappe.utils import nowdate, getdate, get_first_day, get_last_day
from dateutil.relativedelta import relativedelta

def execute(filters=None):
    columns = [
        {
            "label": "Salesperson",
            "fieldname": "salesperson",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 120,
        },
        {
            "label": "Sales Target (Amount)",
            "fieldname": "sales_target_amount",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Achieved Sales Amount (Total)",
            "fieldname": "achieved_sales_amount",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Collection Target (Amount)",
            "fieldname": "collection_target_amount",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Achieved Payment Entry Amount (Total)",
            "fieldname": "achieved_payment_entry_amount",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Sales Visits Target (Number)",
            "fieldname": "sales_visits_target",
            "fieldtype": "Int",
            "width": 200,
        },
        {
            "label": "Number of Sales Visits (Count)",
            "fieldname": "number_of_sales_visits",
            "fieldtype": "Int",
            "width": 200,
        },
        {
            "label": "Number of Payment Visits (Count)",
            "fieldname": "number_of_payment_visits",
            "fieldtype": "Int",
            "width": 200,
        },
    ]
    data = get_report_data(filters)
    return columns, data

def get_report_data(filters):
    data = []
    sales_persons = frappe.db.sql("""
    select name from `tabSales Person WHERE enabled = 1`
    """, as_dict=0)
    salesperson_ = filters.get("salesperson")
    if salesperson_:
        sales_persons = [(salesperson_,)] # add it as tuple to be on the same shape of the sql query result
    month_name = filters.get("month")
    company = filters.get("company")
    territory = filters.get("territory")

    start_date = get_first_day(month_name)
    end_date = get_last_day(month_name)
    for salesperson_tuple in sales_persons:
        salesperson = salesperson_tuple[0]
        sales_target_amount = f"""
            SELECT sum(tvg.target) from `tabVisit Goal` tvg
            where sales_person = '{salesperson}'
            AND `from` >= '{start_date}'
            AND `to` <= '{end_date}'
            AND company = '{company}'
            """
        if territory:
            sales_target_amount += f"AND territory = '{territory}'"
        sales_target_amount = frappe.db.sql(sales_target_amount)[0][0] or 0

        collection_target_amount = f"""
            SELECT SUM(`total_targets`)
            FROM `tabCollects Goal`
            WHERE `sales_person` = '{salesperson}'
            AND `from` >= '{start_date}'
            AND `to` <= '{end_date}'
            AND company = '{company}'
            """
        if territory:
            collection_target_amount += f"AND territory = '{territory}'"
        collection_target_amount = frappe.db.sql(collection_target_amount)[0][0] or 0

        achieved_sales_amount = f"""
            SELECT SUM(si.net_total) 
            FROM `tabSales Invoice` AS si
            JOIN `tabSales Team` AS st ON si.name = st.parent
            WHERE st.sales_person = '{salesperson}'
            AND si.posting_date BETWEEN '{start_date}' AND '{end_date}'
            AND si.docstatus = 1
            AND company = '{company}'
        """
        achieved_sales_amount = frappe.db.sql(achieved_sales_amount)[0][0] or 0

        achieved_payment_entry_amount = f"""
            SELECT SUM(pe.paid_amount)
            FROM `tabPayment Entry` AS pe
            JOIN `tabCommission` AS com ON pe.name = com.parent
            WHERE com.sales_person = '{salesperson}'
            AND pe.posting_date BETWEEN '{start_date}' AND '{end_date}'
            AND pe.docstatus = 1
            AND company = '{company}'
            """
        achieved_payment_entry_amount = frappe.db.sql(achieved_payment_entry_amount)[0][0] or 0

        sales_visits_target = f"""
            SELECT sum(p.number_of_visits) from `tabProductivity` p
            join `tabVisit Goal` tvg 
            on p.parent = tvg.name
            WHERE tvg.sales_person = '{salesperson}'
            AND tvg.creation BETWEEN '{start_date}' AND '{end_date}'
            AND tvg.company = '{company}'
            """

        if territory:
            sales_visits_target += f"AND tvg.territory = '{territory}'"

        sales_visits_target = frappe.db.sql(sales_visits_target)[0][0] or 0

        number_of_sales_visits = f"""
            SELECT sum(p.verified_visits) from `tabProductivity` p
            join `tabVisit Goal` tvg 
            on p.parent = tvg.name
            WHERE tvg.sales_person = '{salesperson}'
            AND tvg.creation BETWEEN '{start_date}' AND '{end_date}'
            AND tvg.company = '{company}'
            """
        if territory:
            number_of_sales_visits += f"AND territory = '{territory}'"
        number_of_sales_visits = frappe.db.sql(number_of_sales_visits)[0][0] or 0

        number_of_payment_visits = f"""
            SELECT COUNT(*)
            FROM `tabCollecting`
            WHERE visited_by = '{salesperson}'
            AND date BETWEEN '{start_date}' AND '{end_date}'
            AND company = '{company}'
            AND docstatus = 1
            """
        if territory:
            number_of_payment_visits += f"AND territory = '{territory}'"
        number_of_payment_visits = frappe.db.sql(number_of_payment_visits)[0][0] or 0

        data.append(
            {
                "salesperson": salesperson,
                "sales_target_amount": sales_target_amount,
                "achieved_sales_amount": achieved_sales_amount,
                "collection_target_amount": collection_target_amount,
                "achieved_payment_entry_amount": achieved_payment_entry_amount,
                "sales_visits_target": sales_visits_target,
                "number_of_sales_visits": number_of_sales_visits,
                "number_of_payment_visits": number_of_payment_visits,
            }
        )

    return data