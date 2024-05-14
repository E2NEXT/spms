// Copyright (c) 2024, aoai and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Payment Analysis"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
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
			"fieldname": "show_zeros",
			"label": __("Show Zeros"),
			"fieldtype": "Check",
			// "width": 100,
		},
	]
};

		// {
		// 	"fieldname": "from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	"width": 100,
		// 	"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
		// },
		// {
		// 	"fieldname": "to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
		// 	"width": 100,
		// 	"default": frappe.datetime.get_today(),
		// 	"reqd": 1,
		// }, 