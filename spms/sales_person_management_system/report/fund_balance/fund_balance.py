import frappe


def execute(filters=None):
    columns = [
        "Account:Link/Account:150",
        "Company:Link/Company:150",
        "Balance:Currency:150",
    ]

    # Initialize the filters for the Account
    account_filters = {}

    # If account filter is provided, add it to the filters
    if filters and filters.get("account"):
        account_filters["name"] = ["in", filters.get("account")]

    # If company filter is provided, add it to the filters
    if filters and filters.get("company"):
        account_filters["company"] = ["in", filters.get("company")]

    if filters and filters.get("account_type") and filters.get("account_type") != "All":
        account_filters["account_type"] = ["in", filters.get("account_type")]

    if filters and filters.get("root_type") and filters.get("root_type") != "All":
        account_filters["root_type"] = ["in", filters.get("root_type")]

    # Fetch the Accounts based on the filters
    accounts = frappe.get_all(
        "Account", filters=account_filters, fields=["name", "company"]
    )

    account_totals = {}
    total_balance = 0
    for account in accounts:
        # Initialize the filters for the GL Entry
        gl_filters = {"account": ["in", account["name"]]}

        # If cost_center filter is provided, add it to the filters
        if filters and filters.get("cost_center"):
            gl_filters["cost_center"] = ["in", filters.get("cost_center")]

        if (
            filters
            and filters.get("from_date")
            and filters.get("to_date")
            and filters.get("from_date") <= filters.get("to_date")
            and filters.get("from_date") != ""
            and filters.get("to_date") != ""
        ):
            gl_filters["posting_date"] = [
                "between",
                [filters.get("from_date"), filters.get("to_date")],
            ]

        gl_entries = frappe.get_all(
            "GL Entry",
            filters=gl_filters,
            fields=["account", "company", "debit", "credit"],
        )
        debit = sum(entry["debit"] for entry in gl_entries)
        credit = sum(entry["credit"] for entry in gl_entries)

        balance = debit - credit

        account_totals[account["name"]] = [account["name"], account["company"], balance]

        # total_balance += balance

    data = list(account_totals.values())

    # data.append(["Total", "", total_balance])

    return columns, data
