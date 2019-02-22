// Copyright (c) 2019,Dokos and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on(this.frm.doctype, {
	refresh: function(frm) {
		frm.add_custom_button(__('Show linked prices'), () => { 
			check_if_item_price_exists(frm);
		});
	}
});

function check_if_item_price_exists(frm) {
	frappe.call('shared_place.shared_place.doctype.shared_place_settings.shared_place_settings.check_pricing', { doc: frm.doc })
	.then(r => {
		const msg = frappe.render_template(prices_template, {data: r.message})
		
		if (r.message.length > 0) {
			frappe.msgprint(msg)
		} else {
			frappe.msgprint(__("Please setup prices for this item before allowing online booking"))
		}
		
	})
}

const prices_template = `
	<div>
	{% for row in data %}
	<h2>{{ __(row.uom) }} : <span>{{ row.price }}</span></h2>
	{% endfor%}
	</div>
`