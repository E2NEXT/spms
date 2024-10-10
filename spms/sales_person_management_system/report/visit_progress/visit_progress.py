import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()

    data = get_data(filters)

    return columns, data

# function to get the columns for the report
def get_columns():
    return [
        {
            "fieldname": "sales_person",
            "label": "Salesperson",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "target",
            "label": "Target",
            "fieldtype": "Float",
            "width": 200
        },
        {
            "fieldname": "achieved",
            "label": "Achieved",
            "fieldtype": "Float",
            "width": 200
        },
        {
            "fieldname": "percent",
            "label": "Achievement %",
            "fieldtype": "HTML",
            "width": 500
        }
    ]

# Fetch the data based on filters (parent and children records)
def get_data(filters):
    data = []

    # Check for empty filters and set them to default wildcard values if empty
    sales_person_filter = filters.get("sales_person") if filters.get("sales_person") else "%"
    company_filter = filters.get("company") if filters.get("company") else "%"
    from_date_filter = filters.get("from_date") if filters.get("from_date") else "1900-01-01"
    to_date_filter = filters.get("to_date") if filters.get("to_date") else "2999-12-31"

    # Query for parent data (Visit Goal with is_group = 1)
    parent_data = frappe.db.sql("""
        SELECT 
            name, sales_person, target, achieved, 
            (achieved / target) * 100 as percent
        FROM `tabVisit Goal`
        WHERE docstatus < 2
        AND is_group = 1
        AND sales_person LIKE %(sales_person)s
        AND company LIKE %(company)s
        AND `from` >= %(from_date)s
        AND `to` <= %(to_date)s
        AND EXISTS (SELECT 1 FROM `tabSales Person` sp WHERE sp.name = `tabVisit Goal`.sales_person AND sp.enabled = 1)
    """, {
        "sales_person": sales_person_filter,
        "company": company_filter,
        "from_date": from_date_filter,
        "to_date": to_date_filter
    }, as_dict=1)

    # Process each parent record
    for parent in parent_data:
        # Append the parent row
        data.append({
            "sales_person": parent.sales_person,
            "target": parent.target,
            "achieved": parent.achieved,
            "percent": format_progress_bar(parent.percent),
            "is_parent": True
        })

        # Query for child salespersons related to the parent (Visit Goal with is_group = 0)
        child_salespersons = frappe.db.sql("""
            SELECT 
                sales_person, target, achieved,
                (achieved / target) * 100 as percent
            FROM `tabVisit Goal`
            WHERE parent_visit_goal = %(parent_name)s
            AND is_group = 0
        """, {"parent_name": parent.name}, as_dict=1)

        # Append each child salesperson row
        for child in child_salespersons:
            data.append({
                "sales_person": child.sales_person,
                "target": child.target,
                "achieved": child.achieved,
                "percent": format_progress_bar(child.percent),
                "is_parent": False
            })
        
        # Add a separator after each parent's children
        data.append({
            "sales_person": None,
            "target":  None,
            "achieved": None,
            "percent": None,
            "is_parent": False
        })

    return data

# function to format the progress bar based on percentage
def format_progress_bar(percent):
    color = "danger"
    
    if flt(percent) >= 75:
        color = "success"
    elif flt(percent) >= 50:
        color = "warning"

    return f'''
    <div class="progress" style="height: 20px;">
        <div class="progress-bar bg-{color}" role="progressbar" style="width: {percent}%;" aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100">
            {percent:.2f}%
        </div>
    </div>
    '''
