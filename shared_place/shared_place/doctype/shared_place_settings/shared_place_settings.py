# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dokos and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.utils import fmt_money, flt

class SharedPlaceSettings(Document):
	pass


@frappe.whitelist()
def check_pricing(doc):
	doc = json.loads(doc)
	settings = frappe.get_doc("Shared Place Settings", None)

	item_prices = frappe.get_all("Item Price", {"item_code": doc["item"], "price_list": doc["price_list"]}, ["item_code", "uom", "price_list_rate", "currency"])

	result = []
	for price in item_prices:
		if (price.uom == None or price.uom == settings.default_uom):
			result.append({'uom': settings.default_uom, 'price': fmt_money(flt(price.price_list_rate), currency=price.currency)})

		if settings.half_day_booking == 1 and settings.half_day_uom == price.uom:
			result.append({'uom': settings.half_day_uom, 'price': fmt_money(flt(price.price_list_rate), currency=price.currency)})

		if settings.full_day_booking == 1 and settings.full_day_uom == price.uom:
			result.append({'uom': settings.full_day_uom, 'price': fmt_money(flt(price.price_list_rate), currency=price.currency)})

	return result