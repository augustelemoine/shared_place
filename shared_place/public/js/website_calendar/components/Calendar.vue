<template>
	<div>
		<help-text :helpText="helpText"/>
		<resource-selector v-if="this.isMobile()" :selectResource="selectResource" :resources="selectableResources" :selectedResource="selectedResource"/>
		<uom-section v-if="showUOMSection()" :available_uoms="available_uoms" :uom="uom" :changeUom="uomChanged"/>
		<div class="text-center">
			<a v-if="this.route!==null" :href="route">{{ __("Buy units without selecting a slot") }}</a>
		</div>
		<full-calendar v-if="showCalendar()" ref="calendar" :config="config" :events="events"/>
		<booking-dialog :booked="booked" :uom="uom"/>
	</div>
</template>

<script>
	import 'fullcalendar-scheduler';
	import 'fullcalendar/dist/locale/fr'
	import moment from 'moment';
	import BookingDialog from './BookingDialog.vue';
	import UomSection from './UomSection.vue';
	import resourceSelector from './resourceSelector.vue'
	import helpText from './helpText.vue'

	export default {
		name: 'calendar',
		props: ['booked', 'isMobile', 'lang'],
		components: {
			BookingDialog,
			UomSection,
			resourceSelector,
			helpText
		},
		data () {
			return {
				events: [],
				resources: [],
				available_uoms: [],
				uom: null,
				selectedResource: {},
				selectableResources: [],
				helpText: null,
				route: null
			}
		},
		created() {
			this.$root.$on('booking', (response) => {
				this.$refs.calendar.$emit('refetch-events');
			})

			this.$root.$on('reload_calendar', () => {
				this.$refs.calendar.$emit('refetch-events');
			})

		},
		mounted() {
			this.getUoms();
			this.getSettings(false);
			if (window.location.href) {
				this.route = new URL(window.location.href).searchParams.get("route")
			}
			if (this.isMobile()) {
				this.getResources();
			}
		},
		computed: {
			config() {
				return {
					locale: Vue.prototype.frappe.lang,
					header: {
						left: 'prev,next today',
						center: this.isMobile() ? '' : 'title',
						right: this.isMobile() ? '' :'timelineDay,timelineWeek,timelineMonth'
					},
					schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
					resourceAreaWidth: "20%",
					defaultView: this.isMobile() ? "listWeek": "timelineDay",
					resourceLabelText: __("Rooms/Resources"),
					resourceGroupField: "category",
					resources: (callback) => {
						callback(this.resources);
					},
					resourceRender: function(resourceObj, labelTds, bodyTds) {
						if (resourceObj.selected === 1) {
							labelTds.css('font-weight', '600');
							labelTds.css('background-color', '#d1d3fc');
						}
						labelTds.eq(0).find('.fc-cell-content').popover({
								html: true,
								title: resourceObj.id,
								content: resourceObj.description,
								trigger: 'hover',
								placement: 'bottom',
								container: 'body',
							});
					},
					events: (start, end, timezone, callback) => {
						frappe.call({
							method: "shared_place.templates.pages.shared_place_calendar.check_availabilities",
							args: {
								'start':  moment(start).format("YYYY-MM-DD"), 
								'end': moment(end).format("YYYY-MM-DD"),
								'uom': this.uom,
								'resources': this.isMobile() ? (Object.keys(this.selectedResource).length ? [this.selectedResource] : []) : this.resources
							},
							callback: (r) => {
								if (r.message.length) {
									this.events = r.message;
								} else {
									this.events = [
										{
											end: end,
											start: start,
											title: __("No slot available"),
											rendering: "background",
											backgroundColor: "#FBFBFB"
										}
									]
								}
								callback(this.events)
							}
						})
					},
					eventRender: function (event, element) {
						if (event.rendering == 'background') {
							element.append(`<div class="no-events">${event.title}</div>`);
						}
					},
					eventClick: (event) => {
						this.showBookingDialog(event)
					},
					allDaySlot: false,
					minTime: '06:00:00',
					maxTime: '20:00:00',
					slotDuration: '60',
					scrollTime: '06:00:00',
					height: this.isMobile() ? 1000 : "auto",
					contentHeight: this.isMobile() ? 1000 : "auto",
					aspectRatio: 4,
					weekends: false,
					defaultDate: moment(new Date()).add(1,'days'),
					handleWindowResize: true,
					editable: false,
					timeFormat: 'H(:mm)',
					noEventsMessage: __("No slot available"),
					displayEventTime: false,
					titleFormat: 'D MMMM YYYY',
					slotLabelFormat: Vue.prototype.frappe.lang == 'fr' ? 'H:mm' : 'h(:mm)a',
					loading: function( isLoading, view ) {
						if (isLoading) {
							frappe.freeze();
						} else {
							frappe.unfreeze();
						}
					}
				}
				}
		},
		methods: {
			getResources() {
				frappe.call({
					method: "shared_place.templates.pages.shared_place_calendar.get_rooms_and_resources",
					args: {
						'route': this.route || new URL(window.location.href).searchParams.get("route")
					},
					callback: (r) => {
						this.resources = r.message;
						this.selectableResources = r.message.filter(f => f.selected === 1);
						if (!this.isMobile()) {
							this.getSettings(true);
						}
					}
				})
			},
			showBookingDialog(event) {
				let res = this.resources.filter((e) => { return e.id===event.resourceId})[0]
				if ('room' in res && res.room !== null) {
					let correspondingRoom = this.resources.filter((e) => { return e.id===res.room})[0]
					res['room_item'] = correspondingRoom.item
				}
				this.$modal.show('booking-dialog', {
					date: moment(event.start).format('LL'),
					start_time: event.start,
					end_time: event.end,
					doctype: event.resourceDt,
					item: event.item,
					events: this.events.filter((e) => { return e.resourceId===event.resourceId}),
					resource: res
				})
			},
			getSettings(cal) {
				frappe.call({	
					method: 'shared_place.templates.pages.shared_place_calendar.get_settings',
					callback: (r) => {
						this.helpText = r.message.calendar_help_text;

						if (cal) {
							this.$refs.calendar.fireMethod('option', {
							'locale': r.message.lang,
							'minTime': r.message.calendar_start_time,
							'scrollTime': r.message.calendar_start_time,
							'maxTime': r.message.calendar_end_time,
							'slotDuration': (parseInt(r.message.minimum_booking_time) * 60).toString(),
							'weekends': r.message.week_end_bookings
						});
						this.$refs.calendar.fireMethod('refetchResources');
						this.$refs.calendar.$emit('refetch-events');
						}
					}
				});
			},
			uomChanged(value) {
				const oldValue = this.uom;
				this.uom = value;
				if (oldValue === null) {
					this.getResources();
				} else {
					this.$refs.calendar.$emit('refetch-events');
				}
			},
			getUoms() {
				frappe.call({
					method: "shared_place.templates.pages.shared_place_calendar.get_uoms",
					callback: (r) => {
						this.available_uoms = r.message;
					}
				})
			},
			selectResource(res) {
				this.selectedResource = res;
				if (this.$refs.calendar) {
					this.$refs.calendar.$emit('refetch-events');
				}

			},
			showCalendar() {
				if (this.isMobile()) {
					if (Object.keys(this.selectedResource).length && this.uom !== null) {
						return true;
					} else {
						return false;
					}
				} else {
					if (this.uom !== null) {
						return true;
					} else {
						return false;
					}
				}
			},
			showUOMSection() {
				if (this.isMobile()) {
					if (Object.keys(this.selectedResource).length) {
						return true;
					} else {
						return false;
					}
				} else {
					return true;
				}
			}
		}
	}

</script>

<style>

.fc-bgevent {
	text-align: center;
	opacity: 0.8;
}

.no-events {
	margin-top: 15%;
	width: 100px;
	height: 100px;
	display: inline-block;
	opacity: 90%;
}

</style>