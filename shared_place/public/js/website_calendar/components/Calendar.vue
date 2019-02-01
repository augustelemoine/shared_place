<template>
	<div>
		<full-calendar ref="calendar" :config="config" :events="events"/>
		<booking-dialog/>
	</div>
</template>

<script>
	import 'fullcalendar/dist/locale/fr'
	import moment from 'moment';
	import BookingDialog from './BookingDialog.vue';

	export default {
		name: 'calendar',
		components: {
			BookingDialog
		},
		data () {
			return {
				events: [],
				resources: []
			}
		},
		created() {
			this.getSettings();
			this.$root.$on('booking', (response) => {
				 this.$refs.calendar.$emit('refetch-events');
			})

			this.$root.$on('reload_calendar', () => {
				this.$refs.calendar.$emit('refetch-events');
			})
		},
		mounted() {
			this.getResources();
		},
		computed: {
			config() {
				return {
					locale: frappe.boot.lang,
					header: {
						left: 'prev,next today',
						center: 'title',
						right: 'timelineDay,timelineWeek,timelineMonth'
					},
					schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
					resourceAreaWidth: "20%",
					defaultView: "timelineDay",
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
								'end': moment(end).format("YYYY-MM-DD")
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
					maxTime: '21:00:00',
					slotDuration: '60',
					scrollTime: '06:00:00',
					weekends: false,
					defaultDate: moment(new Date()).add(1,'days'),
					handleWindowResize: false,
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
						this.$refs.calendar.fireMethod('refetchResources');
					}
				})
			},
			showBookingDialog(event) {
				let res = this.resources.filter((e) => { return e.id===event.resourceId})[0]
				if ('room' in res) {
					let correpondingRoom = this.resources.filter((e) => { return e.id===res.room})[0]
					res['room_item'] = correpondingRoom.item
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
					method: 'frappe.client.get',
					args: {
						"doctype": "Shared Place Settings",
						"name": "Shared Place Settings",
					},
					callback: (r) => {
						this.$refs.calendar.fireMethod('option', 'minTime', r.message.calendar_start_time);
						this.$refs.calendar.fireMethod('option', 'scrollTime', r.message.calendar_start_time);
						this.$refs.calendar.fireMethod('option', 'maxTime', r.message.calendar_end_time);
						this.$refs.calendar.fireMethod('option', 'slotDuration', r.message.minimum_booking_time_mins);
						this.$refs.calendar.fireMethod('option', 'weekends', r.message.week_end_bookings);
					}
				});
			}
		}
	}

</script>

<style></style>