# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dokos and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
import datetime
from frappe.utils import getdate, get_datetime, get_datetime_str, add_days, cstr, date_diff, add_months, cint

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

class SharedPlaceBooking(Document):
	def on_submit(self):
		pass

	def on_trash(self):
		linked_docs = frappe.get_all(self.doctype, filters={"linked_booking": self.name, "docstatus": 0, "name": ["!=", self.name]})
		if linked_docs:
			for doc in linked_docs:
				frappe.db.set_value(self.doctype, doc.name, "linked_booking", "")
				frappe.delete_doc(self.doctype, doc.name, ignore_permissions=True)
				frappe.db.commit()

		elif self.linked_booking:
			frappe.delete_doc(self.doctype, self.linked_booking, ignore_permissions=True)
			frappe.db.commit()


@frappe.whitelist()
def get_events(start, end, filters=None):
	from frappe.desk.calendar import get_event_conditions
	add_filters = get_event_conditions("Shared Place Booking", filters)

	events = frappe.db.sql("""select name, title, booked_by, booking_type, booked_resource, color, starts_on, ends_on, repeat_this_event, repeat_on, repeat_till,
		monday, tuesday, wednesday, thursday, friday, saturday, sunday, docstatus from `tabShared Place Booking` where ((
		(date(starts_on) between date(%(start)s) and date(%(end)s))
		or (date(ends_on) between date(%(start)s) and date(%(end)s))
		or (date(starts_on) <= date(%(start)s) and date(ends_on) >= date(%(end)s))
		) or (
		date(starts_on) <= date(%(start)s) and repeat_this_event=1 and
		ifnull(repeat_till, "3000-01-01") >= date(%(start)s)
		))and docstatus < 2 {add_filters}""".format(add_filters=add_filters), {
		"start": start,
		"end": end
	}, as_dict=True, update={"allDay": 0})

	# process recurring events
	start = start.split(" ")[0]
	end = end.split(" ")[0]
	add_events = []
	remove_events = []

	def add_event(e, date):
		new_event = e.copy()

		enddate = add_days(date, int(date_diff(e.ends_on.split(" ")[0], e.starts_on.split(" ")[0]))) \
			if (e.starts_on and e.ends_on) else date
		new_event.starts_on = date + " " + e.starts_on.split(" ")[1]
		if e.ends_on:
			new_event.ends_on = enddate + " " + e.ends_on.split(" ")[1]
		add_events.append(new_event)

	for e in events:
		if e.repeat_this_event:
			e.starts_on = get_datetime_str(e.starts_on)
			if e.ends_on:
				e.ends_on = get_datetime_str(e.ends_on)

			event_start, dummy = get_datetime_str(e.starts_on).split(" ")
			if cstr(e.repeat_till) == "":
				repeat = "3000-01-01"
			else:
				repeat = e.repeat_till
			if e.repeat_on == "Every Year":
				start_year = cint(start.split("-")[0])
				end_year = cint(end.split("-")[0])
				event_start = "-".join(event_start.split("-")[1:])

				# repeat for all years in period
				for year in range(start_year, end_year + 1):
					date = str(year) + "-" + event_start
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) and getdate(date) <= getdate(repeat):
						add_event(e, date)

				remove_events.append(e)

			if e.repeat_on == "Every Month":
				date = start.split(
					"-")[0] + "-" + start.split("-")[1] + "-" + event_start.split("-")[2]

				# last day of month issue, start from prev month!
				try:
					getdate(date)
				except ValueError:
					date = date.split("-")
					date = date[0] + "-" + \
						str(cint(date[1]) - 1) + "-" + date[2]

				start_from = date
				for i in range(int(date_diff(end, start) / 30) + 3):
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) \
					   and getdate(date) <= getdate(repeat) and getdate(date) >= getdate(event_start):
						add_event(e, date)
					date = add_months(start_from, i + 1)

				remove_events.append(e)

			if e.repeat_on == "Every Week":
				weekday = getdate(event_start).weekday()
				# monday is 0
				start_weekday = getdate(start).weekday()

				# start from nearest weeday after last monday
				date = add_days(start, weekday - start_weekday)

				for cnt in range(int(date_diff(end, start) / 7) + 3):
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) \
						and getdate(date) <= getdate(repeat) and getdate(date) >= getdate(event_start):
						add_event(e, date)

					date = add_days(date, 7)

				remove_events.append(e)

			if e.repeat_on == "Every Day":
				for cnt in range(date_diff(end, start) + 1):
					date = add_days(start, cnt)
					if getdate(date) >= getdate(event_start) and getdate(date) <= getdate(end) \
					   and getdate(date) <= getdate(repeat) and e[weekdays[getdate(date).weekday()]]:
						add_event(e, date)
				remove_events.append(e)

	for e in remove_events:
		events.remove(e)

	events = events + add_events

	for e in events:
		# remove weekday properties (to reduce message size)
		for w in weekdays:
			del e[w]

	return events
