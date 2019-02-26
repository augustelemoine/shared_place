# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dokos and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from shared_place.shared_place.utils import get_url_list_for_redirect, get_resource_price_and_qty, \
	shared_place_order, shared_update_cart
from erpnext.shopping_cart.cart import update_cart
from frappe.utils import cint

class TestSharedPlaceBooking(unittest.TestCase):
	def setUp(self):
		add_room()
		add_address()
		frappe.db.set_value("Shopping Cart Settings", None, "enabled", 1)

	def test_get_url_list_for_redirect(self):
		urls = get_url_list_for_redirect()
		self.assertTrue(urls['items'] == ['Petite salle'])

	def test_get_resource_price_and_qty(self):
		resource_details = get_resource_price_and_qty({ "item_code": "Petite salle", "price_list": "Standard Selling"})
		self.assertTrue(cint(resource_details[0]['price_list_rate']) == 15)

	def test_shared_place_order(self):
		frappe.set_user = "test_cart_user@example.com"
		update_cart("Petite salle", 2)
		so = shared_place_order()
		self.assertTrue(so)

	def test_shared_update_cart(self):
		frappe.set_user = "test_cart_user@example.com"
		shared_update_cart("Petite salle", 2)
		qu = shared_update_cart("Petite salle", 1)
		doc = frappe.get_doc("Quotation", qu["name"])
		self.assertTrue(len(doc.items)==2)

	def tearDown(self):
		pass

def add_room():
	if not frappe.db.exists("Shared Place Room", "Salle A"):
		item = frappe.new_doc("Item")
		item.item_code = "Petite salle"
		item.item_group = "Services"
		item.is_stock_item = 0
		item.insert()

		item_price = frappe.new_doc("Item Price")
		item_price.item_code = item.name
		item_price.price_list = "Standard Selling"
		item_price.price_list_rate = 15
		item_price.insert()


		room = frappe.new_doc("Shared Place Room")
		room.room_name = "Salle A"
		room.item = item.name
		room.price_list = "Standard Selling"
		room.insert()

def add_address():
	address = frappe.new_doc("Address")
	address.address_title = "Test address for shared places"
	address.address_line1 = "10 rue de la Paix"
	address.city = "Paris"
	address.country = "France"
	address.insert()