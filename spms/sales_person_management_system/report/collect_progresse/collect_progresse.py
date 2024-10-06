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
			"fieldname": "total_targets",
			"label": "Total Target",
			"fieldtype": "Float",
			"width": 200
		},
		{
			"fieldname": "total_collected",
			"label": "Total Collected",
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

# function to get the data for the report
def get_data(filters):
    data = []
    
    # check for empty filters and set them to default wildcard values if empty
    sales_person_filter = filters.get("sales_person") if filters.get("sales_person") else "%"
    company_filter = filters.get("company") if filters.get("company") else "%"
    from_date_filter = filters.get("from_date") if filters.get("from_date") else "1900-01-01"
    to_date_filter = filters.get("to_date") if filters.get("to_date") else "2999-12-31"
    
    # query for parent data (Collects Goal with is_group = 1)
    parent_data = frappe.db.sql("""
		SELECT
			name, sales_person, total_targets, total_collected,
			(total_collected / total_targets) * 100 as percent
		FROM `tabCollects Goal`
		WHERE docstatus < 2
		AND is_group = 1
		AND sales_person LIKE %(sales_person)s
		AND company LIKE %(company)s
		AND `from` >= %(from_date)s
		AND `to` <= %(to_date)s
		AND EXISTS (SELECT 1 FROM `tabSales Person` sp WHERE sp.name = `tabCollects Goal`.sales_person AND sp.enabled = 1)
	""", {
		"sales_person": sales_person_filter,
		"company": company_filter,
		"from_date": from_date_filter,
		"to_date": to_date_filter
	}, as_dict=1)
    
    for parent in parent_data:
        data.append({
			"sales_person": parent.sales_person,
			"total_targets": parent.total_targets,
			"total_collected": parent.total_collected,
			"percent": format_progress_bar(parent.percent),
			"is_group": True
		})
        
        # query for child data (Collects Goal with is_group = 0)
        child_collects = frappe.db.sql("""
			SELECT
				sales_person, total_targets, total_collected,
				(total_collected / total_targets) * 100 as percent
			FROM `tabCollects Goal`
			WHERE parent_collects_goal = %(parent_name)s
			AND is_group = 0
		""", {"parent_name": parent.name}, as_dict=1)
        
        for child in child_collects:
            data.append({
				"sales_person": child.sales_person,
				"total_targets": child.total_targets,
				"total_collected": child.total_collected,
				"percent": format_progress_bar(child.percent),
				"is_parent": False
			})
        
        # Add a separator after each parent's children
        data.append({
			"sales_person": None,
			"total_targets": None,
			"total_collected": None,
			"percent": None,
			"is_parent": False
		})
    
    return data

# function to format the progress bar
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