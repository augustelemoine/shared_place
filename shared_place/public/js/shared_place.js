frappe.ready(function() {
	frappe.provide("erpnext.shopping_cart");
	frappe.provide('shared_place.updates');
	frappe.provide('shared_place.utils');

	frappe.call({
		method: "shared_place.shared_place.utils.get_url_list_for_redirect",
		callback: (r) => {
			window.redirects = r.message.links;
			window.calendar_items = r.message.items;
			change_default_btn()
		}
	})

	ready('.shopping-cart-menu', function() {
		change_default_btn()
	});

	ready('.cart-dropdown-container', function() {
		change_default_btn()
	});

	ready('.checkout', function() {
		change_default_btn()
	});

	$('.product-link').on('click', function() {
		if (window.redirects.includes(this.href)) {
			this.href = "/shared_place_calendar"
		}
	})

	shared_place.utils.make_event_emitter(shared_place.updates);
	$("body").on('click', '.sp-remove-btn', function() {
		let item_code = $(this).attr("data-item-code");

		frappe.call({
			method: "shared_place.shared_place.utils.remove_linked_bookings",
			args: {item: item_code}
		}).done(() => {
				erpnext.shopping_cart.shopping_cart_update(item_code, 0, true);
				shared_place.updates.trigger('item_removed', item_code);
				shared_place.updates.trigger('reload_calendar');
		});
	});

})

function change_default_btn() {
	if (window.calendar_items && window.calendar_items.length > 0) {
		window.calendar_items.forEach(item => {
			let $btnWrapper = $('body').find(`[data-item-code="${item}"]`).parent();
			$btnWrapper.removeClass("number-spinner");
			let btnText = __("Remove all items: {0}", [item])
			$btnWrapper.html(`<button class="btn btn-xs sp-remove-btn" data-item-code="${item}">${btnText}</button>`);
		})
	}
}

// Modified from https://github.com/ryanmorr/ready
let observer;
const listeners = [];
const doc = window.document;
const documentElement = doc.documentElement;
let docReady = /complete|loaded|interactive/.test(doc.readyState);

if (!docReady) {
	doc.addEventListener('DOMContentLoaded', () => {
		docReady = true;
		let i = listeners.length;
		while (i--) {
			const listener = listeners[i];
			if (listener.selector === doc) {
				listener.callback.call(doc, doc);
				listeners.splice(i, 1);
			}
		}
	});
}

const matchesFn = [
	'matches',
	'webkitMatchesSelector',
	'msMatchesSelector'
].reduce((fn, name) => {
	if (fn) {
		return fn;
	}
	return name in documentElement ? name : fn;
}, null);

function matches(el, selector) {
	return el[matchesFn](selector);
}

function checkMutations(mutations) {
	for (const mutation of mutations) {
		for (const element of mutation.addedNodes) {
			listeners.forEach((listener) => {
				if (element.nodeType === 1 && matches(element, listener.selector)) {
					listener.callback.call(element, element);
				}
			});
		}

		for (const element of mutation.removedNodes) {
			listeners.forEach((listener) => {
				if (element.nodeType === 1 && matches(element, listener.selector)) {
					listener.callback.call(element, element);
				}
			});
		}
	}
}

function removeListener(listener) {
	let i = listeners.length;
	while (i--) {
		if (listener === listeners[i]) {
			listeners.splice(i, 1);
		}
	}
	if (!listeners.length && observer) {
		observer.disconnect();
		observer = null;
	}
}

function ready(selector, callback) {
	if (!observer) {
		observer = new MutationObserver(checkMutations);
		observer.observe(doc.documentElement, {
			childList: true,
			subtree: true
		});
	}
	if (selector === doc && docReady) {
		callback.call(doc, doc);
		return () => {};
	}
	const listener = {selector, callback};
	listeners.push(listener);
	if (typeof selector === 'string') {
		Array.from(doc.querySelectorAll(selector)).forEach((el) => callback.call(el, el));
	}
	return () => removeListener(listener);
}