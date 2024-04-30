# Copyright (c) 2022, aoai and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from spms.methods.utils import generate_qrcode
from frappe.utils import cstr
from spms.methods.utils import update_collects_goal
import hashlib


class Collecting(WebsiteGenerator):

	def on_submit(self) -> None:
		"""
		`update_collects_goal(self, 1)`
		
		This function is called when the user clicks the submit button. It updates the goal for the
		number of collects
		"""
		update_collects_goal(self, 1)

	def on_cancel(self) -> None:
		"""
		`update_collects_goal(self, -1)`
		
		This function is called when the user clicks the "Cancel" button
		"""
		update_collects_goal(self, -1)

	def before_submit(self):
		"""
		It takes the name of the route and generates a QR code image for it
		"""
		if not self.image:
			self.route = hashlib.sha1(str(self.name).encode()).hexdigest()
			site_name = frappe.utils.get_url()
			image_path = generate_qrcode(
				site_name=site_name, route_name=self.route)
			self.image = image_path
		# Calculate outstanding amount for each invoice
		for invoice in self.invoices:
			invoice.out_standing_amount = invoice.out_standing_amount - invoice.allocated_amount
