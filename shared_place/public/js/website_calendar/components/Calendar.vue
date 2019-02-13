<template>
	<div>
		<resource-selector v-if="frappe.is_mobile()" :selectResource="selectResource" :resources="resources" :selectedResource="selectedResource"/>
		<uom-section :available_uoms="available_uoms" :uom="uom" :changeUom="uomChanged"/>
		<full-calendar v-if="showCalendar()" ref="calendar" :config="config" :events="events"/>
		<booking-dialog :booked="booked"/>
	</div>
</template>

<script>
	import 'fullcalendar-scheduler';
	import 'fullcalendar/dist/locale/fr'
	import moment from 'moment';
	import BookingDialog from './BookingDialog.vue';
	import UomSection from './UomSection.vue';
	import resourceSelector from './resourceSelector.vue'

	export default {
		name: 'calendar',
		props: ['booked'],
		components: {
			BookingDialog,
			UomSection,
			resourceSelector
		},
		data () {
			return {
				events: [],
				resources: [],
				available_uoms: ["hour"],
				uom: "hour",
				selectedResource: {}
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
			this.getResources();
		},
		computed: {
			config() {
				return {
					locale: frappe.boot.lang,
					header: {
						left: 'prev,next today',
						center: frappe.is_mobile() ? '' : 'title',
						right: frappe.is_mobile() ? '' :'timelineDay,timelineWeek,timelineMonth'
					},
					schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
					resourceAreaWidth: "20%",
					defaultView: frappe.is_mobile() ? "listWeek": "timelineDay",
					resourceLabelText: "Room/Resources",
					resourceGroupField: "category",
					resources: (callback) => {
						callback(this.resources);
					},
					events: (start, end, timezone, callback) => {
						frappe.call({
							method: "shared_place.templates.pages.shared_place_calendar.check_availabilities",
							args: {
								'start':  moment(start).format("YYYY-MM-DD"), 
								'end': moment(end).format("YYYY-MM-DD"),
								'uom': this.uom,
								'resources': frappe.is_mobile() ? (Object.keys(this.selectedResource).length ? [this.selectedResource] : []) : this.resources
							},
							callback: (r) => {
								this.events = r.message;
								callback(this.events)
							}
						})
					},
					eventClick: (event) => {
						this.showBookingDialog(event)
					},
					allDaySlot: false,
					minTime: '06:00:00',
					maxTime: '20:00:00',
					slotDuration: '60',
					scrollTime: '06:00:00',
					height: frappe.is_mobile() ? 1000 : "auto",
					contentHeight: frappe.is_mobile() ? 1000 : "auto",
					aspectRatio: 4,
					weekends: false,
					defaultDate: moment(new Date()).add(1,'days'),
					handleWindowResize: true,
					editable: false,
					timeFormat: 'H(:mm)'
				}
				}
		},
		methods: {
			getResources() {
				frappe.call({
					method: "shared_place.templates.pages.shared_place_calendar.get_rooms_and_resources",
					callback: (r) => {
						this.resources = r.message;
						this.getSettings();
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
			getSettings() {
				frappe.call({	
					method: 'shared_place.templates.pages.shared_place_calendar.get_settings',
					callback: (r) => {
						this.$refs.calendar.fireMethod('option', {
							'minTime': r.message[0].calendar_start_time,
							'scrollTime': r.message[0].calendar_start_time,
							'maxTime': r.message[0].calendar_end_time,
							'slotDuration': (parseInt(r.message[0].minimum_booking_time) * 60).toString(),
							'weekends': r.message[0].week_end_bookings
							});
						this.$refs.calendar.fireMethod('refetchResources');
						this.$refs.calendar.$emit('refetch-events');
					}
				});
			},
			uomChanged(value) {
				this.uom = value;
				this.$refs.calendar.$emit('refetch-events');
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
				this.$refs.calendar.$emit('refetch-events');
			},
			showCalendar() {
				if (frappe.is_mobile()) {
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

<style></style>