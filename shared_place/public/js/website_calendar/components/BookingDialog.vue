
<template>
	<modal height="auto" :adaptive="adaptive" name="booking-dialog" @before-open="beforeOpen">
		<div>
			<div class="bookpage-section">
				<h2 class="bookpage-date">{{ date }}</h2>
				<h3 class="bookpage-time">{{ start_time | moment }} - {{ end_time | moment }}</h3>
			</div>
			<div class="bookpage-section">
				<h2 class="bookpage-resource">{{ resource.title }}</h2>
			</div>
			<div class="bookpage-section">
				<div class="input-group number-spinner">
					<span class="input-group-btn">
						<button class="btn btn-default cart-btn" @click="removeQty">–</button>
					</span>
					<input class="form-control text-right cart-qty" v-model="qty" @blur="validateQty">
					<span class="input-group-btn">
						<button class="btn btn-default cart-btn" @click="addQty">+</button>
					</span>
				</div>
			</div>
			<div class="bookpage-section bookpage-footer">
				<button class="btn bookpage-btn" @click="$modal.hide('booking-dialog')">{{ __("Close") }}</button>
				<button class="btn btn-primary bookpage-btn" @click="addToCart">{{ __("Add to cart") }}</button>
			</div>
		</div>
	</modal>
</template>

<script>

import moment from 'moment';

export default {
	name: 'BookingDialog',
	data () {
		return {
			date: null,
			start_time: null,
			end_time: null,
			doctype: null,
			adaptive: true,
			qty: 1,
			events: [],
			resource: {}
		}
	},
	watch: {
		qty: function(val) {
			this.end_time = moment(this.start_time).add(val, 'hours');
		} 
	},
	filters: {
		moment: function (date) {
			return moment(date).format('LT');
		}
	},
	methods: {
		beforeOpen(event) {
			this.date = event.params.date;
			this.start_time = event.params.start_time;
			this.end_time = event.params.end_time;
			this.resource = event.params.resource;
			this.doctype = event.params.doctype;
			this.item = event.params.item;
			this.events = event.params.events;
			this.qty = 1;
		},
		addToCart() {
			const me = this;
			frappe.provide('erpnext.shopping_cart');
			erpnext.shopping_cart.update_cart({
				item_code: this.item,
				qty: this.qty,
				callback: function(r) {
					if ('room' in me.resource) {
						erpnext.shopping_cart.update_cart({
							item_code: me.resource.room_item,
							qty: me.qty,
							callback: function(r) {
								me.$modal.hide('booking-dialog');
							}
						});
					}

					frappe.call({
						method: "shared_place.templates.pages.shared_place_calendar.book_slot",
						args: {
							doctype: me.doctype,
							resource: me.resource,
							start: moment(me.start_time).format('YYYY-MM-DD H:mm:SS'),
							end: moment(me.end_time).format('YYYY-MM-DD H:mm:SS')
						},
						callback: (r) => {
							me.$root.$emit('booking', r.message)
						}
					})

					me.$modal.hide('booking-dialog');
				}
			});

		},
		removeQty() {
			if (this.qty > 1) {
				this.qty -= 1;
			}
		},
		addQty() {
			if (this.events.filter((e) => { return e.start===this.end_time.toISOString() }).length > 0) {
				this.qty += 1;
			}
		},
		validateQty() {
			let end = this.start_time
			for (let i = 1; i <= this.qty; i++) {
				end = moment(this.start_time).add(i, 'hours');
				if (this.events.filter((e) => { return e.start===end.toISOString() }).length > 0) {
					continue;
				} else {
					this.qty = i;
					break;
				}
			}
		}
	}
}
</script>

<style>
.bookpage-section {
	min-height: 110px;
	text-align: center;
	font-weight: 400;
}

.bookpage-section .input-group {
	margin: auto;
}

.bookpage-footer {
	margin-top: 50px;
}

.bookpage-date {
	font-size: 34px;
	margin-top: 50px;
	margin-bottom: 10px;
}

.bookpage-resource {
	font-size: 34px;
	margin-bottom: 10px;
}

.bookpage-time {
	text-align: center;
	font-size: 17px;
	margin-bottom: 15px;
	margin-top: 10px;
}

.bookpage-btn {
	margin-left: 8px;
}

.bookpage-button-set {
	margin-bottom: 8px;
}
</style>