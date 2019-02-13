// Copyright (c) 2019, Dokos and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shared Place Settings', {
	refresh: function(frm) {
		frm.toggle_reqd("half_day_uom", frm.doc.half_day_booking);
		frm.toggle_reqd("half_day_schedule", frm.doc.half_day_booking);
		frm.toggle_reqd("full_day_uom", frm.doc.full_day_booking);
		frm.toggle_reqd("full_day_schedule", frm.doc.full_day_booking);
	},
	half_day_booking: function(frm) {
		frm.toggle_reqd("half_day_uom", frm.doc.half_day_booking);
		frm.toggle_reqd("half_day_schedule", frm.doc.half_day_booking);
	},
	full_day_booking: function(frm) {
		frm.toggle_reqd("full_day_uom", frm.doc.full_day_booking);
		frm.toggle_reqd("full_day_schedule", frm.doc.full_day_booking);
	}
});
