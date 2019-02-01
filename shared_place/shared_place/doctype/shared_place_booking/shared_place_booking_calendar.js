frappe.views.calendar["Shared Place Booking"] = {
	field_map: {
		"start": "starts_on",
		"end": "ends_on",
		"id": "name",
		"title": "title",
		"color": "color"
	},
	gantt: false,
	get_events_method: "shared_place.shared_place.doctype.shared_place_booking.shared_place_booking.get_events",
	filters: [
		{
			'fieldtype': 'Link',
			'fieldname': 'booked_by',
			'options': 'User',
			'label': __('Booked by')
		}
	]
}