from . import __version__ as app_version
app_name = "spms"
app_title = "Sales Person Management System"
app_publisher = "aoai"
app_description = "Sales Person Management System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@aoai.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/spms/css/spms.css"
# app_include_js = "/assets/spms/js/spms.js"

# include js, css files in header of web template
# web_include_css = "/assets/spms/css/spms.css"
# web_include_js = "/assets/spms/js/spms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "spms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "Sales Order": "public/js/sales_invoice_form.js",
    "Item": "public/js/item.js",
    "Payment Entry": "public/js/payment_entry.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "spms.install.before_install"
# after_install = "spms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "spms.uninstall.before_uninstall"
# after_uninstall = "spms.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "spms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {

    # A hook to the sales invoice doctype.
    "Sales Invoice": {
        "on_submit": "spms.methods.events.sales_invoice.on_submit",
        "on_cancel": "spms.methods.events.sales_invoice.on_cancel",
    }, 
    
    # A hook to the item doctype.
    "Item": {
        "before_save": "spms.methods.events.item.before_save"
    }, 
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"spms.tasks.all"
# 	],
# 	"daily": [
# 		"spms.tasks.daily"
# 	],
# 	"hourly": [
# 		"spms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"spms.tasks.weekly"
# 	]
# 	"monthly": [
# 		"spms.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "spms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "spms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "spms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#     {
#         "doctype": "{doctype_1}",
#         "filter_by": "{filter_by}",
#         "redact_fields": ["{field_1}", "{field_2}"],
#         "partial": 1,
#     },
#     {
#         "doctype": "{doctype_2}",
#         "filter_by": "{filter_by}",
#         "partial": 1,
#     },
#     {
#         "doctype": "{doctype_3}",
#         "strict": False,
#     },
#     {
#         "doctype": "{doctype_4}"
#     }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"spms.auth.validate"
# ]

# Translation
# --------------------------------
fixtures = [
    "Translation",
    "Territory",
]

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
