# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dokos and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import get_url, flt, cint, fmt_money
from frappe import _
from erpnext.accounts.doctype.pricing_rule.pricing_rule import get_pricing_rule_for_item

@frappe.whitelist(allow_guest=True)
def get_url_list_for_redirect():
	items = frappe.db.sql_list("""
		SELECT DISTINCT item 
		FROM (SELECT item FROM `tabShared Place Room`
		UNION ALL 
		SELECT item FROM `tabShared Place Resource`
		UNION ALL 
		SELECT item FROM `tabShared Place Coworking Space`
		UNION ALL
		SELECT item FROM `tabShared Place Booking Options`) result
	""")
	
	url_list = [get_url(x[0]) for x in frappe.get_all("Item", filters=[["name", "in", items]], fields=["route"], as_list=1)]

	return {"items": items, "links": url_list}


@frappe.whitelist()
def get_resource_price_and_qty(args):
	conditions = "where (customer is null or customer = '') and (supplier is null or supplier = '')"
	conditions += """ and item_code=%(item_code)s
		and price_list=%(price_list)s"""

	if args.get('transaction_date'):
		conditions += """ and %(transaction_date)s between
			ifnull(valid_from, '2000-01-01') and ifnull(valid_upto, '2500-12-31')"""

	return frappe.db.sql(""" select name, price_list_rate, uom, packing_unit, min_qty
		from `tabItem Price` {conditions}
		order by uom desc, min_qty desc """.format(conditions=conditions), args, as_dict=True)

@frappe.whitelist()
def shared_place_order():
	from erpnext.shopping_cart.cart import place_order
	sales_order = place_order()

	so = frappe.get_doc("Sales Order", sales_order)
	for quotation in list(set([d.prevdoc_docname for d in so.get("items")])):
		if quotation:
			bookings = frappe.get_all("Shared Place Booking", filters={"quotation": quotation})

			for booking in bookings:
				doc = frappe.get_doc("Shared Place Booking", booking.name)
				doc.sales_order = sales_order
				doc.flags.ignore_permissions=True
				doc.save()
				doc.submit()

	return sales_order

@frappe.whitelist()
def shared_update_cart(item_code, qty, with_items=False):
	from erpnext.shopping_cart.cart import update_cart
	calendar_items = get_url_list_for_redirect()

	if item_code in calendar_items["items"]:
		return update_calendar_items_cart(item_code, qty, with_items)
	else:
		return update_cart(item_code, qty, with_items)

def update_calendar_items_cart(item_code, qty, uom_name):
	from erpnext.shopping_cart.cart import _get_cart_quotation, apply_cart_settings, \
		set_cart_count, get_cart_quotation, get_shopping_cart_menu
	quotation = _get_cart_quotation()

	empty_card = False
	qty = flt(qty)
	if qty == 0:
		quotation_items = quotation.get("items", {"item_code": ["!=", item_code]})
		if quotation_items:
			quotation.set("items", quotation_items)
		else:
			empty_card = True

	else:
		quotation.append("items", {
			"doctype": "Quotation Item",
			"item_code": item_code,
			"qty": qty,
			"uom": get_sp_uom(uom_name)
		})

	apply_cart_settings(quotation=quotation)

	quotation.flags.ignore_permissions = True
	quotation.payment_schedule = []
	if not empty_card:
		quotation.save()
	else:
		quotation.delete()
		quotation = None

	set_cart_count(quotation)

	context = get_cart_quotation(quotation)

	return {
		'name': quotation.name,
		'shopping_cart_menu': get_shopping_cart_menu(context)
	}

@frappe.whitelist()
def remove_linked_bookings(item):
	from erpnext.shopping_cart.cart import _get_cart_quotation, update_cart

	quotation = _get_cart_quotation()

	rooms = [x['name'] for x in frappe.get_all("Shared Place Room", filters={"item": item})]
	resources = [x['name'] for x in frappe.get_all("Shared Place Resource", filters={"item": item})]

	bookings = []
	if rooms:
		bookings.extend(frappe.get_all("Shared Place Booking", filters={"booking_type": "Shared Place Room", "booked_resource": ("in", (rooms)), "quotation": quotation.name, "docstatus": 0}))
	if resources:
		bookings.extend(frappe.get_all("Shared Place Booking", filters={"booking_type": "Shared Place Resource", "booked_resource": ("in", (resources)), "quotation": quotation.name, "docstatus": 0}, fields=["name", "linked_booking"]))

	for booking in bookings:
		if booking.linked_booking:
			room = frappe.db.get_value("Shared Place Booking", booking.linked_booking, "booked_resource")
			item = frappe.db.get_value("Shared Place Room", room, "item")
			update_cart(item, 0)

		else:
			links = frappe.get_all("Shared Place Booking", filters={"linked_booking": booking.name, "docstatus": 0, "name": ["!=", booking.name]})
			for link in links:
				res = frappe.db.get_value("Shared Place Booking", link.name, "booked_resource")
				item = frappe.db.get_value("Shared Place Resource", res, "item")
				update_cart(item, 0)

		frappe.delete_doc("Shared Place Booking", booking.name, ignore_permissions=True)

	return bookings

def on_quotation_delete(doc, method):
	if doc.order_type == "Shopping Cart":
		bookings = frappe.get_all("Shared Place Booking", filters={"quotation": doc.name})
		for booking in bookings:
			frappe.delete_doc("Shared Place Booking", booking.name, ignore_permissions=True)

def update_gcalendar_connector(doc, method):
	if doc.python_module == "frappe.data_migration.doctype.data_migration_connector.connectors.calendar_connector":
		doc.python_module = "shared_place.shared_place.shared_place_connector"

def get_price(item_code, price_list, uom, customer_group, company, qty=1):
	template_item_code = frappe.db.get_value("Item", item_code, "variant_of")

	if price_list:
		price = frappe.get_all("Item Price", fields=["price_list_rate", "currency"],
			filters={"price_list": price_list, "item_code": item_code, "uom": uom})

		if template_item_code and not price:
			price = frappe.get_all("Item Price", fields=["price_list_rate", "currency"],
				filters={"price_list": price_list, "item_code": template_item_code, "uom": uom})

		if price:
			pricing_rule = get_pricing_rule_for_item(frappe._dict({
				"item_code": item_code,
				"qty": qty,
				"transaction_type": "selling",
				"price_list": price_list,
				"customer_group": customer_group,
				"company": company,
				"conversion_rate": 1,
				"for_shopping_cart": True,
				"currency": frappe.db.get_value("Price List", price_list, "currency")
			}))

			if pricing_rule:
				if pricing_rule.pricing_rule_for == "Discount Percentage":
					price[0].price_list_rate = flt(price[0].price_list_rate * (1.0 - (flt(pricing_rule.discount_percentage) / 100.0)))

				if pricing_rule.pricing_rule_for == "Rate":
					price[0].price_list_rate = pricing_rule.price_list_rate

			price_obj = price[0]
			if price_obj:
				price_obj["formatted_price"] = fmt_money(price_obj["price_list_rate"], currency=price_obj["currency"])

				price_obj["currency_symbol"] = not cint(frappe.db.get_default("hide_currency_symbol")) \
					and (frappe.db.get_value("Currency", price_obj.currency, "symbol", cache=True) or price_obj.currency) \
					or ""

				uom_conversion_factor = frappe.db.sql("""select	C.conversion_factor
					from `tabUOM Conversion Detail` C
					inner join `tabItem` I on C.parent = I.name and C.uom = I.sales_uom
					where I.name = %s""", item_code)

				uom_conversion_factor = uom_conversion_factor[0][0] if uom_conversion_factor else 1
				price_obj["formatted_price_sales_uom"] = fmt_money(price_obj["price_list_rate"] * uom_conversion_factor, currency=price_obj["currency"])

				if not price_obj["price_list_rate"]:
					price_obj["price_list_rate"] = 0

				if not price_obj["currency"]:
					price_obj["currency"] = ""

				if not price_obj["formatted_price"]:
					price_obj["formatted_price"] = ""

			return price_obj

def get_sp_uom(name):
	if name == "halfday":
		uom = frappe.db.get_value("Shared Place Settings", None, "half_day_uom")
	elif name == "fullday":
		uom = frappe.db.get_value("Shared Place Settings", None, "full_day_uom")
	else:
		uom = frappe.db.get_value("Shared Place Settings", None, "default_uom")
	
	return uom