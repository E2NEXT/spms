# Copyright (c) 2022, aoai and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from spms.methods.utils import update_doctor_productivity


class Visiting(WebsiteGenerator):
    def on_save(self):
        frappe.publish_realtime('notification', data={'key': 'value'})
        
    def on_submit(self):
        """
        It updates the doctor's productivity by 1
        """
        update_doctor_productivity(self, 1)

    def on_cancel(self):
        """
        It updates the doctor's productivity by subtracting 1 from the doctor's productivity
        """
        update_doctor_productivity(self, -1)