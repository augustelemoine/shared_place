<template>
	<div class="text-center">
		<div class="btn-group" role="group" aria-label="unit of measure">
			<button v-for="(value, key) in available_uoms" :key="key" type="button" class="btn btn-default" @click="changeUom(key)">{{ value }}</button>
		</div>
	</div>
</template>

<script>

export default {
	name: 'UomSection',
	props: ['available_uoms', 'uom', 'changeUom']
}
</script>