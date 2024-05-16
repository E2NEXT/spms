// Copyright (c) 2024, aoai and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Payment Analysis V2"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default":frappe.defaults.get_user_default("company"),
			"width": 100,
			"reqd": 1,
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 100,
		},
		 {
			"fieldname": "customer_group",
			"label": __("Customer Group"),
			"fieldtype": "Link",
			"options": "Customer Group",
			"width": 100,
		}, 
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 100,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 100,
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"on_change": function(query_report) {
				if (!query_report.date_range_change) {
					query_report.set_filter_value('date_range', '');
				}
			}
		},
	]
};
