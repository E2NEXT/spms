# Copyright (c) 2022, aoai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Doctor(Document):
    def save(self):
        print("qqqqqqqqqqqqq")
        frappe.publish_realtime('notification')
        