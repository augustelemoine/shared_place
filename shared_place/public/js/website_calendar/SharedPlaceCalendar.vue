<template>
	<div>
		<div id="shared_place_calendar">
			<calendar :booked='booked'></calendar>
		</div>
	</div>
</template>

<script>
	import Calendar from './components/Calendar.vue';

	export default {
		name: 'shared_place_calendar',
		data() {
			return {
				booked: {}
			}
		},
		components: {
			Calendar
		},
		created() {
			shared_place.updates.on('reload_calendar', () => {
				this.$root.$emit('reload_calendar')
			})
			shared_place.updates.on('item_removed', (data) => {
				this.booked[data] = 0;
			})
		},
		mounted() {
			this.getBooked();
		},
		methods: {
			getBooked() {
				frappe.call({
					method: "shared_place.templates.pages.shared_place_calendar.get_booked_items",
					callback: (r) => {
						this.booked = r.message;
					}
				})
			}
		}
	}
</script>

<style></style>