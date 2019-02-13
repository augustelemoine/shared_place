<template>
	<ul class="nav nav-pills nav-justified">
		<li v-if="available_uoms.indexOf('hour') > -1 && available_uoms.length > 1" :class="uom=='hour' ? 'active' : ''" @click="changeUom('hour')"><a href="#">{{ __("Hour") }}</a></li>
		<li v-if="available_uoms.indexOf('halfday') > -1" :class="uom=='halfday' ? 'active' : ''" @click="changeUom('halfday')"><a href="#">{{ __("Half-day") }}</a></li>
		<li v-if="available_uoms.indexOf('fullday') > -1" :class="uom=='fullday' ? 'active' : ''" @click="changeUom('fullday')"><a href="#">{{ __("Full-day") }}</a></li>
	</ul>
</template>

<script>


export default {
	name: 'UomSection',
	props: ['available_uoms', 'uom', 'changeUom']
}
</script>

<style>
.nav-pills > li.active > a,
.nav-pills > li.active > a:hover,
.nav-pills > li.active > a:focus {
	background-color: #d2e3ee;
}

.nav-pills > li {
	line-height: 0.8em;
}

.nav-justified {
	width: 60% !important;
	margin: auto;
}
</style>