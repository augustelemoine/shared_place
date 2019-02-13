# -*- coding: utf-8 -*-
# Copyright (c) 2019, DOKOS and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, datetime, calendar, json
from frappe import _
from frappe.utils import getdate, get_time, now_datetime, cint, get_datetime, add_days, format_datetime, fmt_money
from datetime import timedelta, date
from shared_place.shared_place.utils import get_resource_price_and_qty
from shared_place.shared_place.doctype.shared_place_booking.shared_place_booking import get_registered_slots

def get_context(context):
	context.no_cache = 1

@frappe.whitelist(allow_guest=True)
def get_rooms_and_resources():
	coworking = [dict(x,**{"doctype": "Shared Place Coworking Space","category": _("Coworking Spaces")}) for x in frappe.get_all("Shared Place Coworking Space", \
		filters={"allow_online_booking": 1}, fields=['name as id', 'coworking_space as title', 'item', 'number_of_seats', 'price_list', 'half_day_booking', 'full_day_booking'])]
	rooms = [dict(x,**{"doctype": "Shared Place Room","category": _("Rooms")}) for x in frappe.get_all("Shared Place Room", \
		filters={"allow_online_booking": 1}, fields=['name as id', 'room_name as title', 'item', 'price_list', 'half_day_booking', 'full_day_booking'])]
	resources = [dict(x,**{"doctype": "Shared Place Resource", "category": _("Resources")}) for x in frappe.get_all("Shared Place Resource", \
		filters={"allow_online_booking": 1}, fields=['name as id', 'resource_name as title', 'item', 'room', 'price_list', 'half_day_booking', 'full_day_booking'])]

	result = []
	if coworking:
		result.extend(coworking)
	if rooms:
		result.extend(rooms)
	if resources:
		result.extend(resources)
	return result


@frappe.whitelist(allow_guest=True)
def get_uoms():
	half_day = frappe.db.get_value("Shared Place Settings", None, "half_day_booking")
	full_day = frappe.db.get_value("Shared Place Settings", None, "full_day_booking")

	result = ['hour']
	if half_day and int(half_day) == 1:
		result.append('halfday')
	if full_day and int(full_day) == 1:
		result.append('fullday')

	return result

@frappe.whitelist(allow_guest=True)
def get_settings():
	return frappe.db.get_values("Shared Place Settings", None, ["calendar_start_time", "calendar_end_time", "minimum_booking_time", "week_end_bookings"], as_dict=True)

def daterange(start_date, end_date):
	if start_date < now_datetime():
		start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

@frappe.whitelist(allow_guest=True)
def check_availabilities(start, end, resources, uom='hour'):
	final_avail = []
	resources = json.loads(resources)
	linked_resource = False

	for resource in resources:

		if resource['doctype'] == "Shared Place Coworking Space": 
			group = True 
		else: 
			group = False

		if 'room' in resource and resource['room'] is not None:
			linked_resource = True
			original_resource = resource.copy()
			resource = frappe.db.get_values("Shared Place Room", resource['room'], ['name as id', 'room_name as title', 'item'], as_dict=True)[0]
			resource.update({"doctype": "Shared Place Room"})

		linked_item = frappe.db.get_values(resource['doctype'], resource['id'], ['item', 'price_list'], as_dict=True)[0]
		resource_details = get_resource_price_and_qty({ "item_code": linked_item.item, "price_list": linked_item.price_list})

		if resource_details and resource_details[0].min_qty:
			minimum_booking_time = frappe.db.get_value("Shared Place Settings", None, "minimum_booking_time")
			if minimum_booking_time:
				duration = (int(minimum_booking_time) * 60)
				init = datetime.datetime.strptime(start, '%Y-%m-%d')
				finish = datetime.datetime.strptime(end, '%Y-%m-%d')
				days_limit = frappe.db.get_value("Shared Place Settings", None, "limit") or 360
				limit = datetime.datetime.combine(add_days(getdate(), cint(days_limit)), datetime.datetime.time(datetime.datetime.now()))

				payload = []
				if init < limit:
					for dt in daterange(init, finish):
						date = dt.strftime("%Y-%m-%d")

						calendar_availability = _check_availability(resource, date, duration, group, uom)

						if bool(calendar_availability) == True:
							if bool(linked_resource) == True:
								avail = [dict(x,**{"resourceId": original_resource["id"], "resourceDt": original_resource['doctype'], "item": original_resource['item']}) for x in calendar_availability]
							else:
								avail = [dict(x,**{"resourceId": resource["id"], "resourceDt": resource['doctype'], "item": resource['item']}) for x in calendar_availability]

							payload += avail


						if resource['doctype'] == "Shared Place Coworking Space":
							payload = get_coworking_availabilities(resource, payload, start, end)

				final_avail.extend(payload)
	return final_avail

def get_coworking_availabilities(resource, payload, start, end):
	registered = get_registered_slots(resource, start)
	
	result = []
	for slot in payload:
		filtered_registrations = [d for d in registered if \
			get_datetime(slot["start"])<get_datetime(d["ends_on"]) and get_datetime(slot["end"])>get_datetime(d["starts_on"])]
		slot["registered"] = len(filtered_registrations)

		if slot["registered"] < resource["number_of_seats"]:
			result.append(slot)

	return result

def _check_availability(resource, date, duration, group, uom):
	date = getdate(date)
	day = calendar.day_name[date.weekday()]
	if (date < getdate()):
		return

	availability = []
	schedules = []

	uom_dict = {"hour": {"field": "custom_schedule", "schedule": "schedule"}, \
		"halfday": {"field": "half_day_booking", "schedule": "half_day_schedule"}, \
		"fullday": {"field": "full_day_booking", "schedule": "full_day_schedule"}
	}

	schedule = uom_dict[uom]["schedule"]
	if uom in ["halfday", "fullday"]:
		if frappe.db.get_value(resource['doctype'], resource['id'], uom_dict[uom]["field"]) == 1:
			sch_settings = frappe.get_doc("Shared Place Settings", None)
		else:
			return availability
	elif frappe.db.get_value(resource['doctype'], resource['id'], uom_dict[uom]["field"]) == 1:
		sch_settings = frappe.get_doc(resource['doctype'], resource['id'])
	else:
		sch_settings = frappe.get_doc("Shared Place Settings", None)
	

	if getattr(sch_settings, schedule):
		day_sch = filter(lambda x: x.day == day, getattr(sch_settings, schedule))
		if not day_sch:
			return availability

		for line in day_sch:
			if(datetime.datetime.combine(date, get_time(line.end_time)) > now_datetime()):

				if uom == "hour":
					duration = datetime.timedelta(minutes=cint(duration))
				else:
					diff = datetime.datetime.combine(date, get_time(line.end_time)) - datetime.datetime.combine(date, get_time(line.start_time))
					duration = datetime.timedelta(minutes=cint(diff.seconds/60))
	
				schedules.append({"start": datetime.datetime.combine(date, get_time(line.start_time)), "end": datetime.datetime.combine(
					date, get_time(line.end_time)), "duration": duration})

		if schedules:
			availability.extend(get_availability_from_schedule(resource, schedules, date, group, uom))

	return availability

def get_availability_from_schedule(resource, schedules, date, group, uom):
	from shared_place.shared_place.doctype.shared_place_booking.shared_place_booking import get_events
	data = []
	for line in schedules:
		duration = get_time(line["duration"])

		if group:
			event_list = []

		else:
			events = get_events(line["start"].strftime("%Y-%m-%d %H:%M:%S"), \
				line["end"].strftime("%Y-%m-%d %H:%M:%S"), \
				filters=[["Shared Place Booking","booking_type","=", resource['doctype']], ["Shared Place Booking","booked_resource","=", resource['id']]])

			if events and uom != "hour":
				return []

			event_list = []
			for event in events:
				if (get_datetime(event.starts_on) >= line["start"] and get_datetime(event.starts_on) <= line["end"]) \
					or get_datetime(event.ends_on) >= line["start"]:
					event_list.append(event)

		available_slot = find_available_slot(date, duration, line, event_list)
		data.extend(available_slot)

	return data

def find_available_slot(date, duration, line, scheduled_items):
	available_slots = []
	current_schedule = []
	if scheduled_items:
		for scheduled_item in scheduled_items:

			if get_datetime(scheduled_item.starts_on) < line["start"]:
				new_entry = (get_datetime(line["start"]),
							 get_datetime(scheduled_item.ends_on))
			elif get_datetime(scheduled_item.starts_on) < line["end"]:
				new_entry = (get_datetime(scheduled_item.starts_on),
						 get_datetime(scheduled_item.ends_on))
			try:
				current_schedule.append(new_entry)
			except:
				pass

		scheduled_items = sorted(current_schedule, key = lambda x: x[0])
		final_schedule = list(reduced(scheduled_items))
		slots = get_all_slots(
			line["start"], line["end"], line["duration"], final_schedule)

		for slot in slots:
			available_slots.append(get_dict(slot[0], slot[1]))

		return available_slots

	else:
		slots = get_all_slots(line["start"], line["end"], line["duration"])

		for slot in slots:
			available_slots.append(get_dict(slot[0], slot[1]))

		return available_slots


def get_all_slots(day_start, day_end, time_delta, scheduled_items=None):
	interval = int(time_delta.total_seconds() / 60)

	if scheduled_items:
		slots = sorted([(day_start, day_start)] +
					scheduled_items + [(day_end, day_end)])
	else:
		slots = sorted([(day_start, day_start)] + [(day_end, day_end)])

	free_slots = []
	for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
		while start + timedelta(minutes=interval) <= end:
			free_slots.append([start, start + timedelta(minutes=interval)])
			start += timedelta(minutes=interval)
	return free_slots


def get_dict(start, end, slots=None):
	return {
		"start": start.isoformat(), 
		"end": end.isoformat(), 
		"title": "{0}-{1}".format(format_datetime(start, "HH:mm"), format_datetime(end, "HH:mm"))
	}

def reduced(timeseries):
	prev = datetime.datetime.min
	for start, end in timeseries:
		if end > prev:
			prev = end
			yield start, end

@frappe.whitelist(allow_guest=True)
def get_booked_items():
	from erpnext.shopping_cart.cart import get_cart_quotation
	doc = get_cart_quotation()

	items = {}
	for item in doc["doc"].items:
		items.update({item.item_code: item.stock_qty})

	return items

@frappe.whitelist(allow_guest=True)
def get_slot_price(item_code, qty, price_list=None):
	from erpnext.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import get_shopping_cart_settings
	from erpnext.utilities.product import get_price

	settings = get_shopping_cart_settings()

	if not price_list:
		price_list = settings.price_list

	price = get_price(item_code, price_list, settings.default_customer_group, settings.company, qty)
	return fmt_money(float(price.price_list_rate) * float(qty), currency=price.currency)

@frappe.whitelist()
def book_slot(doctype, resource, start, end):
	from erpnext.shopping_cart.cart import _get_cart_quotation
	user = frappe.db.get_values("User", frappe.session.user, ["full_name", "name"], as_dict=True)[0]
	resource = json.loads(resource)
	bookings = {"quotation": None, "bookings": []}

	quotation = _get_cart_quotation()
	bookings["quotation"] = quotation.name

	booking = frappe.get_doc({
		"doctype": "Shared Place Booking",
		"booking_type": doctype,
		"booked_resource": resource['id'],
		"booked_by": user.name,
		"starts_on": start,
		"ends_on": end,
		"title": user.full_name,
		"quotation": quotation.name
	}).insert()

	if 'room' in resource and resource['room'] is not None:

		room_booking = frappe.get_doc({
			"doctype": "Shared Place Booking",
			"booking_type": "Shared Place Room",
			"booked_resource": resource['room'],
			"booked_by": user.name,
			"starts_on": start,
			"ends_on": end,
			"title": user.full_name,
			"quotation": quotation.name
		}).insert()

		booking.linked_booking = room_booking.name
		booking.save(ignore_permissions=True)

		bookings["bookings"].append(room_booking)

	bookings["bookings"].append(booking)
	frappe.clear_cache()

	return bookings


