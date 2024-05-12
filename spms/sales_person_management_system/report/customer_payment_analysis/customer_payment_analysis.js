// Copyright (c) 2024, aoai and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Payment Analysis"] = {
	"filters": [
		{
			"fieldname": "show_zeros",
			"label": __("Show Zeros"),
			"fieldtype": "Check",
			// "width": 100,
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 100,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 100,
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			// "on_change": function (query_report) {
			// 	if (!query_report.date_range_change) {
			// 		query_report.set_filter_value('date_range', '');
			// 	}
			// }
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
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": 100,
			"reqd": 1,
			// "on_change": function (query_report) {
			// 	company = query_report.get_filter_value('company');
			// 	const cost_center_filter = query_report.get_filter('cost_center');
			// 	cost_center_filter.df.get_query = function (doc, cdt, cdn) {
			// 		// query_report.refresh();
			// 		return {
			// 			filters: {
			// 				"company": company
			// 			}
			// 		};
			// 	};
			// 	cost_center_filter.refresh();
			// 	query_report.refresh();
			// }
		},
	]
};
