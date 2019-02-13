// Copyright (c) 2019, Dokos and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shared Place Booking', {
	onload(frm) {
		frm.set_query("booking_type", function() {
			return {
				filters: {
					name: ['in', ['Shared Place Room', 'Shared Place Resource', 'Shared Place Coworking Space']]
				}
			}
		})
	},
	refresh(frm) {
		if (!frm.doc.booked_by) {
			frm.set_value("booked_by", frappe.session.user);
			frm.refresh_field("booked_by");
		}
	},
	booked_resource(frm) {
		if (frm.doc.booked_resource) {
			frm.set_value("title", frm.doc.booked_resource);
			frm.refresh_field("title");
		}
	}
});
