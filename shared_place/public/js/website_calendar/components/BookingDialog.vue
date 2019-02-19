
<template>
	<modal height="auto" :adaptive="adaptive" name="booking-dialog" @before-open="beforeOpen">
		<div>
			<div class="bookpage-section">
				<h2 class="bookpage-date">{{ date }}</h2>
				<h3 class="bookpage-resource">{{ resource.title }}</h3>
			</div>
			<div class="bookpage-section">
				<span class="blue">{{ __("Add or remove an hour") }}</span>
				<div class="input-group number-spinner">
					<span class="input-group-btn">
						<button class="btn btn-default cart-btn" @click="removeQty">–</button>
					</span>
					<input class="form-control text-right cart-qty" v-model="qty" @blur="validateQty">
					<span class="input-group-btn">
						<button class="btn btn-default cart-btn" @click="addQty">+</button>
					</span>
				</div>
				<h2 class="bookpage-time">{{ start_time | moment }} - {{ end_time | moment }}</h2>
			</div>
			<div class="bookpage-section">
				<div class="btn-group" v-if="showOptions()">
					<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
						{{ selectedOption.option || __("Select an option") }}<span class="caret"></span>
					</button>
					<ul class="dropdown-menu">
						<li v-for="option in resource.options" :key="option.name" @click="selectOption(option)"><a>{{ option.option }}</a></li>
					</ul>
				</div>
			</div>
			<div class="bookpage-section">
				<h3 class="bookpage-price green">{{ price }}</h3>
			</div>
			<div class="bookpage-section">
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
	props: ['booked'],
	data () {
		return {
			date: null,
			start_time: null,
			end_time: null,
			doctype: null,
			adaptive: true,
			qty: 1,
			events: [],
			resource: {},
			price: null,
			selectedOption: {},
			item: null
		}
	},
	watch: {
		qty: function(val) {
			this.end_time = moment(this.start_time).add(val, 'hours');
			this.getPrice();
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
			this.events = event.params.events;
			this.qty = 1;
			if (Object.keys(this.resource.options).length) {
				this.selectedOption = this.resource.options[0]
				this.item = this.resource.options[0].item;
			} else {
				this.item = event.params.item;
			}
			this.getPrice();
		},
		addToCart() {
			const me = this;

			this.booked[this.item] = (this.booked[this.item] || 0) + this.qty

			frappe.provide('erpnext.shopping_cart');
			erpnext.shopping_cart.update_cart({
				item_code: this.item,
				qty: this.qty,
				callback: function(r) {
					if ('room' in me.resource && me.resource.room !== null) {
						erpnext.shopping_cart.update_cart({
							item_code: me.resource.room_item,
							qty: me.qty,
							hash: me.hash,
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
		},
		getPrice() {
			frappe.call({
				method: "shared_place.templates.pages.shared_place_calendar.get_slot_price",
				args: {
					"item_code": this.item,
					"price_list": this.resource.price_list,
					"qty": this.qty
				},
				callback: (r) => {
					this.price = r.message;
				}
			});
		},
		showOptions() {
			if (!Object.keys(this.resource).length) {
				return false;
			} else if (!Object.keys(this.resource.options).length) {
				return false;
			} else {
				return true;
			}
		},
		selectOption(option) {
			this.selectedOption = option;
			this.item = option.item;
			this.getPrice();
		}
	}
}
</script>

<style>
.bookpage-section {
	text-align: center;
	font-weight: 400;
	margin-bottom: 50px;
}

.bookpage-section .input-group {
	margin: auto;
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
	margin-top: 20px;
	font-weight: 600;
}

.bookpage-price {
	font-weight: 600;
}

.bookpage-btn {
	margin-left: 8px;
}

.bookpage-button-set {
	margin-bottom: 8px;
}

.blue {
	color: #5e64ff;
}

.green {
	color: #98d85b;
}
</style>