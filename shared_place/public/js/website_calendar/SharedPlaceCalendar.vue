<template>
	<div>
		<div id="shared_place_calendar">
			<calendar></calendar>
		</div>
	</div>
</template>

<script>
	import Calendar from './components/Calendar.vue';

	export default {
		name: 'shared_place_calendar',
		components: {
			Calendar
		},
		created() {
			shared_place.updates.on('reload_calendar', () => {
				this.$root.$emit('reload_calendar')
			})
		}
	}
</script>

<style></style>