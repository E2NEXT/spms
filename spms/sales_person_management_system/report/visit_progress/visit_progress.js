frappe.query_reports["Visit Progress"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 0
        },
        {
            "fieldname": "sales_person",
            "label": __("Salesperson"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "reqd": 0
        },
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 0
        }
    ]
};
